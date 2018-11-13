import requests
from proxy import scrapeProxy
import log.log as log

linkSpider_logger = log.get_logger(__name__)


class HTMLParser(HTMLParser):

    def tagCategorizer(self, tag, attrs):
        '''
        Detects, categorizes and retrieves links, static files
        '''
        pass

    def run(self, uri):

        self.uri = uri
        self.domain = get_domain()
        self.urls = []
        self.httpsProxyList = []
        self.httpProxyList = []
        self.poppedProxy = {}
        self.spent_proxy = []

    def initProxies(self):
        '''
        Calls scrapeProxy.main() to generate Active proxy lists
        :return:
        '''
        self.httpsProxyList, self.httpProxyList = scrapeProxy.main()
        linkSpider_logger.info(f'Active Proxies now available.')

    def proxyTracking(self):
        '''
        fixme: This function depends on proxyUse(). This function expects 2 strings, https and http proxies
        :return:
        '''
        self.spent_proxy.append()

    def proxyUse(self):
        '''

        :return: httpsPoppedProxy, httpPoppedProxy
        '''

        try:
            #   get the first proxy and assign to paramProxy dictionary
            self.paramProxy = {
                'https': self.httpsProxyList.pop(0),
                'http': self.httpProxyList.pop(0)
            }

        except IndexError as noProxyAvailable:
            #   replenish proxy lists by calling initProxies()
            linkSpider_logger.error(f'Error: {noProxyAvailable}. Replenishing Proxies...')
            self.initProxies()
