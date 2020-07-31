import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page_content(request_url):
    # 得到页面的内容
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser')
    return soup

def get_info(soup):
    #获取所需的网页内容
    search_result = soup.find_all('div', class_="search-result-list-item")
    # print(search_result)
    #建立Dataframe数据表格,建立列名称
    df = pd.DataFrame(columns=['名称', '最低价格', '最高价格','产品图片链接'])
    #遍历search_result列表,提取所需信息
    for result in search_result:
        result_list = result.find_all('p')
        carname = result_list[0].string             #提取汽车名称
        pricerange = result_list[1].string          #提取价格区间
        pricecut = pricerange.split('-')            #依靠-字符分隔价格区间
        imgcontent = result.find_all('img')    #提取图片地址
        # 检查结果用，可忽略
        # print(pricerange)
        # print(pricecut)
        # print(imgcontent)
        #判断并赋值，考虑所有出现的结果
        if pricerange == "暂无":
            lowest_price, highest_price = 'N/A', 'N/A'
        else:
            lowest_price, highest_price = pricecut[0]+'万', pricecut[1]
        #补全图片地址
        imgaddress = 'http:' + imgcontent[0].get('src')

        #创建临时空间存储数据
        temp = {}
        #将内容填入temp空间
        temp['名称'],temp['最低价格'], temp['最高价格'], temp['产品图片链接'] = carname, lowest_price, highest_price, imgaddress
        #将数据加入到Dataframe表格内
        df = df.append(temp, ignore_index=True)

    return df

request_url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
soup = get_page_content(request_url)
df = get_info(soup)
df.to_csv('VWcar_info.csv', index=False, encoding='gbk')
