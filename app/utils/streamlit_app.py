import os
import subprocess
import streamlit as st

# Start the Flask server
def start_flask():
    if not os.path.isfile('app/utils/app.py'):
        raise FileNotFoundError('app.py not found')
    subprocess.Popen(["python", "app.py"])

start_flask()

st.title("AI Model Dashboard")
st.write("Go to [Shuna Academy](http://localhost:5001) to access the website.")
