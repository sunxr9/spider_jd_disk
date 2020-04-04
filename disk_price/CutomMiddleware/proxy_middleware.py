# -*- coding: utf-8 -*-
import logging
import random
from urllib.request import _parse_proxy
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


def _parse(proxy_url):

    proxy_type, user, password, hostprot = _parse_proxy(proxy_url)
    return '%s://%s'%(proxy_type, hostprot)


class ProxyMiddleware(object):

    def __init__(self, settings):
        self.proxies = settings.getlist('PROXIES')
        self.max_failed = settings.getint('PROXY_MAX_FAILED', 1)
        self.stats = {}.fromkeys(map(_parse, self.proxies), 0)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured

        if not crawler.settings.getlist('PROXIES'):
            raise NotConfigured

        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)

        print('current use proxy IP --------------', request.meta['proxy'])
        return None

    def process_response(self, request, response, spider):
        cur_proxy = request.meta['proxy']
        print(cur_proxy)
        if response.status >= 400:
            self.stats[cur_proxy] += 1

        if self.stats[cur_proxy] >= self.max_failed:
            for proxy in self.proxies:
                *_, hostport = _parse_proxy(proxy)
                if cur_proxy.endswith(hostport):
                    self.proxies.remove(proxy)
                    logger.info('proxy {ip} remove from proxy list.'.format(ip=cur_proxy))
                    break

        return response
