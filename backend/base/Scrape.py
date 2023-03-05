import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as BS
import urllib3
import detect
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import sqlite3 as sql
from base.Classification import Classify
from base.Summarization import Summarize

class Scrape_Nepali_News:
    
    def __init__(self):
        self.ekantipur_url = "https://ekantipur.com"
        
        http = urllib3.PoolManager()
        http.addheaders = [('User-agent','Mozilla/61.0')]
        web_page_ekantipur = http.request('GET',self.ekantipur_url)
        self.soup_ekantipur = BS(web_page_ekantipur.data,'html')
        
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
        for link in scrape_link:
            url = link
            http = urllib3.PoolManager()
            http.addheaders = [('User-agent','Mozilla/61.0')]
            web_page = http.request('GET',url)
            soup = BS(web_page.data,'html')
            
            description = []
            row = soup.select(".normal")
            #title = row.find("h1")

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
            source = (link.split('.')[0]).split('//')[1]
            date = url.split('/')[4] + '/' + url.split('/')[5] + '/' + url.split('/')[6]
            category,confidence = Classify(news_str).Predict_News()
            
            print("/n /n /n /n")
            
            news_sentence_count = news_str.count("।")+1
            print(news_sentence_count)
            summary_count = int(news_sentence_count * (1/4))
            summary = Summarize(news_str).sentence_number(summary_count)
            confidence = max(confidence)
            if confidence > 30:
                self.scraped_dict[count] = {'link':link,'title':title,'news':news_str,'source':source,'category':category,'date':date,'confidence':confidence,'summary':summary}
            else:
                self.scraped_dict[count] = {'link':link,'title':title,'news':news_str,'source':source,'category':'OTHERS','date':date,'confidence':confidence,'summary':summary}
            count += 1
        
    def create_table(self):
        table = " CREATE TABLE IF NOT EXISTS nepali_news(pk_categoryid INTEGER PRIMARY KEY AUTOINCREMENT,title VARCHAR(100), news VARCHAR(2000), source VARCHAR(100), link VARCHAR(100),category VARCHAR(15),date VARCHAR(25),confidence BIGINT,summary VARCHAR(2000))"
        self.cursor_obj.execute(table)
    
    def update_table(self,key):
        try:
            self.cursor_obj.execute("INSERT INTO nepali_news (title,news,source,link,category,date,confidence,summary) VALUES (?,?,?,?,?,?,?,?)",(self.scraped_dict[key]['title'],self.scraped_dict[key]['news'],self.scraped_dict[key]['source'],self.scraped_dict[key]['link'],self.scraped_dict[key]['category'],self.scraped_dict[key]['date'],self.scraped_dict[key]['confidence'],self.scraped_dict[key]['summary']) )
            self.con.commit()
        except sql.Error as er:
            print(er)
        #self.cursor_obj.execute(query)

    def scrape_nepali_news(self):
        if self.ekantipur_url != "":
            scrape_link = self.get_ekantipur_news_url()
            self.get_ekantipur_scraped_news(scrape_link[0:10])
            self.create_table()
            for key in self.scraped_dict:
                self.update_table(key)
        self.con.close()
    
    
            