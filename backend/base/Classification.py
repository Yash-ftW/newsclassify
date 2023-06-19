import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import joblib
from langdetect import detect
import pickle

import os

model_directory = "backend/base/model"

# Get the absolute path to the directory containing the current script
base_path = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the model directory
model_path = os.path.join(base_path, model_directory)

# Loading Models
# nepali_model = joblib.load('base/model/nepali_model_1000.pkl')
# english_model = joblib.load('base/model/english_model.pkl')
# Loading idf values
with open('base/idf_values/nepali_tfidf_1000.model','rb') as f:
    nepali_base_tfidf = pickle.load(f)

with open('base/idf_values/english_tfidf.model','rb') as f:
    english_base_tfidf = pickle.load(f)

# Loading Nepali words and numbers

#stop_words
stop_words=open("base/nepali_words/stopwords.txt","r",encoding="utf-8")
stop_words=stop_words.read()
stop_words=stop_words.split("\n")

#num file
nepali_num=open("base/nepali_words/numbers.txt","r",encoding="utf-8")
nepali_num=nepali_num.read()
nepali_num=nepali_num.split(",")

#suffix file
nepali_suffix=open("base/nepali_words/suffix.txt","r",encoding="utf-8")
nepali_suffix=nepali_suffix.read()
nepali_suffix=nepali_suffix.split("\n")


class Classify:
    def __init__(self,news,model_name):
        self.news = news
        self.language = detect(self.news)
        #self.model_selection = model_selection
        if self.language != "en":
            self.pre_processed_news = self.pre_process_nepali_news()
            self.model = joblib.load(f"E:\\My Files\\Class\\Sem VII\\Project Work\\news\\newsclassify\\backend\\base\model\\{model_name}_model_nepali.pkl")
        else:
            self.pre_processed_news = self.pre_process_english_news()
            self.model = joblib.load(f"E:\\My Files\\Class\\Sem VII\\Project Work\\news\\newsclassify\\backend\\base\\model\\{model_name}_model_english.pkl")
            
        self.category_class = ['business', 'entertainment', 'politics', 'sport', 'tech']
    def pre_process_nepali_news(self):
        news = self.news
        
        #removing \n and \ufeff
        remove=['\n','\ufeff']
        for i in remove:
            news.replace(i,'')
        
        #Remove Stop Words
        word_tokens = news.split(" ")
        filtered_list = [w for w in word_tokens if not w in stop_words]
        
        #Remove Nepali numbers
        num_filter=[]
        for i in range(0,len(filtered_list)):
            for j in range(0,len(nepali_num)):
                if nepali_num[j] in filtered_list[i]:
                    num_filter.append(filtered_list[i])
                    break
        for filter in num_filter:
            filtered_list.remove(filter)
        
        #Remove English numbers
        num=['0','1','2','3','4','5','6','7','8','9']
        num_filter=[]
        for i in range(0,len(filtered_list)):
            for j in range(0,len(num)):
                if num[j] in filtered_list[i]:
                    num_filter.append(filtered_list[i])
                    break
        for filter in num_filter:
            filtered_list.remove(filter)       
        
        #Stemming Manual
        filtered_string =' '.join(filtered_list)
        
        #stemmed_string=' '.join(filtered_list)
        
        return filtered_string
    
    def pre_process_english_news(self):
        news=str(self.news)
        
        #lowercasing
        news=news.lower()
        
        #Remove Stop Words
        stop_words=set(stopwords.words('english'))
        word_tokens = word_tokenize(news)
        filtered_list = [w for w in word_tokens if not w in stop_words]
        
        #Remove numbers and special Symbols
        #words like 100m 2m were not removed so using this
        num=['0','1','2','3','4','5','6','7','8','9']
        num_filter=[]
        for i in range(0,len(filtered_list)):
            for j in range(0,len(num)):
                if num[j] in filtered_list[i]:
                    num_filter.append(filtered_list[i])
                    break
        
        for filter in num_filter:
            filtered_list.remove(filter)
                    
        filtered_list = [w for w in filtered_list if w.isalnum()]
        filtered_list=  [w for w in filtered_list if not w.isdigit()]
        
        #Lematizing
        wordnet_lemmatizer=WordNetLemmatizer()
        lemmatized_list=[wordnet_lemmatizer.lemmatize(w,wordnet.VERB) for w in filtered_list]
        lemmatized_string=' '.join(lemmatized_list)
        
        return lemmatized_string
    
    def predict_news(self):
        
        if self.language != "en":
            tf_idf = nepali_base_tfidf.transform([self.pre_processed_news]).toarray()
        else:
            tf_idf = english_base_tfidf.transform([self.pre_processed_news]).toarray()
        
        confidence = self.model.predict_proba(tf_idf)
        index = np.argmax(confidence)
        confidence = [np.around(x*100,2) for x in confidence][0]
        return(self.category_class[int(index)].upper(),confidence)
            