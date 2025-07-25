from flask import Flask, request, jsonify, render_template
from naive_bayes_inference.naive_bayes_model import detect_spam_naive_bayes
from LSTM_inference.lstm_model import detect_spam_lstm
from LLM_inteference.llm_model import llm_model
from random_tree_inference.random_tree import detect_spam_random_forest
import traceback
import langdetect



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('website.html')

@app.route('/detect-spam', methods=['POST'])
def detect_spam():
    try:
        data = request.get_json()
        text = data.get('text')
        model_type = data.get('method') 
        
        if model_type == 'Naive Bayes':
            lang = langdetect.detect(text)
            if lang != 'en':
                return jsonify({'message': "Language not supported."})
            return jsonify(detect_spam_naive_bayes(text))
        elif model_type == 'Random Forest':
            lang = langdetect.detect(text)
            if lang != 'en':
                return jsonify({'message': "Language not supported."})
            return jsonify(detect_spam_random_forest(text))
            
        elif model_type == 'LSTM':
            lang = langdetect.detect(text)
            if lang != 'en':
                return jsonify({'message': "Language not supported."})
            return jsonify(detect_spam_lstm(text))
        elif model_type == 'LLM':
            return jsonify(llm_model(text))
        else:
            return jsonify({'message': 'Model not supported.'})
    except:
        print("Exception in Main: ", traceback.format_exc())
        return jsonify({'message': f'API error { traceback.format_exc()}'})

if __name__ == '__main__':
    app.run(debug=True)
