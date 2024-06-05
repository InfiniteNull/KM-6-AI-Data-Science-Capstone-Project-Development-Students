import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from nltk.corpus import stopwords
from collections import defaultdict
from wordcloud import WordCloud, STOPWORDS
import string
import warnings

warnings.filterwarnings('ignore')

st.title("Sentiment Analysis Dashboard")

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
st.header("Data Overview")
st.write(data.head(10))

st.header("Sentiment Distribution")
fig, ax = plt.subplots()
sns.countplot(x='Sentiment', data=data, palette=['green', 'red'], ax=ax)
st.pyplot(fig)

st.header("Model Training and Evaluation")
X = data['Text']
y = data['Sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "MLP Classifier": MLPClassifier(max_iter=1000, random_state=42)
}

def train_and_evaluate_model(model_name):
    model = models[model_name]
    model.fit(X_train_tfidf, y_train)
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    return accuracy, report, matrix

selected_model = st.selectbox("Select a model", list(models.keys()))

if st.button("Train and Evaluate"):
    accuracy, report, matrix = train_and_evaluate_model(selected_model)
    st.write(f"Accuracy: {accuracy}")
    st.text(f"Classification Report:\n{report}")
    st.text(f"Confusion Matrix:\n{matrix}")

st.header("Predict Sentiment")
text_input = st.text_input("Enter text to predict sentiment")

if st.button("Predict Sentiment"):
    model = models[selected_model]
    text_tfidf = vectorizer.transform([text_input])
    prediction = model.predict(text_tfidf)
    st.write(f'The sentiment for the text is: {prediction[0]}')

def plot_word_cloud(sentiment):
    corpus = data[data['Sentiment'] == sentiment]['Text'].str.cat(sep=' ')
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white').generate(corpus)
    return wordcloud

st.header("Word Cloud")
sentiment = st.selectbox("Select Sentiment for Word Cloud", ['positive', 'negative'])
if st.button("Generate Word Cloud"):
    wordcloud = plot_word_cloud(sentiment)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()
