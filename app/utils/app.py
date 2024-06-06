import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from load_and_predict import predict_sentiment, plot_word_cloud
import warnings

warnings.filterwarnings('ignore')

@st.cache_data
def load_data():
    data = pd.read_csv('/data/sentiment-data.csv')
    data.columns = ['Text', 'Sentiment', 'Source', 'Date/Time', 'User ID', 'Location', 'Confidence Score']
    data.dropna(inplace=True)
    data[['Date', 'Time']] = data['Date/Time'].str.strip().str.split(' ', expand=True)
    data.drop(columns=['Date/Time'], inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S').dt.time
    data['Sentiment'] = data['Sentiment'].str.strip().str.lower()
    return data

data = load_data()

st.title("Sentiment Analysis Dashboard")

st.header("Data Overview")
st.write(data.head(10))

st.header("Sentiment Distribution")
fig, ax = plt.subplots()
sns.countplot(x='Sentiment', data=data, palette=['green', 'red'], ax=ax)
st.pyplot(fig)

st.header("Model Evaluation")
X = data['Text']
y = data['Sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
matrix = confusion_matrix(y_test, y_pred)

st.write(f"Accuracy: {accuracy}")
st.text(f"Classification Report:\n{report}")
st.text(f"Confusion Matrix:\n{matrix}")

st.header("Predict Sentiment")
text_input = st.text_input("Enter text to predict sentiment")

if st.button("Predict Sentiment"):
    prediction = predict_sentiment(text_input)
    st.write(f'The sentiment for the text is: {prediction}')

st.header("Word Cloud")
sentiment = st.selectbox("Select Sentiment for Word Cloud", ['positive', 'negative'])
if st.button("Generate Word Cloud"):
    wordcloud_img = plot_word_cloud(data, sentiment)
    st.image(wordcloud_img, use_column_width=True)
