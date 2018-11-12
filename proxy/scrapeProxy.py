import requests
from lxml import html
import log.log as log
import random

proxyLogger = log.get_logger(__name__)


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

    httpsProxyList = []
    httpProxyList = []

    for key, value in proxyDict.items():
        if value[3] == 'yes':
            httpsProxyList.append(f'https://{value[0]}:{value[1]}')
        else:
            httpProxyList.append(f'http://{value[0]}:{value[1]}')

    proxyLogger.info(
        f'From {len(httpsProxyList) + len(httpProxyList)} available proxies, {len(httpsProxyList)} are HTTPS capable and {len(httpProxyList)} for HTTP')

    return httpsProxyList, httpProxyList


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

if __name__ == '__main__':
    proxyScraper()
