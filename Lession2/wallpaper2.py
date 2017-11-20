#coding=utf-8;

import urllib.request

from  bs4 import  BeautifulSoup

import os
"""
    爬取一个网站有很多种方式 采取什么方式取决于结构
"""

"""
    Lession2 进入套图进行下载
    爬取壁纸
    http://desk.zol.com.cn/jieri/2880x1800_p4/
"""
baseUrl = 'http://desk.zol.com.cn/jieri/2880x1800_p4/';
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'
target_path = '/Users/alexander/Desktop/About Python/抓取资料/downImg/';


# 1 下载网页 返回HTML
# 代理的设置 下载重试
def download_url(url,user_agent,num_retries):
    print("download:" + url);
    req1 = urllib.request.Request(url);
    req1.add_header('User-Agent',user_agent);

    # 异常捕获
    try:
        res1 = urllib.request.urlopen(req1);
        html1 = res1.read().decode('gbk');
       # print(html1);
    except urllib.request.URLError as e:
        print("error haappend");
        html1 = None;
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                # 进行重新下载
                return download_url(url,num_retries - 1);

    return  html1;

# 2 使用beautiful soup 处理网页数据，返回我们想要的信息
"""
    在这个方法中获取套图连接 返回出去
"""
def process_html(html):
    bsObj = BeautifulSoup(html);
    """
        class='photo-list-padding
        findAll 参数 丢一个参数是 你要找的 标签
        第二个参数 是属性字典
        第三个参数 是布尔变量 是否递归查找子标签以及子标签的标签
        第四个参数是 根据标签文本查找内容
        第五个参数限制查找几条数据
        第六个参数 关键词参数
        findAll(tag,attrs,recursive,text,limit,keywords)

    """
    # 找到图片的盒子
    item_list = bsObj.findAll('li',{'class':{'photo-list-padding'}});
    # img 连接的地址
    imgUrl_list = [];

    base_img_url = "http://desk.zol.com.cn";

    # for 循环找到所有的img_url
    for item in item_list:
         # 取到a标签的herf
         pic_href = item.find('a')['href'];

         # 拼接上baseUrl
         img_group_url = base_img_url + pic_href;
         imgUrl_list.append(img_group_url);

         # 紧接着处理数据
         get_one_group_img(img_group_url);




#  3 要单独写一个函数去处理套图 还是要发请求
"""
    获取套图的入口地址，返回HTML
    1> 筛选出一套图有多少张
    2> 获取下一页的连接
"""
def get_one_group_img(url):
    req3 = urllib.request.Request(url);
    req3.add_header('User-Agent',user_agent);
    res3 = urllib.request.urlopen(req3);
    # 还是要筛选数据
    bsObj3 = BeautifulSoup(res3.read().decode('gbk'));
    # 筛选出数量
    parrent_obj = bsObj3.find('div',{'class':{'slideTxt'}}).get_text();
    # 3.1 获得数量
    temp1 = parrent_obj.split('/')[-1];
    group_img_count = temp1[0:-1];
    # 3.2 获取下一张的连接  id = pageNext
    next_page_url = bsObj3.find(id='pageNext')['href'];
    print(next_page_url);




# 写入本地操作
def write_img(path,img_list):

    # 切换到指定目录

    # new_path = target_path + '/' + 'downImg';
    # if os.path.exists(new_path):
    #     pass
    # else:
    #     os.makedirs(new_path);


    # 切换到当前目录
    os.chdir(target_path);

    # 写入图片
    for item in img_list:
        req2 = urllib.request.Request(item);
        req2.add_header('User-Agent',user_agent);
        res2 = urllib.request.urlopen(req2);
        res2_img = res2.read();

        pic_name = item.split('/')[-1];
        with open(pic_name,'wb') as f:
            f.write(res2_img);

    print("download complete");


if __name__ == '__main__':
    html = download_url(baseUrl,user_agent,4);
    process_html(html);

    # 创建个目录


