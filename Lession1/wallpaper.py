#coding=utf-8;

import urllib.request

from  bs4 import  BeautifulSoup

import os
"""
    爬取一个网站有很多种方式 采取什么方式取决于结构
"""

"""
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

# 使用beautiful soup 处理网页数据
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
    # for 循环找到所有的img_url
    for item in item_list:
         pic = item.find('img')['src'];
         imgUrl_list.append(pic);


    write_img(target_path,imgUrl_list);




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


