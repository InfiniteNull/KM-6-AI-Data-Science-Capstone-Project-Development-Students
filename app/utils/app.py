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
            const result = predictSentiment(text);
            window.parent.postMessage({ type: 'prediction-result', result: result }, '*');
        } else if (event.data.type === 'generate-word-cloud') {
            const sentiment = event.data.sentiment;
            const result = generateWordCloud(sentiment);
            window.parent.postMessage({ type: 'word-cloud-result', result: result }, '*');
        }
    });

    function predictSentiment(text) {
        return streamlit_predict(text);
    }

    function generateWordCloud(sentiment) {
        return streamlit_generate_word_cloud(sentiment);
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Functions for predictions and word cloud generation
def streamlit_predict(text):
    return predict_sentiment(text)

def streamlit_generate_word_cloud(sentiment):
    return plot_word_cloud(data, sentiment)
