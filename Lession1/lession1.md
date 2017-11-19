## 编写第一个爬虫
### wallpaper.py  爬取壁纸网站
一 要考虑的问题点 以此来保证代码的健壮性  

1. 异常捕获，让代码继续执行  
2. 重试下载，如遇到服务器的错误时，要去判断，然后从新下载  
3. 设置用户代理  

二 使用BeautifulSoup4 提取所需的内容  
1 使用pip beautiful 的安装   
> pip install beautifulsoup4  

2 
