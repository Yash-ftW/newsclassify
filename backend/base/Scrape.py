from bs4 import BeautifulSoup as BS
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import sqlite3 as sql
from base.Classification import Classify
from base.Summarization import Summarize
import requests
from datetime import datetime
class ScrapeEkantipur:
    
    def __init__(self):
        self.ekantipur_url = "https://ekantipur.com/"
        web_page_ekantipur = requests.get(self.ekantipur_url)
        self.soup_ekantipur = BS(web_page_ekantipur.content,'html.parser')
        
        self.CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.scraped_dict = {}
        
        self.con = sql.connect('database_scrapy.db')
        self.cursor_obj = self.con.cursor()
            
    def cleanhtml(self,raw_html):
        cleantext = re.sub(self.CLEANR, '', raw_html)
        return cleantext

    def clean_text(self,text):
        clean_str = ""
        text_str = str(text)
        text_str = self.cleanhtml(text_str)
        text_str = text_str.replace("\xa0","")
        text_str = text_str.replace("\u202f","")
        clean_str += " "
        clean_str += text_str  
        return clean_str
    
    def get_ekantipur_news_url(self):
        front_link = self.ekantipur_url
        scrape_link = []
        for a in self.soup_ekantipur.find_all('a', href=True):
            if a['href'].split(".")[-1] == 'html':
                if front_link not in a['href']:
                    scrape_link.append(front_link + a['href'])
                elif '...' in a['href']:
                    scrape_link.append(a['href'].split('...')[-1])
                else:
                    scrape_link.append(a['href'])
        
        scrape_link =   list( dict.fromkeys(scrape_link) )
        return scrape_link
    
    def get_ekantipur_scraped_news(self,scrape_link):
        count = 0
        for link in scrape_link[0:3]:
            try:    
                url = link
                web_page = requests.get(url)
                soup = BS(web_page.content,'html.parser')
                
                description = []
                row = soup.select(".normal")

                description_div = soup.select("article")

                for elements in description_div:
                    title = elements.find("h1")
                    title = self.clean_text(title)
                    temp = elements.find_all("p")
                    description.append(temp)
                description = description[0]
                news_str = ""
                for description_text in description:
                    news_str += self.clean_text(description_text)
                source = "Ekantipur"
                
                split_index = len(url.split('/')) -1
                news_id = int(url.split('/')[split_index].replace('.html',''))

                date = datetime.now().strftime("%Y/%m/%d")
                category,confidence = Classify(news_str,model_name='SVM').predict_news()
                
                
                news_sentence_count = news_str.count("।")+1
                summary_count = int(news_sentence_count * (1/4))
                summary = Summarize(news_str).summarize_in_sentence_number(summary_count)
                confidence = max(confidence)
                if confidence > 70:
                    self.scraped_dict[count] = {'news_id':news_id,'link':link,'title':title,'news':news_str,'source':source,'category':category,'date':date,'confidence':confidence,'summary':summary}
                else:
                    self.scraped_dict[count] = {'news_id':news_id,'link':link,'title':title,'news':news_str,'source':source,'category':'OTHERS','date':date,'confidence':confidence,'summary':summary}
                count += 1
                print(self.scraped_dict)
            except:
                continue
        
    def create_table(self):
        table = " CREATE TABLE IF NOT EXISTS nepali_news(news_id INTEGER(20) PRIMARY KEY ,title VARCHAR(100), news VARCHAR(2000), source VARCHAR(100), link VARCHAR(100),category VARCHAR(15),date VARCHAR(25),confidence BIGINT,summary VARCHAR(2000))"
        self.cursor_obj.execute(table)
    
    def update_table(self,key):
        try:
            self.cursor_obj.execute("INSERT INTO nepali_news (news_id,title,news,source,link,category,date,confidence,summary) VALUES (?,?,?,?,?,?,?,?,?)",(self.scraped_dict[key]['news_id'],self.scraped_dict[key]['title'],self.scraped_dict[key]['news'],self.scraped_dict[key]['source'],self.scraped_dict[key]['link'],self.scraped_dict[key]['category'],self.scraped_dict[key]['date'],self.scraped_dict[key]['confidence'],self.scraped_dict[key]['summary']) )
            self.con.commit()
        except sql.Error as er:
            print(er)
        #self.cursor_obj.execute(query)

    def scrape_news(self):
        if self.ekantipur_url != "":
            scrape_link = self.get_ekantipur_news_url()
            print(scrape_link)
            print("HERE")
            self.get_ekantipur_scraped_news(scrape_link)
            self.create_table()
            for key in self.scraped_dict:
                self.update_table(key)
        self.con.close()

class ScrapeSetopati:
    
    def __init__(self):
        self.setopati_url = "https://www.setopati.com/"
        print("Scraping Setopati")
        self.response = requests.get(self.setopati_url)
        self.soup = BS(self.response.content, "html.parser")
        
        web_page_setopati = requests.get(self.setopati_url)
        self.soup_setopati = BS(web_page_setopati.content,'html.parser')
        
        self.CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.scraped_dict = {}
        
        self.con = sql.connect('database_scrapy.db')
        self.cursor_obj = self.con.cursor()
            
    def cleanhtml(self,raw_html):
        cleantext = re.sub(self.CLEANR, '', raw_html)
        return cleantext

    def clean_text(self,text):
        clean_str = ""
        text_str = str(text)
        text_str = self.cleanhtml(text_str)
        text_str = text_str.replace("\xa0","")
        text_str = text_str.replace("\u202f","")
        clean_str += " "
        clean_str += text_str
        clean_str = clean_str.replace("|,","|")  
        clean_str = clean_str.replace("| ,","| ")
        clean_str = clean_str.replace("[","")
        clean_str = clean_str.replace("]","")
        
        return clean_str
    
    def get_setopati_news_url(self):
        scrape_link = []
        main_container = self.soup.find("div",id='content')
        link = main_container.find_all("a")
        # print(link)
        temp_web_links = [web_link['href'] for web_link in link] 

        #removing faltu links
        for links in temp_web_links:
            if links.find("https://www.setopati.com") == 0:
                scrape_link.append(links)

        #removing duplicate links
        scrape_link = list(dict.fromkeys(scrape_link))
        return scrape_link
    
    def get_setopati_scraped_news(self,scrape_link):
        count = 0
        #extracting news articles
        for link in scrape_link[0:3]:
            try:
                url = link
                response = requests.get(url)
                soup = BS(response.content, "html.parser")
                title = soup.find("h1",class_='news-big-title').getText()
                news_body = soup.find("div",class_='editor-box')
                news_str = news_body.find_all("p")
                news_str = self.clean_text(news_str)
                date = datetime.now().strftime("%Y/%m/%d")

                split_index = len(url.split('/')) -1
                news_id = int(url.split('/')[split_index])

                source = "Setopati"
                date = datetime.now().strftime("%Y/%m/%d")
            
                category,confidence = Classify(news_str,model_name='SVM').predict_news()
                
                news_sentence_count = news_str.count("।")+1
                summary_count = int(news_sentence_count * (1/4))
                summary = Summarize(news_str).summarize_in_sentence_number(summary_count)
                confidence = max(confidence)
                if confidence > 70:
                    self.scraped_dict[count] = {'news_id':news_id,'link':link,'title':title,'news':news_str,'source':source,'category':category,'date':date,'confidence':confidence,'summary':summary}
                else:
                    self.scraped_dict[count] = {'news_id':news_id,'link':link,'title':title,'news':news_str,'source':source,'category':'OTHERS','date':date,'confidence':confidence,'summary':summary}
                count += 1
                

            except:
                continue
            
            
    def create_table(self):
        table = " CREATE TABLE IF NOT EXISTS nepali_news(news_id INTEGER(20) PRIMARY KEY ,title VARCHAR(100), news VARCHAR(2000), source VARCHAR(100), link VARCHAR(100),category VARCHAR(15),date VARCHAR(25),confidence BIGINT,summary VARCHAR(2000))"
        self.cursor_obj.execute(table)
    
    def update_table(self,key):
        try:
            self.cursor_obj.execute("INSERT INTO nepali_news (news_id,title,news,source,link,category,date,confidence,summary) VALUES (?,?,?,?,?,?,?,?,?)",(self.scraped_dict[key]['news_id'],self.scraped_dict[key]['title'],self.scraped_dict[key]['news'],self.scraped_dict[key]['source'],self.scraped_dict[key]['link'],self.scraped_dict[key]['category'],self.scraped_dict[key]['date'],self.scraped_dict[key]['confidence'],self.scraped_dict[key]['summary']) )
            self.con.commit()
        except sql.Error as er:
            print(er)
        #self.cursor_obj.execute(query)

    def scrape_news(self):
        if self.setopati_url != "":
            scrape_link = self.get_setopati_news_url()
            self.get_setopati_scraped_news(scrape_link)
            self.create_table()
            for key in self.scraped_dict:
                self.update_table(key)
        self.con.close()
    
class ScrapeBBC:
    
    def __init__(self):
        self.bbc_url = "https://www.bbc.com/"
        print("Scraping BBC")
        self.response = requests.get(self.bbc_url)
        self.soup = BS(self.response.content, "html.parser")
        
        web_page_bbc = requests.get(self.bbc_url)
        self.soup_bbc = BS(web_page_bbc.content,'html.parser')
        
        self.CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.scraped_dict = {}
        
        self.con = sql.connect('database_scrapy.db')
        self.cursor_obj = self.con.cursor()
            
    def cleanhtml(self,raw_html):
        cleantext = re.sub(self.CLEANR, '', raw_html)
        return cleantext

    def clean_text(self,text):
        clean_str = ""
        text_str = str(text)
        text_str = self.cleanhtml(text_str)
        text_str = text_str.replace("\xa0","")
        text_str = text_str.replace("\u202f","")
        clean_str += " "
        clean_str += text_str
        clean_str = clean_str.replace(".,",".")  
        clean_str = clean_str.replace(". ,",". ")
        clean_str = clean_str.replace("[","")
        clean_str = clean_str.replace("]","")
        return clean_str
    
    def get_bbc_news_url(self):
        scrape_link = []
        row = self.soup_bbc.select(".media-list")

        web_links = self.soup_bbc.find_all("a",class_='media__link')
        actual_web_links = [web_link['href'] for web_link in web_links] 

        for links in actual_web_links:
            if links.find("https://www.bbc.com") == -1:
                links = "https://www.bbc.com" + links
            scrape_link.append(links)

        #removing duplicate links
        scrape_link = list(dict.fromkeys(scrape_link))
        return scrape_link
    
    def get_bbc_scraped_news(self,scrape_link):
        count = 0
        for link in scrape_link[0:3]:
            try:
                url = link
                response = requests.get(url)
                soup = BS(response.content, "html.parser")
                title = soup.find("h1").getText()
                if len(soup.find_all("p",class_='ssrcss-1q0x1qg-Paragraph')) != 0:
                    news_str = soup.find_all("p",class_='ssrcss-1q0x1qg-Paragraph')
                    news_str = self.clean_text(news_str)
                    date = datetime.now().strftime("%Y/%m/%d")
                    source = "BBC"
                    
                    split_index = len(url.split('-')) - 1
                    news_id = int(url.split('-')[split_index])
                    category,confidence = Classify(news_str,model_name='SVM').predict_news()

                    news_sentence_count = news_str.count(".")+1
                    summary_count = int(news_sentence_count * (1/4))
                    summary = Summarize(news_str).summarize_in_sentence_number(summary_count)
                    confidence = max(confidence)
                    if confidence > 70:
                        self.scraped_dict[count] = {'news_id':news_id,'link':link,'title':title,'news':news_str,'source':source,'category':category,'date':date,'confidence':confidence,'summary':summary}
                    else:
                        self.scraped_dict[count] = {'news_id':news_id,'link':link,'title':title,'news':news_str,'source':source,'category':'OTHERS','date':date,'confidence':confidence,'summary':summary}
                    count += 1
                    
            except:
                continue
            
    def create_table(self):
        table = " CREATE TABLE IF NOT EXISTS english_news(news_id INTEGER(20) PRIMARY KEY ,title VARCHAR(100), news VARCHAR(2000), source VARCHAR(100), link VARCHAR(100),category VARCHAR(15),date VARCHAR(25),confidence BIGINT,summary VARCHAR(2000))"
        self.cursor_obj.execute(table)
    
    def update_table(self,key):
        try:
            self.cursor_obj.execute("INSERT INTO english_news (news_id,title,news,source,link,category,date,confidence,summary) VALUES (?,?,?,?,?,?,?,?,?)",(self.scraped_dict[key]['news_id'],self.scraped_dict[key]['title'],self.scraped_dict[key]['news'],self.scraped_dict[key]['source'],self.scraped_dict[key]['link'],self.scraped_dict[key]['category'],self.scraped_dict[key]['date'],self.scraped_dict[key]['confidence'],self.scraped_dict[key]['summary']) )
            self.con.commit()
        except sql.Error as er:
            print(er)
        #self.cursor_obj.execute(query)

    def scrape_news(self):
        if self.bbc_url != "":
            scrape_link = self.get_bbc_news_url()
            self.get_bbc_scraped_news(scrape_link)
            self.create_table()
            for key in self.scraped_dict:
                self.update_table(key)
        self.con.close()   
        
class ScrapeKathmanduPost:
    
    def __init__(self):
        self.kathmandupost_url = "https://kathmandupost.com//"
        print("Scraping Kathmandu Post")
        web_page_kathmandupost = requests.get(self.kathmandupost_url)
        self.soup_kathmandupost = BS(web_page_kathmandupost.content,'html.parser')
        
        self.CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.scraped_dict = {}
        
        self.con = sql.connect('database_scrapy.db')
        self.cursor_obj = self.con.cursor()
            
    def cleanhtml(self,raw_html):
        cleantext = re.sub(self.CLEANR, '', raw_html)
        return cleantext

    def clean_text(self,text):
        clean_str = ""
        text_str = str(text)
        text_str = self.cleanhtml(text_str)
        text_str = text_str.replace("\xa0","")
        text_str = text_str.replace("\u202f","")
        clean_str += " "
        clean_str += text_str 
        clean_str = clean_str.replace(".,",".")  
        clean_str = clean_str.replace(". ,",". ")
        clean_str = clean_str.replace("[","")
        clean_str = clean_str.replace("]","")  
        return clean_str
    
    def get_kathmandupost_news_url(self):
        scrape_link = []
        
        main_container = self.soup_kathmandupost.find("main")
        web_links = main_container.find_all("a") 

        for links in web_links:
            links = links['href']
            if links.find("https://kathmandupost.com/") == -1:
                links = "https://kathmandupost.com" + links
            scrape_link.append(links)

        #removing duplicate links
        scrape_link = list(dict.fromkeys(scrape_link))
        return scrape_link
    
    def get_kathmandupost_scraped_news(self,scrape_link):
        count = 0
        for link in scrape_link[0:3]:
            try:
                url = link
                response = requests.get(url)
                soup = BS(response.content, "html.parser")
                title = soup.find(attrs={"style": "margin-bottom:0.1rem;"}).get_text()
                temp_container=soup.find("section",class_='story-section')
                news_str = temp_container.find_all('p')
                news_str = self.clean_text(news_str)
                
                date = datetime.now().strftime("%Y/%m/%d")                
                source = "KathmanduPost"
                split_index = len(url.split('/')) - 1
                news_id = url.split('/')[split_index]
                news_id = int(''.join(str(ord(c)) for c in news_id)[0:10])
                
                category,confidence = Classify(news_str,model_name='SVM').predict_news()
                news_sentence_count = news_str.count(".")+1
                summary_count = int(news_sentence_count * (1/4))
                summary = Summarize(news_str).summarize_in_sentence_number(summary_count)
                confidence = max(confidence)
                if confidence > 70:
                    self.scraped_dict[count] = {'news_id':news_id,'link':link,'title':title,'news':news_str,'source':source,'category':category,'date':date,'confidence':confidence,'summary':summary}
                else:
                    self.scraped_dict[count] = {'news_id':news_id,'link':link,'title':title,'news':news_str,'source':source,'category':'OTHERS','date':date,'confidence':confidence,'summary':summary}
                count += 1
            except:
                continue
                  
    def create_table(self):
        table = " CREATE TABLE IF NOT EXISTS english_news(news_id INTEGER(20) PRIMARY KEY ,title VARCHAR(100), news VARCHAR(2000), source VARCHAR(100), link VARCHAR(100),category VARCHAR(15),date VARCHAR(25),confidence BIGINT,summary VARCHAR(2000))"
        self.cursor_obj.execute(table)
    
    def update_table(self,key):
        try:
            self.cursor_obj.execute("INSERT INTO english_news (news_id,title,news,source,link,category,date,confidence,summary) VALUES (?,?,?,?,?,?,?,?,?)",(self.scraped_dict[key]['news_id'],self.scraped_dict[key]['title'],self.scraped_dict[key]['news'],self.scraped_dict[key]['source'],self.scraped_dict[key]['link'],self.scraped_dict[key]['category'],self.scraped_dict[key]['date'],self.scraped_dict[key]['confidence'],self.scraped_dict[key]['summary']) )
            self.con.commit()
        except sql.Error as er:
            print(er)
        #self.cursor_obj.execute(query)

    def scrape_news(self):
        if self.kathmandupost_url != "":
            scrape_link = self.get_kathmandupost_news_url()
            self.get_kathmandupost_scraped_news(scrape_link)
            self.create_table()
            for key in self.scraped_dict:
                self.update_table(key)
        self.con.close()      