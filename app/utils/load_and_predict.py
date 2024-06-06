import pickle

# Load the model and vectorizer
with open('/app/models/logistic_regression_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('/app/models/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

def predict_sentiment(text):
    text_tfidf = vectorizer.transform([text])
    prediction = model.predict(text_tfidf)
    return prediction[0]

def plot_word_cloud(data, sentiment):
    from wordcloud import WordCloud, STOPWORDS
    import matplotlib.pyplot as plt
    import io
    import base64

    corpus = data[data['Sentiment'] == sentiment]['Text'].str.cat(sep=' ')
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white').generate(corpus)

    buffer = io.BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str
