import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
from collections import defaultdict
from wordcloud import WordCloud, STOPWORDS
import string
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load the model and vectorizer
@st.cache_resource
def load_model_and_vectorizer():
    with open('models/logistic_regression_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    with open('models/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    
    return model, vectorizer

model, vectorizer = load_model_and_vectorizer()

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('../data/sentiment-data.csv')
    data.columns = ['Text', 'Sentiment', 'Source', 'Date/Time', 'User ID', 'Location', 'Confidence Score']
    data.dropna(inplace=True)
    data[['Date', 'Time']] = data['Date/Time'].str.strip().str.split(' ', expand=True)
    data.drop(columns=['Date/Time'], inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S').dt.time
    data['Sentiment'] = data['Sentiment'].str.strip().str.lower()
    return data

data = load_data()

# Sidebar configuration
st.sidebar.title("Sentiment Analysis Dashboard")
st.sidebar.markdown("Analyze sentiment of textual data using various machine learning models.")
st.sidebar.markdown("---")

# Main Page
st.title("Sentiment Analysis Dashboard")

# Display data
st.header("Data Overview")
st.write(data.head(10))

# Sentiment Distribution
st.header("Sentiment Distribution")
fig, ax = plt.subplots()
sns.countplot(x='Sentiment', data=data, palette=['green', 'red'], ax=ax)
st.pyplot(fig)

# Model Training and Evaluation
st.header("Model Training and Evaluation")
X = data['Text']
y = data['Sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Evaluate the model
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
matrix = confusion_matrix(y_test, y_pred)

st.write(f"Accuracy: {accuracy}")
st.text(f"Classification Report:\n{report}")
st.text(f"Confusion Matrix:\n{matrix}")

# Prediction
st.header("Predict Sentiment")
text_input = st.text_area("Enter text to predict sentiment")

if st.button("Predict Sentiment"):
    if text_input:
        text_tfidf = vectorizer.transform([text_input])
        prediction = model.predict(text_tfidf)
        st.write(f'The sentiment for the text is: **{prediction[0].capitalize()}**')
    else:
        st.error("Please enter text to predict sentiment")

# Word Cloud
st.header("Word Cloud")
sentiment = st.selectbox("Select Sentiment for Word Cloud", ['positive', 'negative'])

def plot_word_cloud(sentiment):
    corpus = data[data['Sentiment'] == sentiment]['Text'].str.cat(sep=' ')
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white').generate(corpus)
    return wordcloud

if st.button("Generate Word Cloud"):
    wordcloud = plot_word_cloud(sentiment)
    fig, ax = plt.subplots()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud for {sentiment.capitalize()} Sentiment')
    st.pyplot(fig)
