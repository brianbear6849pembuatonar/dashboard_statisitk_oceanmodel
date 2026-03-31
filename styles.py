import streamlit as st
#Pengaturan style bentuk web
def inject_css():
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa; }
        .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .stButton>button { border-radius: 20px; transition: 0.3s; }
        .stButton>button:hover { background-color: #007bff; color: white; }
        </style>
    """, unsafe_allow_html=True)