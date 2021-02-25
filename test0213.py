"""
專案步驟:
1.商品清單頁取得商品連結(每頁60件商品)
2.從商品頁取得每個商品資訊11項，存入list
3.換頁,重複步驟1.2，直到爬完8個頁面
4.將取得資料存入excel
"""
# 當爬取的網頁為 JavaScript 網頁前端（非伺服器端）生成，需引入 selenium 套件來模擬瀏覽器載入網頁並跑完 JavaScript 程式才能取得資料
from selenium import webdriver
# 引入套件
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import codecs
# ./chromedriver.exe 為 chrome 瀏覽器驅動引擎檔案位置（注意 MacOS/Linux 沒有 .exe 副檔名），也可以使用絕對路徑，例如： C:\downloads\chromedriver.exe

#步驟1 爬取搜尋結果的商品連結清單
def linklist(url):
    driver = webdriver.Chrome('./chromedriver.exe')
    # 發出網路請求
    driver.get(url)
    # 取出網頁整頁內容
    page_content = driver.page_source
    # 將 HTML 內容轉換成 BeautifulSoup 物件，html.parser 為使用的解析器
    soup = BeautifulSoup (page_content, 'html.parser')
    # 透過 select 使用 CSS 選擇器 選取我們要選的 html 內容
    links = soup.select('#filterItems .m-card-product')
    # 檢視是否有抓取到產品網址
    link_lists = []
    for l in links:
        prodlist  = l.select('.link-top a')[0]['href'] 
        urls = f'https://www.pinkoi.com/{prodlist}'
        link_lists.append(urls)
        #print(len(link_lists)) 第一頁72個品項
    return link_lists
           
#步驟2 從商品連結取得商品資訊      
def Crawl_prodinfo(link_lists):
   row_list1 = [] 
   links = link_lists
   #print(links)--有順利列印出來嘞
   # 挑選第一頁資料作為範例
   #urls = f'https://www.pinkoi.com/{prodlist}'
   for i in links:
     #嘗試不開網頁搜尋
     option = webdriver.ChromeOptions()
     option.add_argument("headless")
     driver = webdriver.Chrome('./chromedriver.exe', chrome_options=option)
     #driver = webdriver.Chrome('./chromedriver.exe')
     driver.get(i)
     page_content2 = driver.page_source
     soup2 = BeautifulSoup(page_content2, 'html.parser')
     products = soup2.select('#sider .m-product-list')
     #print(products)
     #商品名
     prod_name = soup2.select('div.m-product-main-info.m-box.test-product-main-info > h1 > span')[0].getText()
     #價錢
     prod_price = soup2.select('div.m-product-main-info.m-box.test-product-main-info > div > div.price-wrap > div > span.amount')[0].getText()
     #商店名
     prod_store = soup2.select('div > div.m-clearfix > div > p > a')[0].getText()
     #產品材質,去除/n
     prod_mat = soup2.select('dl > div:nth-child(1) > dd')[0].getText()
     prod_mat = prod_mat.replace("\n","")
     #產地,去除/n和空格
     prod_location = soup2.select('dl > div:nth-child(3) > dd')[0].getText()
     prod_location = prod_location.replace("\n","").strip()
     #庫存,去除/n和空格
     prod_stock = soup2.select('dl > div:nth-child(5) > dd')[0].getText()
     prod_stock = prod_stock.replace("\n","").strip()
     #view
     prod_view = soup2.select ('dd > ul > li:nth-child(1)')[0].getText()
     #sold
     prod_sold = soup2.select('dd > ul > li:nth-child(2)')[0].getText()
     #評價數
     prod_rating_num = soup2.select('div > div.m-clearfix > div > div > div.shop-ratings > a:nth-child(2) > span')[0].getText()
     #回應率,去除/n和空格
     prod_response = soup2.select('#js-block-shop > div > dl > div:nth-child(1) > dd')[0].getText()
     prod_response = prod_response.replace("\n","").strip()
     #出貨速度,去除/n和空格
     prod_shipping = soup2.select('#js-block-shop > div > dl > div:nth-child(3) > dd')[0].getText()
     prod_shipping = prod_shipping.replace("\n","").strip()
     data = {}
     data['product_name'] = prod_name
     data['price'] = prod_price
     data['store'] = prod_store
     data['mat'] = prod_mat
     data['location'] = prod_location
     data['stock'] = prod_stock
     data['view'] = prod_view
     data['sold'] = prod_sold 
     data['rating_num'] = prod_rating_num
     data['res_rate'] = prod_response  
     data['shipping'] = prod_shipping
     row_list1.append(data)
     print("列印商品資訊中....")
     #print(row_list1)
     time.sleep(2)  
     driver.quit()
   return row_list1

def save_csv(row_list1):
    headers = ['product_name','price','store', 'mat', 'location','stock','view','sold','rating_num','res_rate','shipping']
    with open ('products.csv', 'a', newline='', encoding='utf-8') as fp:
       dict_writer = csv.DictWriter(fp, headers)
       dict_writer.writeheader()
       dict_writer.writerows(row_list1)

  

if __name__=="__main__":
   url = 'https://www.pinkoi.com/search?page={}&q=%E7%9C%BC%E7%BD%A9'
   for i in range(7,9):
       url = f'https://www.pinkoi.com/search?page={i}&q=%E7%9C%BC%E7%BD%A9'
       link_lists = linklist(url)
       row_list1 = Crawl_prodinfo(link_lists)
       print(row_list1) 
       save_csv(row_list1)
