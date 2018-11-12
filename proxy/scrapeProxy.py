import requests
from lxml import html
import log.log as log
import random
import traceback
import re

from concurrent.futures import ThreadPoolExecutor as TPE
from concurrent.futures import as_completed

proxyLogger = log.get_logger(__name__)

httpsCount = 0
httpCount = 0

def proxyScraper():
    """
    Parses htmlobject using xpath search pulling IP, port, Country, type, HTTPS and Time discovered
    information for a single request
    :param htmlobject:
    :return: proxyDict
    """
    uri = 'https://free-proxy-list.net/'

    pageContent = requests.get(url=uri, headers=rand_useragent(), timeout=10)

    tree = html.fromstring(pageContent.content)

    proxyIP = [item for item in tree.xpath('//table/tbody/tr/td[1]/text()')]
    proxyPort = [item for item in tree.xpath('//table/tbody/tr/td[2]/text()')]
    proxyCountry = [item for item in tree.xpath('//table/tbody/tr/td[4]/text()')]
    proxyType = [item for item in tree.xpath('//table/tbody/tr/td[5]/text()')]
    proxyHTTPS = [item for item in tree.xpath('//table/tbody/tr/td[7]/text()')]
    proxyDiscovered = [item for item in tree.xpath('//table/tbody/tr/td[8]/text()')]

    proxyDict = {key: value for key, *value in
                 zip(proxyCountry, proxyIP, proxyPort, proxyType, proxyHTTPS, proxyDiscovered)}

    httpsProxy = ['https', ]
    httpProxy = ['http']

    for key, value in proxyDict.items():
        if value[3] == 'yes':
            httpsProxy.append(f'https://{value[0]}:{value[1]}')
        else:
            httpProxy.append(f'http://{value[0]}:{value[1]}')

    proxyLogger.info(
        f'From {len(httpsProxy) + len(httpProxy)} available proxies, {len(httpsProxy)} are HTTPS capable and {len(httpProxy)} for HTTP')

    return httpsProxy, httpProxy


def rand_useragent():
    useragent = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    ]

    html_headers = {
        'User-Agent': f'{random.choice(useragent)}'
    }
    return html_headers


def proxyCheck(proxyURI):
    test_site = "http://api.ipify.org/?format=json"

    httpsProxy = []
    httpProxy = []

    pattern = r'(https)://'

    if bool(re.match(pattern, proxyURI)) == True:
        param_proxy = {
            'https': proxyURI
        }

        # Test HTTPS proxy if active
        try:
            r = requests.get(test_site, headers=rand_useragent(), proxies=param_proxy, timeout=(20, 15))
            status = r.status_code
            if status is 200:
                httpsProxy.append(proxyURI)
                proxyLogger.info(f'Proxy {proxyURI} is Online. Appending to active proxy list.')
                counter('https')
        except Exception as error:
            proxyLogger.error(f'Error on proxy {proxyURI}. Exception: {error} Stack Trace: {traceback.print_exc()}')
            pass
    else:
        param_proxy = {
            'http': proxyURI
        }

        # Test HTTP proxy if active
        try:
            r = requests.get(test_site, headers=rand_useragent(), proxies=param_proxy, timeout=(20, 15))
            status = r.status_code
            if status is 200:
                httpProxy.append(proxyURI)
                proxyLogger.info(f'Proxy {proxyURI} is Online. Appending to active proxy list.')
                counter('http')
        except Exception as error:
            proxyLogger.error(f'Error on proxy {proxyURI}. Exception: {error} Stack Trace: {traceback.print_exc()}')
            pass

    return httpsProxy, httpProxy


def counter(protocol_type):
    global httpsCount, httpCount

    if protocol_type == 'https':
        httpsCount += 1
    elif protocol_type == 'http':
        httpCount += 1


def multiprocessor(proxyList):
    with TPE(max_workers=50) as executor:
        futures = [executor.submit(proxyCheck, uri) for uri in proxyList]
        for future in as_completed(futures):
            proxyLogger.debug(f'Thread Closed for ProxyCheck {future.result()}')

    proxyLogger.info(
        f'{httpsCount + httpCount} active proxies, {httpsCount} are HTTPS capable and {httpCount} for HTTP')


if __name__ == '__main__':
    httpsProxyList, httpProxyList = proxyScraper()

    multiprocessor(httpsProxyList[1:])
    multiprocessor(httpProxyList[1:])
