from flask import Flask, request, render_template,jsonify
from base.Classification import Classify
from base.Summarization import Summarize
from base.Scrape import Scrape_Nepali_News
from flask_cors import CORS
import json
import sqlite3  as sql
app = Flask(__name__)
CORS(app)
category_class = ['business', 'entertainment', 'politics', 'sport', 'tech']
@app.route('/data')
def home_page():
    return {"Hello":"World"}


@app.route('/api/form', methods=['POST'])
def handle_form_data():
    form_data = request.json
    news = str(form_data['news'])
    summarization_count = int(form_data['count']) -1
    confidence_dict = {}
    
    if summarization_count == '':
        summarized_news = Summarize(news).sentence_number(10)
    else:
        summarized_news = Summarize(news).sentence_number(int(summarization_count))
    
    summarized_news = summarized_news
    prediction ,confidence = Classify(news).Predict_News()
    confidence_dict = {category_class:confidence for (category_class,confidence) in zip(category_class,confidence)}
    print(confidence_dict)
    return jsonify({'text':news,'summarized':summarized_news,'count':summarization_count,'prediction':prediction,'confidence':confidence_dict})
    
   


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
        summarized_news = Summarize(news).sentence_number(11)
    else:
        summarized_news = Summarize(news).sentence_number(int(summarization_count))
    
    summarized_news = summarized_news
    prediction ,confidence = Classify(news).Predict_News()
    print(max(confidence))
    return render_template('Form.html',text = news, summarized = summarized_news,summarization_count = summarization_count,prediction = prediction,confidence = confidence)

@app.route('/scrape')
def scrape_window():
    Scrape_Nepali_News().scrape_nepali_news()
    return render_template('index.html')

@app.route('/scraped_news')
def scrapped_news():
    con = sql.connect('database_scrapy.db')
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * FROM nepali_news ORDER BY confidence DESC LIMIT 1")
    
    rows = cur.fetchall()
    return render_template("ViewScrapped.html",rows = rows)

@app.route('/dynamic_fetch',methods=['GET', 'POST'])
def fetch_scrapped_news():
    con = sql.connect('database_scrapy.db')
    cur = con.cursor()
    next_item_index = int(request.form.get('next_item_index', 0))
    con.row_factory = sql.Row
   #print(con.row_factory)
    index = 0
    cur.execute("SELECT * FROM nepali_news ORDER BY confidence DESC ")
    fetch_row = cur.fetchall()
    row_dict = {}
        
    #print("Total records are",len(fetch_row))
    
    for row in fetch_row:
        row_dict[index] = {'primary_number':row[0],'title':row[1],'news':row[2],'link':row[3],'source':row[4],'category':row[5],'date':row[6],'confidence':row[7]}
        index += 1
    #print(row_dict)
    con.close()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Next':
            return render_template('fetch_single.html',data=row_dict[next_item_index],next_item_index=next_item_index+1)
        else:
            sentence_count = int(request.form['summarization_count'])
            row_dict[next_item_index]['news']=Summarize(row_dict[next_item_index]['news']).sentence_number(sentence_count)
            return render_template('fetch_single.html',data=row_dict[next_item_index],next_item_index=next_item_index)
    return render_template('fetch_single.html',data=row_dict[0])
    
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