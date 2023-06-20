from langdetect import detect
import math
from langdetect import detect
import math

# Loading Nepali words and numbers

class SummarizeForVisualization:
    def __init__(self,news):
        self.news = news
        self.language=detect(self.news)
        self.summarizeSentence = []
        for t in self.news.split():
            if t not in self.summarizeSentence:
                self.summarizeSentence.append(t)
    
    def calc_idf(self):
        doc_count=len(self.news)
        df={}
        idf={}
        for char in self.summarizeSentence:
            df[char]=0
            idf[char]=0
        #Calculating df
        for i in range(0,len(self.summarizeSentence)):
            for j in range(0,len(self.news)):
                if self.summarizeSentence[i] in self.news[j]:
                    df[self.summarizeSentence[i]]+=1
        #Calculating idf
        for char in self.summarizeSentence:
            idf[char]=math.log((doc_count+1)/(1+df[char]))+1
        return(idf)
    
    def calc_tf_idf(self,sentence):
        idf=self.calc_idf()
        
        tf_idf={}
        word_count={}
    
        for ch in self.summarizeSentence:
            tf_idf[ch]=0
            word_count[ch]=0
        #Calculating tf
        words = sentence.split()
        for ch in words:
            if ch in self.summarizeSentence:
                if ch in word_count:
                    word_count[ch] += 1
                else:
                    word_count[ch] = 1
    
        rough_tfidf=list(self.summarizeSentence)
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
        cnt=self.news.count(".")+1
        return cnt
    def count_sentence_nep(self):
        cnt=self.news.count("।")+1
        return cnt
    
    def summarize_in_sentence_number(self,number):
        paragraph = self.news
        number = number + 1
        tf_idf_each_sentence = {}
        if self.language=="en":
            each_sentence=paragraph.split(".")
            if "" in each_sentence:
                each_sentence.remove("")
            sentence_count=self.count_sentence_eng()
        else:
            #paragraph=paragraph.replace("।","|")
            each_sentence=paragraph.split("।")
            if "" in each_sentence:
                each_sentence.remove("")
            sentence_count=self.count_sentence_nep()
            
        
        if  (number>sentence_count):
            return("ERROR: Summarization line exceeds total sentence count")
        
        elif (number == 0):
            return("ERROR: Chosen Zero")
        
        else:
            summarized_indexes = {}
            for index in range(len(each_sentence)):
                tf_idf = sum(self.calc_tf_idf(each_sentence[index]))
                each_sentence[index] = f" ({index+1}) " + each_sentence[index]

                tf_idf_each_sentence[index + 1] = format(tf_idf,".2f")
                
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
                    summarized_str += ' | '
                    
            return summarized_str,tf_idf_each_sentence
                