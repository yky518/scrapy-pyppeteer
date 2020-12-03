# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
import asyncio
import pyppeteer


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class WeibospiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeibospiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future((self.getbrowser()))
        loop.run_until_complete(task)

    async def getbrowser(self):
        self.browser = await pyppeteer.launch(headless=False)
        self.page = await self.browser.newPage()
        await self.page.setViewport(viewport={'width': 1366, 'height': 768})
        await self.page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        await self.page.setJavaScriptEnabled(enabled=True)
        # await self.page.evaluate(
        #     '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
        # await self.page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        # await self.page.evaluate(
        #     '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
        # await self.page.evaluate(
        #     '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

        return self.page

    async def usePypuppeteer(self, request):
        print(request.url)
        # self.page = await self.getbrowser()
        await self.page.goto(request.url)
        await asyncio.sleep(3)
        await self.page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        print('等待——————————————————————————————————————————————————————')

        await asyncio.sleep(5)
        for i in range(5):
            #鼠标滚动到底
            await self.page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            print('等待——————————————————————————————————————————————————————')

            await asyncio.sleep(5)
        content = await self.page.content()
        return content

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        if 'zhimg.com' in request.url:
            return None
        else:
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(self.usePypuppeteer(request))
            loop.run_until_complete(task)
            # return task.result()
            return HtmlResponse(url=request.url, body=task.result(), encoding="utf-8", request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
