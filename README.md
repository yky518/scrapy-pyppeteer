# scrapy-pyppeteer

## 安装
先安装annaconda
conda install scrapy
conda isntall pyppeteer

## 配置
图片下载器默认就行，中间间用pyppeteer重写，注意异步操作用asyncio包裹
pyppeteer调试时可以开启界面，pyppeteer.launch(headless=False)
在浏览器实现模拟下拉等操作
```
page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
```
发觉开启界面之后完全可以手动了……
