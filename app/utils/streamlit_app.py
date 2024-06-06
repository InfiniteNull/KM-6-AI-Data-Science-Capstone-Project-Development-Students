import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Load the model and vectorizer
model_path = os.path.join('app', 'models', 'logistic_regression_model.pkl')
vectorizer_path = os.path.join('app', 'models', 'tfidf_vectorizer.pkl')

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

# Page configuration
st.set_page_config(page_title="AI Model Dashboard", layout="wide")

# Title
st.title("AI Model Dashboard")
st.write("Welcome to the AI Model Dashboard. Use this app to evaluate your AI model.")

# File uploader for new data
uploaded_file = st.file_uploader("Choose a CSV file to upload new data", type="csv")

if uploaded_file:
    # Load the uploaded data
    data = pd.read_csv(uploaded_file)
else:
    # Load the default dataset
    data_path = os.path.join('data', 'sentiment-data.csv')
    data = pd.read_csv(data_path)

# Display the data
st.header("Dataset")
st.write(data.head())

# Predict sentiment using the loaded model
def predict_sentiment(text):
    text_tfidf = vectorizer.transform([text])
    prediction = model.predict(text_tfidf)
    return prediction[0]

# Add predictions to the data
data['Predicted Sentiment'] = data['Text'].apply(predict_sentiment)

# Display the data with predictions
st.header("Data with Predictions")
st.write(data)

# Sidebar for filtering predictions
st.sidebar.header("Filter Predictions")
sentiment_filter = st.sidebar.selectbox("Select Sentiment", options=data['Predicted Sentiment'].unique())

filtered_data = data[data['Predicted Sentiment'] == sentiment_filter]
st.write(filtered_data)

# Display metrics
st.header("Metrics")
issue_count = len(data[data['Predicted Sentiment'] == 'negative'])
total_count = len(data)
issue_percentage = f"{issue_count / total_count * 100:.2f}%"

col1, col2 = st.columns(2)
with col1:
    st.metric("Number of Negative Sentiments", issue_count)
with col2:
    st.metric("Percentage of Negative Sentiments", issue_percentage)

# Bar chart for sentiment distribution
st.header("Sentiment Distribution")
sentiment_distribution = data['Predicted Sentiment'].value_counts().reset_index()
sentiment_distribution.columns = ['Sentiment', 'Count']
st.bar_chart(sentiment_distribution)

# Text input for individual prediction
st.header("Predict Sentiment for New Text")
input_text = st.text_area("Enter text for sentiment prediction")
if st.button("Predict"):
    if input_text:
        prediction = predict_sentiment(input_text)
        st.write(f"Predicted Sentiment: {prediction}")
    else:
        st.write("Please enter some text for prediction")
