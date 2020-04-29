# -*- coding: utf-8 -*-

import time
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest
from disk_price.items import DiskPriceItem

NEW_PAGE_URL = 'https://search.jd.com/Search?keyword=机械硬盘&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={page}&s={s}&click=0'
SCROLL_PAGE_URL = 'https://search.jd.com/s_new.php?keyword=机械硬盘&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={page}&s={s}&scrolling=y&log_id={log_id}&tpl=1_M&show_items={show_items}'
PRODUCT_DESC_URL = 'https://item.jd.com/{id}.html#crumb-wrap'
SPLASH_ARGS = {'timeout': 3600, 'wait': 1.5}

price_xpath = '//span[@class="p-price"]/span[contains(@class, "J-p-{product_id}")]/text()'


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

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], self.parse)

    def parse(self, response):
        for n in range(1, 2):
            request_status = n % 2
            if request_status:
                s = (n-1)*30-n*2
                if s < 0:
                    s = 1

                new_page_url = NEW_PAGE_URL.format(page=n, s=s)
                request = SplashRequest(new_page_url,
                                        callback=self.page_parse,
                                        dont_filter=True,
                                        args=SPLASH_ARGS,
                                        endpoint='render.html')
                request.meta['cur_page'] = n
                request.meta["dont_merge_cookies"] = True
                yield request

    def page_parse(self, response):
        cur_page = response.meta['cur_page']
        product_id_list = []
        product_id_list.extend(response.xpath('//div[@id="J_goodsList"]/ul/li/@data-sku').getall())

        log_id = round(time.time(), 5)
        show_items = ','.join(product_id_list)
        s = cur_page*30-cur_page*2-cur_page
        scroll_page_url = SCROLL_PAGE_URL.format(page=cur_page+1, s=s, log_id=log_id, show_items=show_items)
        print('111111111111111111111111111')

        request = SplashRequest(scroll_page_url,
                                callback=self.scroll_page_parse,
                                dont_filter=True,
                                args=SPLASH_ARGS,
                                endpoint='render.html')
        request.meta['product_id_list'] = product_id_list
        yield request

    def scroll_page_parse(self, response):
        response.body.decode('utf-8')
        product_id_list = response.meta['product_id_list']
        product_id_list.extend(response.xpath('//li[@class="gl-item"]/@data-sku').getall())
        print('13222222222222222222222222222')

        n = 0
        for product_id in product_id_list:
            if n > 3:
                break
            n += 1
            if product_id in self.complete_product_id:
                continue
            product_desc_url = PRODUCT_DESC_URL.format(id=product_id)

            request = SplashRequest(product_desc_url,
                                    callback=self.desc_page_parse,
                                    dont_filter=True,
                                    args=SPLASH_ARGS,
                                    endpoint='render.html')
            request.meta['product_id'] = product_id
            request.meta['depth'] = None
            yield request

    def desc_page_parse(self, response):
        depth = response.meta['depth']
        if depth == 2:
            self.disk_content(response)
        elif depth == 1:
            choose_attr_id = response.xpath('//div[@id="choose-attr-2"]/div[@class="dd"]/div/@data-sku')
            choose_attr_title = response.xpath('//div[@id="choose-attr-2"]/div[@class="dd"]/div/@title')
            choose_id = filter(self.clear_id, zip(choose_attr_id, choose_attr_title))
            for i in choose_id:
                product_desc_url = PRODUCT_DESC_URL.format(id=i)
                request = SplashRequest(product_desc_url,
                                        callback=self.desc_page_parse,
                                        dont_filter=True,
                                        args=SPLASH_ARGS,
                                        endpoint='render.html')
                request.meta['product_id'] = i
                request.meta['depth'] = 2
                yield request
        else:
            # 判断是否存在产品选项
            choose = response.xpath("//div[@id='choose-attr-1' or @id='choose-attr-2']")

            if len(choose) > 1:
                choose_attr_id = choose[0].xpath('div[@class="dd"]/div/@data-sku').get()
                # 获取商品选择属性，并跳转
                for i in choose_attr_id:
                    product_desc_url = PRODUCT_DESC_URL.format(id=i)
                    request = SplashRequest(product_desc_url,
                                            callback=self.desc_page_parse,
                                            dont_filter=True,
                                            args=SPLASH_ARGS,
                                            endpoint='render.html')
                    request.meta['product_id'] = i
                    request.meta['depth'] = 1
                    yield request
            elif len(choose) == 1:
                choose_attr_id = choose[0].xpath('div[@class="dd"]/div/@data-sku').get()
                for i in choose_attr_id:
                    product_desc_url = PRODUCT_DESC_URL.format(id=i)
                    request = SplashRequest(product_desc_url,
                                            callback=self.desc_page_parse,
                                            dont_filter=True,
                                            args=SPLASH_ARGS,
                                            endpoint='render.html')
                    request.meta['product_id'] = i
                    request.meta['depth'] = 2
                    yield request
            else:
                return self.disk_content(response)

    def disk_content(self, response):
        # response.body.decode('GBK').encode('utf-8')
        product_id = response.meta['product_id']
        if product_id in self.complete_product_id:
            return
        self.complete_product_id.add(product_id)

        shop_link = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a')
        shop_address = shop_link.xpath('@href').get()
        if shop_address and shop_address.startswith('//'):
            shop_address = 'https:' + shop_address

        disk_item = DiskPriceItem()
        disk_item['shop_address'] = shop_address
        disk_item['shop_name'] = shop_link.xpath('text()').get()

        disk_item['price'] = response.xpath(price_xpath.format(product_id=product_id)).get()

        product_introduction_element = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul')
        product_introduction = product_introduction_element[-1].xpath('li/text()').getall()

        product_intro_dict = self.split_product_intro(product_introduction)

        disk_item['product_id'] = product_id
        disk_item['product_name'] = product_intro_dict['商品名称']
        try:

            disk_item['interface'] = product_intro_dict['接口']
        except KeyError as e:
            disk_item['interface'] = ''

        try:
            disk_item['rotate_speed'] = product_intro_dict['转速']
        except KeyError as e:
            disk_item['rotate_speed'] = ''

        disk_item['capacity'] = product_intro_dict['容量']
        try:

            disk_item['cache'] = product_intro_dict['缓存']
        except KeyError:
            disk_item['cache'] = ''

        print(product_intro_dict)
        yield disk_item

    def split_product_intro(self, product_intro):
        product_intro_dict = {}

        for items in product_intro:
            item = items.split('：')
            product_intro_dict[item[0]] = item[1]

        return product_intro_dict

    def clear_id(self, choose_attr):
        product_id = []

        for i, t in choose_attr:
            if '无此商品' not in t:
                product_id.append(i)

        return product_id








