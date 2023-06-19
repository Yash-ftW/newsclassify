from flask import Flask, request, render_template,jsonify
from base.Classification import Classify
from base.Summarization import Summarize
from base.Scrape import ScrapeSetopati,ScrapeEkantipur,ScrapeBBC,ScrapeKathmanduPost
from flask_cors import CORS
import json
import sqlite3  as sql
app = Flask(__name__)
CORS(app)
category_class = ['business', 'entertainment', 'politics', 'sport', 'tech']
global row_dict_flag
row_dict_flag = None
@app.route('/data')
def home_page():
    return {"Hello":"World"}

@app.route('/test',methods=['POST'])
def testhere():
    my_value = request.json['category']
    print (my_value)
    return my_value



@app.route('/api/form', methods=['POST'])
def handle_form_data():
    form_data = request.json
    news = str(form_data['news'])
    summarization_count = int(form_data['count']) -1
    model_name = str(form_data['model'])
    confidence_dict = {}
    
    if summarization_count == '':
        summarized_news,tf_idf_each_sentence = Summarize(news).summarize_in_sentence_number(10)
    else:
        summarized_news,tf_idf_each_sentence = Summarize(news).summarize_in_sentence_number(int(summarization_count))
    
    print(tf_idf_each_sentence)
    
    summarized_news = summarized_news
    prediction,confidence = Classify(news,model_name).predict_news()
    confidence_dict = {category_class:confidence for (category_class,confidence) in zip(category_class,confidence)}
    print(confidence_dict)
    return jsonify({'text':news,'summarized':summarized_news,'count':summarization_count,'prediction':prediction,'confidence':confidence_dict,'tf_idf':tf_idf_each_sentence})
    
   


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classifcation')
def english_form():
    return render_template('Form.html')
    
    

@app.route('/classifcation',methods = ['POST'])
def english_submit_form():
    news = request.form['news']
    summarization_count = request.form['summarization_count']
    
    if summarization_count == '':
        summarized_news,tf_idf_each_sentence = Summarize(news).summarize_in_sentence_number(11)
    else:
        summarized_news,tf_idf_each_sentence = Summarize(news).summarize_in_sentence_number(int(summarization_count))
    
    summarized_news = summarized_news
    prediction ,confidence = Classify(news).predict_news()
    print(max(confidence))
    return render_template('Form.html',text = news, summarized = summarized_news,summarization_count = summarization_count,prediction = prediction,confidence = confidence)

@app.route('/scrapeNepaliNews')
def scrape_nepali():
    # ScrapeEkantipur().scrape_news()
    ScrapeSetopati().scrape_news()
    return jsonify({"scraped":1})

@app.route('/scrapeEnglishNews')
def scrape_english():
    ScrapeBBC().scrape_news()
    ScrapeKathmanduPost().scrape_news()
    # return render_template('index.html')
    return jsonify({'scrapped':1})

@app.route('/scraped_nepali_news')
def scrapped_nepali_news():
    con = sql.connect('database_scrapy.db')
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * FROM nepali_news ORDER BY confidence DESC ")
    
    rows = cur.fetchall()
    return render_template("ViewScrapped.html",rows = rows)

@app.route('/scraped_english_news')
def scrapped_english_news():
    con = sql.connect('database_scrapy.db')
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * FROM english_news ORDER BY confidence DESC ")
    
    rows = cur.fetchall()
    return render_template("ViewScrapped.html",rows = rows)

@app.route('/dynamic_fetch',methods=['GET', 'POST'])
def fetch_scrapped_news():
    global next_item_index
    global row_dict
        
    if request.method != 'POST':
        row_dict = {}
        con = sql.connect('database_scrapy.db')
        cur = con.cursor()
        con.row_factory = sql.Row
    
        cur.execute("SELECT * FROM nepali_news ORDER BY confidence DESC")
        fetch_row = cur.fetchall()
        index = 0
        
        
        for row in fetch_row:
            row_dict[index] = {'pk_categoryid':row[0],'title':row[1],'news':row[2],'source':row[3],'link':row[4],'category':row[5],'date':row[6],'confidence':row[7],'summary':row[8]}
            index += 1
        
        #print(row_dict)
        con.close()
        
        next_item_index = 0
        flag = 1 
        return render_template('fetch_single.html',data=row_dict[0],news=row_dict[0]['news'])
    else:    
        if request.form['submit_button'] == 'Next':
            next_item_index += 1
            return render_template('fetch_single.html',data=row_dict[next_item_index],news = row_dict[next_item_index]['news'])
        if request.form['submit_button'] == 'Previous':
            next_item_index -= 1
            return render_template('fetch_single.html',data=row_dict[next_item_index],news = row_dict[next_item_index]['news'])
        else:
            sentence_count = int(request.form['summarization_count'])
            news = Summarize(row_dict[next_item_index]['news']).summarize_in_sentence_number(sentence_count)
            return render_template('fetch_single.html',data=row_dict[next_item_index],news = news)
        

@app.route('/api/fetchScrapeNepali',methods=['GET','POST'])
def fetch_scrapped_nepali_news():
    global next_item_index
    global row_dict
    
    if request.method != 'POST': 
        row_dict = {}
        con = sql.connect('database_scrapy.db')
        cur = con.cursor()
        con.row_factory = sql.Row
        cur.execute("SELECT * FROM nepali_news WHERE category =? ORDER BY date DESC", ["BUSINESS"])
        fetch_row = cur.fetchall()
        if len(fetch_row) != 0:
            index = 0
            next_item_index = 0 
            for row in fetch_row:
                row_dict[index] = {'pk_categoryid':row[0],'title':row[1],'news':row[2],'source':row[3],'link':row[4],'category':row[5],'date':row[6],'confidence':row[7],'summary':row[8]}
                index += 1
                # Create a new dictionary to store the non-duplicate rows
            new_row_dict = {}

            # Create a set to keep track of the titles seen so far
            titles_seen = set()

            # Loop through the original row_dict and only add rows with unique titles to the new dictionary
            for index, row in row_dict.items():
                title = row['title']
                if title not in titles_seen:
                    new_row_dict[index] = row
                    titles_seen.add(title)

            # Update the original row_dict with the non-duplicate rows
            row_dict = new_row_dict
            # Create a new dictionary to store the reindexed rows
            reindexed_dict = {}

            # Loop through the rows in the row_dict and reindex them
            for i, (index, row) in enumerate(row_dict.items()):
                reindexed_dict[i] = row

            # Update the original row_dict with the reindexed rows
            row_dict = reindexed_dict
            con.close()
            return jsonify({'error':0,'title':row_dict[0]['title'],'summary':row_dict[0]['summary'],'date':row_dict[0]['date'],'category':row_dict[0]['category'],'link':row_dict[0]['link']})

        else:
            
            return jsonify({'title':"No Title For Now",'summary':"No Summary For Now",'date':"Date Unavailable",'category':"BUSINESS",'link':"No link Avialable"})
    else:
        if request.json["changeCategory"] != "":
            row_dict = {}
            con = sql.connect('database_scrapy.db')
            cur = con.cursor()
            con.row_factory = sql.Row
            change_category = request.json["changeCategory"]
            
        
            cur.execute("SELECT * FROM nepali_news WHERE category = ? ORDER BY date DESC", [change_category])
            fetch_row = cur.fetchall()
            if len(fetch_row) != 0:
                index = 0
                next_item_index = 0 
                for row in fetch_row:
                    row_dict[index] = {'pk_categoryid':row[0],'title':row[1],'news':row[2],'source':row[3],'link':row[4],'category':row[5],'date':row[6],'confidence':row[7],'summary':row[8]}
                    index += 1
                # Create a new dictionary to store the non-duplicate rows
                new_row_dict = {}

                # Create a set to keep track of the titles seen so far
                titles_seen = set()

                # Loop through the original row_dict and only add rows with unique titles to the new dictionary
                for index, row in row_dict.items():
                    title = row['title']
                    if title not in titles_seen:
                        new_row_dict[index] = row
                        titles_seen.add(title)

                # Update the original row_dict with the non-duplicate rows
                row_dict = new_row_dict
                # Create a new dictionary to store the reindexed rows
                reindexed_dict = {}

                # Loop through the rows in the row_dict and reindex them
                for i, (index, row) in enumerate(row_dict.items()):
                    reindexed_dict[i] = row

                # Update the original row_dict with the reindexed rows
                row_dict = reindexed_dict
                con.close()
                return jsonify({'error':0,'title':row_dict[0]['title'],'summary':row_dict[0]['summary'],'date':row_dict[0]['date'],'category':row_dict[0]['category'],'link':row_dict[0]['link']})
            else:
            
                return jsonify({'title':"No Title For Now",'summary':"No Summary For Now",'date':"Date Unavailable",'category':change_category,'link':"No link Avialable"})
        else:
            change_news = request.json["dest"]
            if change_news == 'Next News':
                next_item_index += 1
                return jsonify({'error':0,'title':row_dict[next_item_index]['title'],'summary':row_dict[next_item_index]['summary'],'date':row_dict[next_item_index]['date'],'category':row_dict[next_item_index]['category'],'link':row_dict[next_item_index]['link']})
            if change_news == 'Previous News':
                next_item_index -= 1
                return jsonify({'error':0,'title':row_dict[next_item_index]['title'],'summary':row_dict[next_item_index]['summary'],'date':row_dict[next_item_index]['date'],'category':row_dict[next_item_index]['category'],'link':row_dict[next_item_index]['link']})

@app.route('/api/fetchScrapeEnglish',methods=['GET','POST'])
def fetch_scrapped_english_news():
    global next_item_index
    global row_dict
    
    if request.method != 'POST': 
        row_dict = {}
        con = sql.connect('database_scrapy.db')
        cur = con.cursor()
        con.row_factory = sql.Row
        cur.execute("SELECT * FROM english_news WHERE category =? ORDER BY date DESC", ["BUSINESS"])
        fetch_row = cur.fetchall()
        if len(fetch_row) != 0:
            index = 0
            next_item_index = 0 
            for row in fetch_row:
                row_dict[index] = {'pk_categoryid':row[0],'title':row[1],'news':row[2],'source':row[3],'link':row[4],'category':row[5],'date':row[6],'confidence':row[7],'summary':row[8]}
                index += 1
                # Create a new dictionary to store the non-duplicate rows
            new_row_dict = {}

            # Create a set to keep track of the titles seen so far
            titles_seen = set()

            # Loop through the original row_dict and only add rows with unique titles to the new dictionary
            for index, row in row_dict.items():
                title = row['title']
                if title not in titles_seen:
                    new_row_dict[index] = row
                    titles_seen.add(title)

            # Update the original row_dict with the non-duplicate rows
            row_dict = new_row_dict
            # Create a new dictionary to store the reindexed rows
            reindexed_dict = {}

            # Loop through the rows in the row_dict and reindex them
            for i, (index, row) in enumerate(row_dict.items()):
                reindexed_dict[i] = row

            # Update the original row_dict with the reindexed rows
            row_dict = reindexed_dict
            con.close()
            return jsonify({'error':0,'title':row_dict[0]['title'],'summary':row_dict[0]['summary'],'date':row_dict[0]['date'],'category':row_dict[0]['category'],'link':row_dict[0]['link']})

        else:
            
            return jsonify({'title':"No Title For Now",'summary':"No Summary For Now",'date':"Date Unavailable",'category':"BUSINESS",'link':"No link Avialable"})
    else:
        if request.json["changeCategory"] != "":
            row_dict = {}
            con = sql.connect('database_scrapy.db')
            cur = con.cursor()
            con.row_factory = sql.Row
            change_category = request.json["changeCategory"]
            
        
            cur.execute("SELECT * FROM english_news WHERE category = ? ORDER BY date DESC", [change_category])
            fetch_row = cur.fetchall()
            if len(fetch_row) != 0:
                index = 0
                next_item_index = 0 
                for row in fetch_row:
                    row_dict[index] = {'pk_categoryid':row[0],'title':row[1],'news':row[2],'source':row[3],'link':row[4],'category':row[5],'date':row[6],'confidence':row[7],'summary':row[8]}
                    index += 1
                # Create a new dictionary to store the non-duplicate rows
                new_row_dict = {}

                # Create a set to keep track of the titles seen so far
                titles_seen = set()

                # Loop through the original row_dict and only add rows with unique titles to the new dictionary
                for index, row in row_dict.items():
                    title = row['title']
                    if title not in titles_seen:
                        new_row_dict[index] = row
                        titles_seen.add(title)

                # Update the original row_dict with the non-duplicate rows
                row_dict = new_row_dict
                # Create a new dictionary to store the reindexed rows
                reindexed_dict = {}

                # Loop through the rows in the row_dict and reindex them
                for i, (index, row) in enumerate(row_dict.items()):
                    reindexed_dict[i] = row

                # Update the original row_dict with the reindexed rows
                row_dict = reindexed_dict
                con.close()
                return jsonify({'error':0,'title':row_dict[0]['title'],'summary':row_dict[0]['summary'],'date':row_dict[0]['date'],'category':row_dict[0]['category'],'link':row_dict[0]['link']})
            else:
            
                return jsonify({'title':"No Title For Now",'summary':"No Summary For Now",'date':"Date Unavailable",'category':change_category,'link':"No link Avialable"})
        else:
            change_news = request.json["dest"]
            if change_news == 'Next News':
                next_item_index += 1
                return jsonify({'error':0,'title':row_dict[next_item_index]['title'],'summary':row_dict[next_item_index]['summary'],'date':row_dict[next_item_index]['date'],'category':row_dict[next_item_index]['category'],'link':row_dict[next_item_index]['link']})
            if change_news == 'Previous News':
                next_item_index -= 1
                return jsonify({'error':0,'title':row_dict[next_item_index]['title'],'summary':row_dict[next_item_index]['summary'],'date':row_dict[next_item_index]['date'],'category':row_dict[next_item_index]['category'],'link':row_dict[next_item_index]['link']})

@app.route('/api/next_previous_news',methods=['GET','POST'])
def get_next_previous_news():
    
        change_news = request.json["dest"]
        if change_news == 'Next News':
            next_item_index += 1
            return jsonify({'error':0,'title':row_dict[next_item_index]['title'],'summary':row_dict[next_item_index]['summary'],'date':row_dict[next_item_index]['date'],'category':row_dict[next_item_index]['category'],'link':row_dict[next_item_index]['link']})
        if change_news == 'Previous News':
            next_item_index -= 1
            return jsonify({'error':0,'title':row_dict[next_item_index]['title'],'summary':row_dict[next_item_index]['summary'],'date':row_dict[next_item_index]['date'],'category':row_dict[next_item_index]['category'],'link':row_dict[next_item_index]['link']})

@app.route('/Entertainment')
def scrapped_news_entertainment():
    con = sql.connect('database_scrapy.db')
    con.row_factory = sql.Row
    
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM nepali_news WHERE category = ?",["ENTERTAINMENT"])
    except sql.Error as er:
        print(er)
        
    
    rows = cur.fetchall()
    return render_template("Entertainment.html",rows = rows)
@app.route('/Business')
def scrapped_news_business():
    con = sql.connect('database_scrapy.db')
    con.row_factory = sql.Row
    
    cur = con.cursor()
    try:    
        cur.execute("SELECT * FROM nepali_news WHERE category =?", ["BUSINESS"])
    except sql.Error as er:
        print(er)
    
    rows = cur.fetchall()
    return render_template("Business.html",rows = rows)
@app.route('/Politics/<int:offset>')
def scrapped_news_politics(offset):
    conn = sql.connect('database_scrapy.db')
    c = conn.cursor()
    c.execute('SELECT * FROM nepali_news LIMIT 1 OFFSET ?', (offset,))
    data = c.fetchone()
    conn.close()
    return render_template("Politics.html",data= jsonify(data))
''' con = sql.connect('database_scrapy.db')
    con.row_factory = sql.Row1
    
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM nepali_news WHERE category = ?",["POLITICS"])
    except sql.Error as er:
        print(er)
    
    rows = cur.fetchall()
    return render_template("Politics.html",rows = rows)'''
   

@app.route('/Tech')
def scrapped_news_tech():
    con = sql.connect('database_scrapy.db')
    con.row_factory = sql.Row
    
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM nepali_news WHERE category = ?", ["TECH"])
    except sql.Error as er:
        print(er)
    rows = cur.fetchall()
    return render_template("Entertainment.html",rows = rows)
@app.route('/Sport')
def scrapped_news_sport():
    con = sql.connect('database_scrapy.db')
    con.row_factory = sql.Row
    
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM nepali_news WHERE category = ?", ["SPORT"])
    except sql.Error as er:
        print(er)
    
    rows = cur.fetchall()
    return render_template("Sport.html",rows = rows)

if __name__=='__main__':
    app.run(debug=True)