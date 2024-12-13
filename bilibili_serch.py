from selenium import webdriver
from selenium.webdriver.common.by import By 
import time
import requests
from bs4 import BeautifulSoup
import ast
import re

url_oringin='https://search.bilibili.com/all?keyword={}&from_source=webtop_search&spm_id_from=333.1007&search_source=3&order=pubdate'
#======================用戶輸入====================
hot=50000

howmany=10

key_word_list=['俄烏戰爭']

key_word=key_word_list[0]

limit=0
#======================用戶輸入====================

url=url_oringin.format(key_word)

driver=webdriver.Chrome()

driver.get(url)

driver.implicitly_wait(10)

read_file={}
with open('bilibili_serch.txt','r',encoding='utf=8') as f:
    read_file=ast.literal_eval(f.read())
if key_word not in read_file:
    read_file[key_word]=''
count=0

page=1
#time.sleep(5)
end_flag=False
first_search= ''

while count<=howmany:
    elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'video-list-item col_3 col_xs_1_5 col_md_2 col_xl_1_7 mb_x40')]")
    for element in elements[:24]:
        # 在当前 element 下查找包含特定属性的 span 元素
        span = element.find_element(By.CSS_SELECTOR, 'span[data-v-5686f5fc]')
        if '万' in span.text:
            views=float(span.text.replace('万', ''))*10000
        else:
            try:
                views=int(span.text)
            except:
                views=0
                print('views error')
        if views>=hot:
            video_name=element.find_element(By.TAG_NAME,'img').get_attribute('alt')
            if count==0:
                first_search=video_name
            if limit and video_name==read_file[key_word]:
                end_flag=True
                break
            count+=1
            print(video_name)
            print('播放量',span.text)
            print(element.find_element(By.TAG_NAME,'a').get_attribute('href'))
            print('=======================================')
    page+=1
    if page==43 or end_flag:
        break
    url=url_oringin.format(key_word)+f'&page={page}&o={(page-1)*24}'
    driver.get(url)

if first_search!='':
    read_file[key_word]=first_search
    with open('bilibili_serch.txt','w',encoding='utf-8') as f:
        f.write(str(read_file))
driver.close()