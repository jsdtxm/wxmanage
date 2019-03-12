from bs4 import BeautifulSoup as BS4

soup_root = BS4(open("item_cnki.html",encoding='utf-8'),"lxml")

soup = soup_root.find("div", class_="wxmain")

title = soup.find("div", class_="wxTitle").h2.text
abstract = soup.find(id='ChDivSummary').text
ztcls = soup.find(id='catalog_ZTCLS').parent.text[4:]

all_a = soup.find_all('a')

# for item in all_a:
#     try:
#         onclick = item['onclick'].strip()
#         if not onclick.find('TurnPageToKnet'):
#             print(onclick[15:-2].replace("'","").split(','))
#     except:
#         pass

# print(ztcls)

sour = soup.find("div", class_="sourinfo").find_all('a')
sourinfo = []
for item in sour:
    sourinfo.append(item.text.replace('\\n','').strip())
print(sourinfo)

url = 'http://kns.cnki.net'

preview = soup_root.find(class_="dllink").a['href']
cajDown = soup_root.find(id='cajDown')['href']
pdfDown = soup_root.find(id='pdfDown')['href']


print(pdfDown)
