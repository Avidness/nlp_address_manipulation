from opensearchpy import OpenSearch
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

os_host = config.get('opensearch', 'host')
os_port = config.get('opensearch', 'port')
os_user = config.get('opensearch', 'user')
os_pw = config.get('opensearch', 'pw')

def getOSClient():
    return OpenSearch(
        hosts = [{'host': os_host, 'port': os_port}],
        http_compress = True,
        http_auth = (os_user, os_pw),
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )