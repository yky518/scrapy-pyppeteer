import scrapy
from ..items import WeibospiderItem

class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/question/349551368']


    def parse(self, response):
        print('图片列表')
        img_list = response.css('figure img.origin_image.lazy::attr(data-original)').getall()
        # img_list = response.css('.weibo-media-wraps.weibo-media img::attr(src)').getall()
        print(img_list)
        print(len(img_list))
        for img in img_list:
            item = WeibospiderItem()
            index = img.index('?')
            item['url'] = [img[0:index]]
            print(img[0:index])
            yield item