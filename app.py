import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# ==========================================
# GOOGLE SHEETS CONNECTION
# ==========================================

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json',
    scope
)

client = gspread.authorize(creds)

sheet = client.open('Chore Tracker').sheet1

# ==========================================
# STREAMLIT PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title='⚡ COLTON DAILY CHORES ⚡',
    layout='centered'
)

# ==========================================
# CUSTOM TRON CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #050816;
        color: #00e5ff;
    }

    .main {
        background-color: #050816;
    }

    .title {
        font-size: 54px;
        font-weight: 900;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
        color: #00e5ff;
        text-shadow:
            0 0 5px #00e5ff,
            0 0 10px #00e5ff,
            0 0 20px #00e5ff,
            0 0 40px #0088ff;
        letter-spacing: 3px;
        font-family: 'Orbitron', sans-serif;
    }

    .date {
        font-size: 28px;
        color: #7df9ff;
        text-align: center;
        margin-bottom: 40px;
        text-shadow:
    st.info('No chore data found yet.')