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

# Load the dataset
data_path = os.path.join('data', 'sentiment-data.csv')
data = pd.read_csv(data_path)

# Set up the Streamlit app layout
st.set_page_config(page_title="AI Model Dashboard", layout="wide")
st.title("AI Model Dashboard")
st.write("Welcome to the AI Model Dashboard. Use this app to evaluate your AI model.")

# Display the data
st.header("Dataset")
st.write(data.head())

# Interactive data annotation
st.header("Annotate Data")
data['Issue'] = [False] * len(data)
data['Category'] = [""] * len(data)

annotated_data = st.data_editor(
    data,
    column_config={
        "Text": st.column_config.TextColumn(width="medium", disabled=True),
        "Sentiment": st.column_config.TextColumn(width="medium", disabled=True),
        "Issue": st.column_config.CheckboxColumn("Mark as Issue", default=False),
        "Category": st.column_config.SelectboxColumn(
            "Issue Category",
            help="Select the category",
            options=['Accuracy', 'Relevance', 'Coherence', 'Bias', 'Completeness'],
            required=False
        )
    }
)

# Filter and visualize annotated data
st.header("Annotated Data")
issue_filter = st.selectbox("Filter by Issue", options=[True, False])
category_filter = st.selectbox(
    "Filter by Category",
    options=annotated_data[annotated_data['Issue'] == issue_filter]['Category'].unique()
)

filtered_data = annotated_data[(annotated_data['Issue'] == issue_filter) & (annotated_data['Category'] == category_filter)]
st.write(filtered_data)

# Display metrics
st.header("Metrics")
issue_count = len(annotated_data[annotated_data['Issue'] == True])
total_count = len(annotated_data)
issue_percentage = f"{issue_count / total_count * 100:.2f}%"

col1, col2 = st.columns(2)
with col1:
    st.metric("Number of Issues", issue_count)
with col2:
    st.metric("Issue Percentage", issue_percentage)

# Bar chart for category distribution
st.header("Category Distribution")
category_distribution = annotated_data['Category'].value_counts().reset_index()
category_distribution.columns = ['Category', 'Count']
st.bar_chart(category_distribution)

# Model prediction
st.header("Model Prediction")
input_text = st.text_area("Enter text for sentiment prediction")
if st.button("Predict"):
    if input_text:
        input_tfidf = vectorizer.transform([input_text])
        prediction = model.predict(input_tfidf)
        st.write(f"Predicted Sentiment: {prediction[0]}")
    else:
        st.write("Please enter some text for prediction")

# Footer with link to Shuna Academy
st.markdown("[Go to Shuna Academy to access the website](https://your-shuna-academy-link.com)")

# Custom CSS
st.markdown(
    """
    <style>
    .main {background-color: #f0f2f6;}
    .stButton>button {background-color: #0072c3; color: white; border-radius: 10px; padding: 0.5em 1em;}
    .stButton>button:hover {background-color: #005bb5;}
    </style>
    """,
    unsafe_allow_html=True
)

# Include external JS for modal functionality
st.markdown(
    """
    <script>
    document.addEventListener('DOMContentLoaded', function () {
        var modal = document.getElementById("contact-us-modal");
        var btn = document.getElementById("contact-btn");
        var span = document.getElementsByClassName("close-button")[0];

        btn.onclick = function () {
            modal.style.display = "block";
        }

        span.onclick = function () {
            modal.style.display = "none";
        }

        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)
