from datetime import datetime

from functools import wraps
import pandas as pd
import pymysql
import pymysql.cursors
from pymysql import MySQLError
import time

from echoss_fileformat import FileUtil, get_logger

logger = get_logger("echoss_query")


def log_execution_time(func):
    """Decorator to log the execution time of a method if use_query_debug is True."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not getattr(self, 'use_query_debug', False):
            # If use_query_debug is False, just call the function without logging
            return func(self, *args, **kwargs)

        # Start timing
        start_time = time.time()
        try:
            # Execute the original function
            result = func(self, *args, **kwargs)
            return result
        finally:
            # End timing
            end_time = time.time()
            elapsed_time = end_time - start_time  # Seconds
            # Log elapsed time in seconds with three decimal places
            logger.debug(f"{func.__name__}() executed in {elapsed_time:.3f} seconds")
    return wrapper


def parse_query(keyword):
    """Decorator to parse the query, check for the keyword, and log if needed."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, query_str: str, params=None, *args, **kwargs):
            # Check if the query contains the specified keyword
            if keyword not in query_str.upper():
                raise ValueError(f'Input query does not include "{keyword}"')

            # Parse the query: append semicolon if not present
            if ';' not in query_str:
                query_str += ';'

            # Format the query if parameters are provided
            if params:
                cur = self.conn_cursor()
                query_str = cur.mogrify(query_str, params)

            # Log the final query if use_query_debug is True
            if getattr(self, 'use_query_debug', False):
                logger.debug(f'mysql_query.{func.__name__}() parsed """{query_str}"""')

            # Call the original function with the parsed query
            return func(self, query_str, *args, **kwargs)

        return wrapper
    return decorator


class MysqlQuery:
    conn = None
    empty_dataframe = pd.DataFrame()
    use_query_debug = True

    def __init__(self, conn_info: str or dict, compress=False):
        """
        Args:
            conn_info : configration dictionary
                (ex) conn_info = {
                                'mysql':
                                    {
                                        'user'  : str(user),
                                        'passwd': str(pw),
                                        'host'  : int(ip),
                                        'db'    : str(db_name),
                                        'charset': str(utf8)
                                    }
                            }
        """
        if isinstance(conn_info, str):
            conn_info = FileUtil.dict_load(conn_info)
        elif not isinstance(conn_info, dict):
            raise TypeError("MysqlQuery support type 'str' and 'dict'")
        self.compress = compress
        required_keys = ['user', 'passwd', 'host', 'db', 'charset']
        if (len(conn_info) > 0) and ('mysql' in conn_info) and all(key in conn_info['mysql'] for key in required_keys):
            self.user = conn_info['mysql']['user']
            self.passwd = conn_info['mysql']['passwd']
            self.host = conn_info['mysql']['host']
            self.db = conn_info['mysql']['db']
            self.charset = conn_info['mysql']['charset']
        else:
            logger.debug(f'[MySQL] config info not exist or any required keys are missing {required_keys}')
        try:
            self.conn = self._connect_db()
        except MySQLError as e:
            logger.error(f"mysql connection failed. {self.__str__()} : {e}")

    def __str__(self):
        return f"Mysql(host={self.conn.host}, db={self.conn.db}, charset={self.conn.charset})"

    def query_debug(self, use_query_debug=False):
        if use_query_debug is True or use_query_debug is False:
            self.use_query_debug = use_query_debug
        logger.debug(f"use_query_debug = {self.use_query_debug}")

    def conn_info(self):
        """
        Args:
        Returns:
            tuple : connection information(host_info, db_info, charset_info)
        """
        return self.conn.host, self.conn.db, self.conn.charset

    def _connect_db(self):
        try:
            self.conn = pymysql.connect(
                user=self.user,
                passwd=self.passwd,
                host=self.host,
                db=self.db,
                charset=self.charset,
                compress=self.compress,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            logger.info(f"[MySQL] DB Connection established.")
            return self.conn
        except MySQLError as e:
            logger.error(f"[MySQL] DB Connection Exception : {e}")
            raise

    @log_execution_time
    def _execute_query(self, cur, query_str):
        """Wraps cur.execute() and logs execution time."""
        return cur.execute(query_str)

    @log_execution_time
    def _execute_many(self, cur, query_str):
        """Wraps cur.execute() and logs execution time."""
        return cur.executemany(query_str)

    @log_execution_time
    def _fetch_one(self, cur):
        """Wraps cur.fetchone() and logs execution time."""
        return cur.fetchone()

    @log_execution_time
    def _fetch_all(self, cur):
        """Wraps cur.fetchone() and logs execution time."""
        return cur.fetchall()

    @log_execution_time
    def _fetch_many(self, cur, fetch_size):
        """Wraps cur.fetchone() and logs execution time."""
        return cur.fetchmany(size=fetch_size)

    def conn_cursor(self, cursorclass=None):
        try:
            if not self.conn.open:
                self.conn.ping(reconnect=True)
        except MySQLError as e:
            logger.error(f"Error ping mysql: {e}. Reconnecting...")
            self.conn = self._connect_db()

        try:
            if self.conn.open:
                return self.conn.cursor(cursor=cursorclass)
        except pymysql.MySQLError as e:
            logger.error(f"Error get connection cursor: {e}")
        raise ConnectionError('Connection MySql Cursor Error')

    def ping(self):
        """
        Args:

        Returns:
            str : DB Status
        """
        if self.conn.open:
            logger.debug(f'[MySQL] database {self.__str__()} connection success')
        else:
            raise ConnectionError(f'database {self.__str__()} connection fail')

    def databases(self) -> pd.DataFrame:
        """
        Args:
        Returns:
            pd.DataFrame() : database dataframe
        """
        cur = self.conn_cursor()
        cur.execute('SHOW DATABASES;')
        result = cur.fetchall()

        if result:
            return pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
        else:
            logger.debug("[MySQL] can't find database")
            return self.empty_dataframe

    def tables(self) -> pd.DataFrame:
        """
        Returns:
            pd.DataFrame() : table dataframe
        """
        cur = self.conn_cursor()
        cur.execute('SHOW TABLES;')
        result = cur.fetchall()

        if result != ():
            return pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
        else:
            logger.debug("[MySQL] can't find tables")
            return self.empty_dataframe

    # ##################################3###
    #  Table method
    # ######################################
    @parse_query('CREATE')
    def create(self, query_str: str, params=None) -> None:
        """
        Args:
            query_str(str) : MySQL create query string
            params: query parameters like % operator
        """
        try:
            cur = self.conn_cursor()
            cur.execute(query_str)
            self.conn.commit()
        except MySQLError as e:
            logger.debug(f"[MySQL] Create Exception : {e}")

    @parse_query('DROP')
    def drop(self, query_str: str, params=None) -> None:
        """
        Args:
            query_str(str) : MySQL drop query string
            params: query parameters like % operator
        """
        try:
            cur = self.conn_cursor()
            cur.execute(query_str)
            self.conn.commit()
        except MySQLError as e:
            logger.debug(f"[MySQL] Drop Exception : {e}")

    @parse_query('TRUNCATE')
    def truncate(self, query_str: str, params=None) -> None:
        """
        Args:
            query_str(str) : MySQL truncate query string
            params: query parameters like % operator
        """
        try:
            cur = self.conn_cursor()
            cur.execute(query_str)
            self.conn.commit()
        except MySQLError as e:
            logger.debug(f"[MySQL] Truncate Exception : {e}")

    @parse_query('ALTER')
    def alter(self, query_str: str, params=None) -> None:
        """
        Args:
            query_str(str) : MySQL alter query string
            params: query parameters like % operator
        """
        try:
            cur = self.conn_cursor()
            cur.execute(query_str)
            self.conn.commit()
        except MySQLError as e:
            logger.debug(f"[MySQL] Alter Exception : {e}")

    # ##################################3###
    #  Quqery method
    # ######################################
    @parse_query('SELECT')
    def select_one(self, query_str: str, params=None):
        """
        Args:
            query_str(str): MySQL select query string that returns a single row
            params: query string format parameters like % style
        Returns:
            dict: A single dictionary result from the query
        """
        try:
            cur = self.conn_cursor()
            self._execute_query(cur, query_str)
            result = cur.fetchone()
            if result:
                return result
            else:
                logger.debug("[MySQL] No data found")
                return {}
        except MySQLError as e:
            logger.debug(f"[MySQL] SELECT Exception: {e}")
            return {}

    @parse_query('SELECT')
    def select_list(self, query_str: str, params=None) -> list:
        """
        Args:
            query_str(str) : MySQL select query string
            params: query string format parameters like % style
        Returns:
            list() : List of query result
        """
        try:
            cur = self.conn_cursor()
            self._execute_query(cur, query_str)
            result = self._fetch_all(cur)

            if result is None:
                logger.debug("[MySQL] data not exist")
                result_list = None
            elif isinstance(result, list):
                result_list = result
            else:
                result_list = [result]
            return result_list
        except MySQLError as e:
            logger.debug(f"[MySQL] SELECT_LIST Exception : {e}")
            return []

    @parse_query('SELECT')
    def select(self, query_str: str, params=None) -> pd.DataFrame:
        """
        Args:
            query_str(str) : MySQL select query string
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        try:
            cur = self.conn_cursor()
            self._execute_query(cur, query_str)
            result = self._fetch_all(cur)

            if result:
                return pd.DataFrame(result)
            else:
                logger.debug(f"[MySQL] data not exist")
                return self.empty_dataframe
        except MySQLError as e:
            logger.debug(f"[MySQL] SELECT Exception : {e}")
            return self.empty_dataframe

    @parse_query('SELECT')
    @log_execution_time
    def faster_select(self, query_str: str, params=None, fetch_size=1000) -> pd.DataFrame:
        """
        Args:
            query_str(str) : MySQL select query string better than normal select
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        total_size = 0
        results = []
        try:
            cur = self.conn_cursor(pymysql.cursors.SSCursor)
            self._execute_query(cur, query_str)
            while True:
                rows = self._fetch_many(cur, fetch_size)
                if not rows:
                    break
                total_size += len(rows)
                results.extend(rows)
                if self.use_query_debug:
                    logger.debug(f"fetch {len(rows)} rows, total fetched size = {total_size}")

            if len(results) > 0:
                return pd.DataFrame(results, columns=[desc[0] for desc in cur.description])
            else:
                logger.debug(f"[MySQL] data not exist")
                return self.empty_dataframe
        except MySQLError as e:
            logger.debug(f"[MySQL] FASTER_SELECT Exception : {e}")
            self.close()
            return self.empty_dataframe

    @parse_query('INSERT')
    def insert(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL insert query string
            params : query string format parameters like % style, tuple or  list of tuple
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        try:
            cur = self.conn_cursor()
            if isinstance(params, list):
                self._execute_many(cur, query_str)
            else:
                self._execute_query(cur, query_str)
            logger.debug(f"[MySQL] INSERT {cur.rowcount} rows")
            self.conn.commit()
            return cur.rowcount
        except MySQLError as e:
            self.conn.rollback()
            logger.debug(f"[MySQL] INSERT Exception : {e}")
            return 0

    @parse_query('UPDATE')
    def update(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL update query string
            params: query string format parameters like % style
        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        try:
            cur = self.conn_cursor()
            if isinstance(params, list):
                self._execute_many(cur, query_str)
            else:
                self._execute_query(cur, query_str)
            logger.debug(f"[MySQL] UPDATE {cur.rowcount} rows")
            self.conn.commit()
            return cur.rowcount
        except MySQLError as e:
            self.conn.rollback()
            logger.debug(f"[MySQL] UPDATE Exception : {e}")
            return 0

    @parse_query('DELETE')
    def delete(self, query_str: str, params=None) -> int:
        """
        Args:
            query_str(str) : MySQL delete query string

        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        try:
            cur = self.conn_cursor()
            if isinstance(params, list):
                self._execute_many(cur, query_str)
            else:
                self._execute_query(cur, query_str)
            logger.debug(f"[MySQL] DELETE {cur.rowcount} rows")
            self.conn.commit()
            return cur.rowcount
        except MySQLError as e:
            self.conn.rollback()
            logger.debug(f"[MySQL] DELETE Exception : {e}")
            return 0

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.debug(f"[MySQL] DB Connection closed.")
