import streamlit as st
import pandas as pd
import os

# Fungsi untuk membaca file HTML
def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
    return html

# Fungsi utama untuk menjalankan aplikasi Streamlit
def main():
    st.title("AI Model Dashboard")

    # Tab untuk memilih halaman
    tab = st.selectbox("Pilih Halaman", ["Home", "Login", "Register"])

    # Menampilkan halaman HTML yang dipilih
    if tab == "Home":
        st.markdown(read_html('app/templates/index.html'), unsafe_allow_html=True)
    elif tab == "Login":
        st.markdown(read_html('app/templates/login.html'), unsafe_allow_html=True)
    elif tab == "Register":
        st.markdown(read_html('app/templates/register.html'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
