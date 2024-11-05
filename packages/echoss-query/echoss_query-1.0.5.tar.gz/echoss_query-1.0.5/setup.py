from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = "echoss_query"

setup(
    name='echoss_query',
    version='1.0.5',
    url='',
    install_requires=[
        'pandas>=1.5.3',
        'pymongo>=4.3.3',
        'PyMySQL>=1.0.2',
        'PyYAML>=6.0',
        'opensearch-py>=2.2.0',
        'echoss-fileformat>=1.1.2',
    ],
    license='',
    author='incheolshin',
    author_email='incheolshin@12cm.co.kr',
    description='echoss AI Bigdata Solution - Query Package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    python_requires= '>3.7',
)
