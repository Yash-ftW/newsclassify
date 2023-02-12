from langdetect import detect
import numpy as np
import math
from base.Classification import Classify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet
from langdetect import detect
import numpy as np
import math

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

class Summarize:
    def __init__(self,paragraph):
        self.paragraph=paragraph
        self.language=detect(self.paragraph)
        if self.language != "en":
            self.preparagraph = self.nepali_process_paragraph()
        else:
            self.preparagraph = self.english_process_paragraph()
        self.col=[]
        for t in self.preparagraph.split():
            if t not in self.col:
                self.col.append(t)
    
    def nepali_process_paragraph(self):
        paragraph=str(self.paragraph)
        
        #removing \n and \ufeff
        remove=['\n','\ufeff']
        for i in remove:
            paragraph.replace(i,'')
        
        #read stop words
        #Remove Stop Words
        #word_tokens = Tokenizer().word_tokenize(text)
        word_tokens = paragraph.split(" ")
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
        stemmed_string=' '.join(filtered_list)
        
        return stemmed_string
            
    def english_process_paragraph(self):
        paragraph=str(self.paragraph)
        #lowercasing
        paragraph=paragraph.lower()
        #Remove Stop Words
        stop_words=set(stopwords.words('english'))
        word_tokens = word_tokenize(paragraph)
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
        
        #Lematizing
        wordnet_lemmatizer=WordNetLemmatizer()
        lemmatized_list=[wordnet_lemmatizer.lemmatize(w,wordnet.VERB) for w in filtered_list]
        lemmatized_string=' '.join(lemmatized_list)
        
        return lemmatized_string
    
    def calc_idf(self):
        doc_count=len(self.paragraph)
        df={}
        idf={}
        for char in self.col:
            df[char]=0
            idf[char]=0
        #Calculating df
        for i in range(0,len(self.col)):
            for j in range(0,len(self.paragraph)):
                if self.col[i] in self.paragraph[j]:
                    df[self.col[i]]+=1
        #Calculating idf
        for char in self.col:
            idf[char]=math.log((doc_count+1)/(1+df[char]))+1
        return(idf)
    
    def calc_tf_idf(self,sentence):
        idf=self.calc_idf()
        
        tf_idf={}
        word_count={}
    
        for ch in self.col:
            tf_idf[ch]=0
            word_count[ch]=0
        #Calculating tf
        words = sentence.split()
        for ch in words:
            if ch in self.col:
                if ch in word_count:
                    word_count[ch] += 1
                else:
                    word_count[ch] = 1
    
        rough_tfidf=list(self.col)
        for keys in word_count.keys():
            tf_idf[keys]=idf[keys]*word_count[keys]
            if keys in rough_tfidf:
                index=rough_tfidf.index(keys)
                rough_tfidf[index]=tf_idf[keys]
        norm=0
        for i in range(0,len(rough_tfidf)):
            norm+=rough_tfidf[i]**2
        if norm==0:
            norm=1
        for i in range(0,len(rough_tfidf)):
            rough_tfidf[i]=round(rough_tfidf[i]/math.sqrt(norm),8)
        return rough_tfidf
    
    def count_sentence_eng(self):
        cnt=self.paragraph.count(".")+1
        return cnt
    def count_sentence_nep(self):
        cnt=self.paragraph.count("।")+1
        return cnt
    
    def sentence_number(self,number):
        paragraph = self.paragraph
        number = number + 1
        if self.language=="en":
            processed_paragraph=self.english_process_paragraph()
            each_sentence=paragraph.split(".")
            if "" in each_sentence:
                each_sentence.remove("")
            sentence_count=self.count_sentence_eng()
        else:
            processed_paragraph=self.nepali_process_paragraph()
            #paragraph=paragraph.replace("।","|")
            each_sentence=paragraph.split("।")
            if "" in each_sentence:
                each_sentence.remove("")
            sentence_count=self.count_sentence_nep()
            
        
        if  (number>sentence_count):
            print("ERROR: Summarization line exceeds total sentence count")
        
        elif (number == 0):
            print("ERROR: Chosen Zero")
        
        else:
            summarized_indexes = {}
            for index in range(len(each_sentence)):
                tf_idf = sum(self.calc_tf_idf(each_sentence[index]))
                summarized_indexes[tf_idf] = index
            sorted_summarized_indexs = sorted(summarized_indexes.items())[-number:]
            sorted_summarized_indexs = sorted([(t[1], t[0]) for t in sorted_summarized_indexs])
            sorted_summarized_indexs = [x[0] for x in sorted_summarized_indexs]
            summarized = []
            for index in sorted_summarized_indexs:
                summarized.append(each_sentence[index]) 
            summarized_str = str()
            if self.language == 'en':
                for summarized_sentence in summarized:
                    summarized_str += summarized_sentence
                    summarized_str += '. '
            else:
                for summarized_sentence in summarized:
                    summarized_str += summarized_sentence
                    summarized_str += '| '
                    
            return summarized_str
                
            