from flask import Flask, render_template, request, redirect, url_for
import os
import streamlit as st

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add your login logic here
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        # Add your registration logic here
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == "__main__":
    # Set Flask's run method
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
