# -*- coding: utf-8 -*-

import time
import scrapy
from scrapy import Request
NEW_PAGE_URL = 'https://search.jd.com/Search?keyword=机械硬盘&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={page}&s={s}&click=0'
SCROLL_PAGE_URL = 'https://search.jd.com/s_new.php?keyword=机械硬盘&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={page}&s={s}&scrolling=y&log_id={log_id}&tpl=1_M&show_items={show_items}'
PRODUCT_DESC_URL = 'https://item.jd.com/{id}.html#crumb-wrap'


class JdDiskSpider(scrapy.Spider):
    name = 'jd_disk'

    def __init__(self):
        '''
        添加 chrome 操作对象
        '''
        super(JdDiskSpider,self).__init__()
        # self.driver = webdriver.Chrome()
        self.allowed_domains = ['https://www.jd.com/']
        self.start_urls = ['https://www.jd.com/']
        self.complete_product_id = set()

    def parse(self, response):
        for n in range(1, 2):
            request_status = n % 2
            if request_status:
                s = (n-1)*30-n*2
                if s < 0:
                    s = 1

                new_page_url = NEW_PAGE_URL.format(page=n, s=s)
                request = Request(new_page_url, callback=self.page_parse, dont_filter=True)
                request.meta['cur_page'] = n
                request.meta["dont_merge_cookies"] = True
                yield request

    def page_parse(self, response):
        cur_page = response.meta['cur_page']
        product_id_list = []

        product_element = response.xpath('//div[@id="J_goodsList"]/ul/li')
        for element in product_element:
            product_id_list.append(element.xpath('@data-sku').get())

        log_id = round(time.time(), 5)
        show_items = ','.join(product_id_list)
        s = cur_page*30-cur_page*2-cur_page
        scroll_page_url = SCROLL_PAGE_URL.format(page=cur_page+1, s=s, log_id=log_id, show_items=show_items)
        print('111111111111111111111111111')

        request = scrapy.Request(scroll_page_url, callback=self.scroll_page_parse, dont_filter=True)
        request.meta['product_id_list'] =  product_id_list
        yield request

    def scroll_page_parse(self, response):
        product_id_list = response.meta['product_id_list']
        product_element = response.xpath('//li[@class="gl-item"]')
        print('13222222222222222222222222222')

        for element in product_element:
            product_id_list.append(element.xpath('@data-sku').get())

        for product_id in product_id_list:
            self.complete_product_id.add(product_id)
            product_desc_url = PRODUCT_DESC_URL.format(id=product_id)

            request = Request(product_desc_url, callback=self.desc_page_parse, dont_filter=True)
            request.meta['product_id'] = product_id
            yield request

    def desc_page_parse(self, response):
        pass
        product_id = response.meta['product_id']
        shop_link = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a')
        shop_address = shop_link.xpath('@href').get()
        if shop_address.startswith('//'):
            shop_address = 'https:' + shop_address

        shop_name = shop_link.xpath('text()').get()

        # price_xpath = '//span[contains(@class, "price") and contains(@class, "J-p-{product_id}")]/text()'
        price_xpath = '//span[@class="p-price"]/span[contains(@class, "J-p-{product_id}")]/text()'
        price = response.xpath(price_xpath.format(product_id=product_id)).get()

        product_introduction_element = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul')
        product_introduction = product_introduction_element[-1].xpath('li/text()').getall()

        product_intro_dict = self.items_product(product_introduction)
        print(product_intro_dict, product_id, shop_address, shop_name, price)

    def items_product(self, product_intro):
        product_intro_dict = {}

        for items in product_intro:
            item = items.split('：')
            product_intro_dict[item[0]] = item[1]

        return product_intro_dict











