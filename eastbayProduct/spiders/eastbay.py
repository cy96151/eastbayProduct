# -*- coding: utf-8 -*-
import scrapy


class EastbaySpider(scrapy.Spider):
    name = 'eastbay'
    allowed_domains = ['eastbay.com']
    start_urls = ['https://www.eastbay.com/_-_/keyword-bb411w?cm_PAGE=0&Nao=0']

    def parse(self, response):
        # 获取商品信息列表
        productList = response.xpath('//div[@id="endeca_search_results"]/ul/li[not(@class="clearRow")]')
        for each_product in productList:
            item = Test111Item()
            item['title'] = each_product.xpath('./a/span[@class="product_title"]/text()').extract_first()
            item['price'] = each_product.xpath('./a/span/span[@class="price"]/text()').extract_first()
            item['sku'] = each_product.xpath('./@data-sku').extract_first()
            # 获取商品明细地址
            dateilUrl = each_product.xpath('./a/@href').extract_first()
            # 通过detail_parse获取明细页面信息
            yield scrapy.Request(url = dateilUrl, meta={'meta_1':item},callback=self.detail_parse)
        # 若列表页存在下一页，则继续读取下一页
        nextUrl = response.xpath('//a[@class="next"]/@href').extract_first()
        if nextUrl is not None:
            # 使用response.urljoin将相对路径转换为绝对路径
            yield scrapy.Request(url = response.urljoin(nextUrl),callback=self.parse)
    def detail_parse(self,response):
        item = response.meta['meta_1']
        item['color'] = response.xpath('//span[@class="attType_color"]/text()').extract_first()
        detailStr = response.xpath('//div[@id="pdp_description"]').extract_first()
        item['details'] = detailStr[detailStr.find('>')+1:detailStr.find('</div>')]
        item['size'] = []
        item['img_urls'] = []
        yield item
