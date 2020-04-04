# -*- coding: utf-8 -*-

# import faker
import random
from scrapy.exceptions import NotConfigured


class UserAgentMiddleware(object):

    def __init__(self, settings):
        self.user_agent = settings.getlist('USER_AGENT')

    @classmethod
    def from_crawler(cls, crawler):

        return cls(crawler.settings)

    def process_request(self, request, spider):

        request.headers['User-Agent'] = random.choice(self.user_agent)
        return None