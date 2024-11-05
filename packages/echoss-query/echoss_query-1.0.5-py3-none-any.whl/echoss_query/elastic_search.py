import pandas as pd
from opensearchpy import OpenSearch
from typing import Any, List, Tuple, Union

from echoss_fileformat import FileUtil, get_logger, set_logger_level

logger = get_logger("echoss_query")


class ElasticSearch:
    conn = None
    query_match_all = {"query": {"match_all": {}}}
    empty_dataframe = pd.DataFrame()
    query_cache = False
    default_size = 1000

    def __init__(self, conn_info: str or dict):
        """
        Args:
            conn_info : configration dictionary (index is option)
            ex) conn_info = {
                                'elastic':
                                    {
                                        'user'  : str(user),
                                        'passwd': str(passwd),
                                        'host'  : str(host),
                                        'port' : int(port),
                                        'index' : str(index_name)
                                    }
                            }

        """
        if isinstance(conn_info, str):
            conn_info = FileUtil.dict_load(conn_info)
        elif not isinstance(conn_info, dict):
            raise TypeError("ElasticSearch support type 'str' and 'dict'")
        required_keys = ['user', 'passwd', 'host', 'port']
        if (len(conn_info) > 0) and ('elastic' in conn_info) and all(k in conn_info['elastic'] for k in required_keys):
            self.user = conn_info['elastic']['user']
            self.passwd = conn_info['elastic']['passwd']
            self.host = conn_info['elastic']['host']
            self.port = conn_info['elastic']['port']
            if 'index' in conn_info['elastic']:
                self.index_name = conn_info['elastic']['index']
            else:
                self.index_name = None

            self.hosts = [{
                'host': self.host,
                'port': self.port
            }]

            self.auth = (self.user, self.passwd)
            # re-use connection
            self.conn = self._connect_es()

            # extra config
            if 'default_size' in conn_info['elastic']:
                default_size = conn_info['elastic']['default_size']
        else:
            logger.debug(f"[Elastic] config info not exist")

    def __str__(self):
        return f"ElasticSearch(hosts={self.hosts}, index={self.index_name})"

    def _connect_es(self):
        """
        ElasticSearch Cloud에 접속하는 함수
        """
        try:
            es_conn = OpenSearch(
                hosts=self.hosts,
                http_compress=True,
                http_auth=self.auth,
                use_ssl=True,
                verify_certs=True,
                ssl_assert_hostname=False,
                ssl_show_warn=False
            )
            if es_conn is None or es_conn.ping() is False:
                raise ValueError(f"open elasticsearch is failed or health ping failed.")
            return es_conn
        except Exception as e:
            raise ValueError("Connection failed by config. Please check config data")

    def ping(self) -> bool:
        """
        Elastic Search에 Ping
        """
        if self.conn:
            return self.conn.ping()
        else:
            return False

    def info(self) -> dict:
        """
        Elastic Search Information
        """
        return self.conn.info()

    def exists(self, id: str or int, index=None) -> bool:
        """
        Args:
            index(str) : 확인 대상 index \n
            id(str) : 확인 대상 id \n
        Returns:
            boolean
        """
        if index is None:
            index = self.index_name
        return self.conn.exists(index, id)

    def search(self, body: dict = None, index=None):
        """
        Args:
            index(str) : 대상 index
            body(dict) : search body
        Returns:
            result(list) : search result
        """
        if index is None:
            index = self.index_name
        if body is None:
            body = self.query_match_all

        response = self.conn.search(
            index=index,
            body=body
        )
        return response

    def to_dataframe(self, result_list):
        if isinstance(result_list, dict):
            if 'hits' in result_list and 'hits' in result_list['hits']:
                result_list = result_list['hits']['hits']
        if result_list is not None and isinstance(result_list, list) and len(result_list)>0:
            if '_source' in result_list[0]:
                documents = [doc['_source'] for doc in result_list]
                df = pd.DataFrame(documents)
                return df
        return self.empty_dataframe

    def _fetch_all_hits(self, index: str, body: dict) -> List[dict]:
        """
        Scroll API를 사용하여 모든 검색 결과를 가져옵니다.

        Args:
            index (str): 대상 인덱스 이름
            body (dict): 검색 쿼리
        Returns:
            all_hits (list): 모든 검색 결과 리스트
        """
        all_hits = []
        scroll_time = '2m'  # Scroll context 유지 시간

        # 'size' 값 확인 및 설정
        size = body.get('size', 1000)
        body = body.copy()  # 원본 body를 변경하지 않도록 복사
        body['size'] = size
        scroll_id = None
        try:
            # 초기 검색 요청
            response = self.conn.search(
                index=index,
                body=body,
                scroll=scroll_time
            )

            scroll_id = response['_scroll_id']
            hits = response['hits']['hits']
            all_hits.extend(hits)

            # 더 이상 결과가 없을 때까지 반복
            while len(hits) > 0:
                response = self.conn.scroll(
                    scroll_id=scroll_id,
                    scroll=scroll_time
                )
                scroll_id = response['_scroll_id']
                hits = response['hits']['hits']
                all_hits.extend(hits)

            # Scroll context 삭제
            self.conn.clear_scroll(scroll_id=scroll_id)

        except Exception as e:
            logger.error(f"Error fetching all hits: {e}")
            # Scroll context 정리 시도
            try:
                if scroll_id is not None:
                    self.conn.clear_scroll(scroll_id=scroll_id)
            except Exception as ce:
                logger.error(f"connection clear_scroll failed : {ce}")
            raise

        return all_hits

    def search_list(self, body: dict = None, index=None, fetch_all: bool = True) -> list:
        """
        Args:
            body(dict) : search body
            index(str) : 대상 index
            fetch_all(bool) : fetch all hits
        Returns:
            result(list) : search result of response['hits']['hits']
        """
        if index is None:
            index = self.index_name
        if body is None:
            body = self.query_match_all
        if fetch_all:
            return self._fetch_all_hits(index, body)
        else:
            response = self.conn.search(
                index=index,
                body=body
            )
            if len(response) > 0 and 'hits' in response and 'hits' in response['hits']:
                return response['hits']['hits']
        return []

    def search_dataframe(self, body: dict = None, index=None, fetch_all: bool = True) -> pd.DataFrame:
        hits_list = self.search_list(body=body, index=index, fetch_all=fetch_all)
        return self.to_dataframe(hits_list)

    def search_field(self, field: str, value: str, index=None, fetch_all=True) -> list:
        """
        해당 index, field, value 값과 비슷한 값들을 검색해주는 함수 \n
        Args:
            index(str) : 대상 index
            field(str) : 검색 대상 field \n
            value(str) : 검색 대상 value \n
        Returns:
            result(list) : 검색 결과 리스트
        """
        if index is None:
            index = self.index_name

        query_body = {
                'query': {
                    'match': {field: value}
                }
            }
        if fetch_all:
            return self._fetch_all_hits(index, query_body)
        else:
            response = self.conn.search(
                index=index,
                body=query_body
            )
            return response['hits']['hits']

    def get(self, id: str or int, index=None) -> dict:
        """
        index에서 id와 일치하는 데이터를 불러오는 함수 \n
        Args:
            id(str) : 가져올 대상 id \n
        Returns:
            result(dict) : 결과 데이터

        """
        if index is None:
            index = self.index_name
        return self.conn.get(index=index, id=id)

    def get_source(self, id: str or int, index=None) -> dict:
        """
        index에서 id와 일치하는 데이터의 소스만 불러오는 함수 \n
        Args:
            id(str) : 가져올 대상 id \n
        Returns:
            result(dict) : 결과 데이터

        """
        if index is None:
            index = self.index_name
        return self.conn.get_source(index, id)

    def create(self, id: str or int, body: dict, index=None):
        """
        index에 해당 id로 새로운 document를 생성하는 함수 \n
        (기존에 있는 index에 데이터를 추가할 때 사용) \n
        Args:
            id(str) : 생성할 id \n
            body(dict) : new data
            index(str) : index name or self.index_name will be used
        Returns:
            result(str) : 생성 결과
        """
        if index is None:
            index = self.index_name
        return self.conn.create(index=index, id=id, body=body)

    def index(self, index: str, body: dict, id: str or int = None) -> str:
        """
        index를 생성하고 해당 id로 새로운 document를 생성하는 함수 \n
        (index를 추가하고 그 내부 document까지 추가하는 방식) \n
        Args:
            index(str) : 생성할 index name \n
            body(dict) : 입력할 json 내용
            id(str) : 생성할 id \n
        Returns:
            result(str) : 생성 결과
        """
        return self.conn.index(index, body, id=id)

    def update(self, id: str or int, body: dict, index=None) -> str:
        """
        기존 데이터를 id를 기준으로 body 값으로 수정하는 함수 \n
        Args:
            id(str) : 수정할 대상 id \n
            body(dict) : data dict to update
            index(str) : 생성할 index name \n
        Returns:
            result(str) : 처리 결과
        """
        if index is None:
            index = self.index_name
        doc_body = {
            'doc' : body
        }
        return self.conn.update(index, id, doc_body)

    def delete(self, id: str or int, index=None) -> str:
        """
        삭제하고 싶은 데이터를 id 기준으로 삭제하는 함수 \n
        Args:
            id(str) : 삭제 대상 id \n
            index(str) : 생성할 index name \n
        Returns:
            result(str) : 처리 결과
        """
        if index is None:
            index = self.index_name
        return self.conn.delete(index, id)

    def delete_index(self, index):
        """
        인덱스를 삭제하는 명령어 신중하게 사용해야한다.\n
        Args:
            index(str) : 삭제할 index
        Returns:
            result(str) : 처리 결과
        """
        return self.conn.indices.delete(index)

    def close(self):
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
        except AttributeError:
            pass

    def __del__(self):
        self.close()

