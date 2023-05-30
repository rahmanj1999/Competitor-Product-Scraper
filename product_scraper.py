#Scraper to get products from competitors so they could be added to my website

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time







def Product_Scraper(main_link):
    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920,1080")

    #option.add_argument("--headless")

    driver = webdriver.Chrome('chromedriver.exe',options= option)
    driver.get(main_link)
    time.sleep(5)
    Links = []

    x = 0
    while x == 0:
        try:
            time.sleep(5)


            text = driver.page_source
            soup = BeautifulSoup(text, 'lxml')



            for i in (soup.findAll('h2',{'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-4'})):
                try:
                    Links.append('https://www.amazon.co.uk'+i.find('a').get('href'))
                except:
                    pass


            elem = driver.find_element_by_class_name('a-last')
            elem.find_element_by_tag_name('a').click()
            x = 0
        except:
            x = 1
            pass





    All_Links = []
    df = pd.DataFrame({'All_Links':All_Links})
    df.to_excel('Links_DB.xlsx',index=False)



    for link in Links:
        url = link
        driver.get(url)
        time.sleep(3)

        text = driver.page_source
        soup = BeautifulSoup(text, 'lxml')



        try:
            for i in soup.find('ul',{'class':'a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare imageSwatches'}).findAll('li'):
                try:
                    df = pd.read_excel('Links_DB.xlsx')
                    my_link = []
                    my_link.append('/'.join(url.split('/')[:4])+i.get('data-dp-url'))
                    All_Links.append('/'.join(url.split('/')[:4])+i.get('data-dp-url'))
                    print('Link is added into a list')
                    data = pd.DataFrame({'All_Links':my_link})
                    df = df.append(data)
                    df.to_excel('Links_DB.xlsx',index=False)
                except:
                    pass
        except:
            pass





        Size_Links = []
        try:
            for i in soup.find('ul',{'class':'a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare'}).findAll('li'):
                try:
                    Size_Links.append('/'.join(url.split('/')[:4])+i.get('data-dp-url'))
                except:
                    pass
        except:
            pass


        try: 
            for i in range(len(Size_Links)):
                try:
                    driver.get(Size_Links[i])
                    time.sleep(3)

                    text = driver.page_source
                    soup = BeautifulSoup(text, 'lxml')

                    try:
                        for i in soup.find('ul',{'class':'a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare imageSwatches'}).findAll('li'):
                            try:
                                df = pd.read_excel('Links_DB.xlsx')
                                my_link = []
                                my_link.append('/'.join(url.split('/')[:4])+i.get('data-dp-url'))
                                All_Links.append('/'.join(url.split('/')[:4])+i.get('data-dp-url'))
                                print('Link is added into a list')
                                data = pd.DataFrame({'All_Links':my_link})
                                df = df.append(data)
                                df.to_excel('Links_DB.xlsx',index=False)
                            except:
                                pass
                    except:
                        df = pd.read_excel('Links_DB.xlsx')
                        my_link = []
                        my_link.append(Size_Links[i])
                        data = pd.DataFrame({'All_Links':my_link})
                        df = df.append(data)
                        df.to_excel('Links_DB.xlsx',index=False)
                        print('done')
                except:
                    pass
        except:
            pass



    data_Links = []
    data_text = []

    df = pd.read_excel('Links_DB.xlsx')
    links = df['All_Links'].to_list()


    for i in links:
        driver.get(i)
        time.sleep(5)
        text = driver.page_source
        soup = BeautifulSoup(text, 'lxml')

        free_text = ''
        try:
            free_text = soup.find('span',{'id':'ourprice_shippingmessage'}).text.strip().lower()
            if 'free delivery' in free_text:
                data_Links.append(i)
                data_text.append(free_text)
                print(free_text)

        except:
            pass


    df = pd.DataFrame({'Links':data_Links,'Free':data_text})
    df.to_excel('Free Delivery Links.xlsx',index = False)





Amazon_Scraper('https://www.amazon.co.uk/s?k=motorcycle+helmet&i=automotive&rh=n%3A301311031%2Cn%3A2491856031%2Cp_76%3A419158031&dc&qid=1590951328&refresh=1&rnid=1642204031&ref=sr_pg_1')






