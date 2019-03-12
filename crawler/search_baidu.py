from bs4 import BeautifulSoup as BS4

soup_root = BS4(open("search_baidu.html",encoding='utf-8'),"lxml")

url = 'http:///xueshu.baidu.com'

result = soup_root.find(id="bdxs_result_lists").find_all(class_="result")
for item in result:
    print(item.div.h3.text.strip())   #标题
    # print(item.div.h3.a['href'])    #url
