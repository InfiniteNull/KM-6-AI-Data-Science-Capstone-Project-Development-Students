import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from load_and_predict import predict_sentiment, plot_word_cloud
import base64
import io
import warnings
import streamlit.components.v1 as components

warnings.filterwarnings('ignore')

@st.cache_data
def load_data():
    data = pd.read_csv('../../data/sentiment-data.csv')
    data.columns = ['Text', 'Sentiment', 'Source', 'Date/Time', 'User ID', 'Location', 'Confidence Score']
    data.dropna(inplace=True)
    data[['Date', 'Time']] = data['Date/Time'].str.strip().str.split(' ', expand=True)
    data.drop(columns=['Date/Time'], inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S').dt.time
    data['Sentiment'] = data['Sentiment'].str.strip().str.lower()
    return data

data = load_data()

# Load the HTML file and display it
with open("../templates/dashboard.html", 'r', encoding='utf-8') as html_file:
    html_string = html_file.read()

components.html(html_string, height=1000)

# JavaScript communication handler
st.write(
    """
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'predict') {
            const text = event.data.text;
            const result = streamlitPredict(text);
            window.parent.postMessage({ type: 'prediction-result', result: result }, '*');
        } else if (event.data.type === 'generate-word-cloud') {
            const sentiment = event.data.sentiment;
            const result = streamlitGenerateWordCloud(sentiment);
            window.parent.postMessage({ type: 'word-cloud-result', result: result }, '*');
        }
    });

    function streamlitPredict(text) {
        return new Promise((resolve, reject) => {
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            })
            .then(response => response.json())
            .then(data => resolve(data.result))
            .catch(error => reject(error));
        });
    }

    function streamlitGenerateWordCloud(sentiment) {
        return new Promise((resolve, reject) => {
            fetch('/generate_word_cloud', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ sentiment: sentiment })
            })
            .then(response => response.json())
            .then(data => resolve(data.result))
            .catch(error => reject(error));
        });
    }
    </script>
    """,
    unsafe_allow_html=True
)

# API Endpoints for Streamlit communication
@st.cache_data
def predict_api(text):
    result = predict_sentiment(text)
    return result

@st.cache_data
def word_cloud_api(sentiment):
    result = plot_word_cloud(data, sentiment)
    return result

# Define routes
def streamlit_api():
    from flask import Flask, request, jsonify
    app = Flask(__name__)

    @app.route('/predict', methods=['POST'])
    def predict():
        text = request.json.get('text')
        result = predict_api(text)
        return jsonify(result=result)

    @app.route('/generate_word_cloud', methods=['POST'])
    def generate_word_cloud():
        sentiment = request.json.get('sentiment')
        result = word_cloud_api(sentiment)
        return jsonify(result=result)

    return app

if __name__ == "__main__":
    app = streamlit_api()
    app.run(port=8501)
