from flask import Flask, request, render_template,jsonify
from base.Classification import Classify
from base.Summarization import Summarize
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/data')
def home_page():
    return {"Hello":"World"}


@app.route('/api/form', methods=['POST'])
def handle_form_data():
    form_data = request.json
    news = str(form_data['news'])
    summarization_count = int(form_data['count']) -1

    
    if summarization_count == '':
        summarized_news = Summarize(news).sentence_number(10)
    else:
        summarized_news = Summarize(news).sentence_number(int(summarization_count))
    
    summarized_news = summarized_news
    prediction ,confidence = Classify(news).Predict_News()
    print(confidence)
    return jsonify({'text':news,'summarized':summarized_news,'count':summarization_count,'prediction':prediction})
    
   


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
    return render_template('Form.html',text = news, summarized = summarized_news,summarization_count = summarization_count,prediction = prediction,confidence = confidence)


if __name__=='__main__':
    app.run(debug=True)