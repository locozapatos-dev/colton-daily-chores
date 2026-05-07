import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
from io import StringIO

# ==========================================
# GOOGLE SHEET CSV EXPORT URL
# ==========================================

SHEET_ID = "1NLgLsiF_93aELUiGbptvMNZs8BunWc0L0K_gmCTBy68"

CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Colton Daily Chores",
    page_icon="⚡",
    layout="centered"
)

# ==========================================
# TRON CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(to bottom, #020617, #050816);
        color: #00e5ff;
    }

    .title {
        text-align: center;
        font-size: 58px;
        font-weight: 900;
        color: #00e5ff;
        margin-top: 20px;
        margin-bottom: 10px;
        letter-spacing: 3px;
        text-shadow:
            0 0 5px #00e5ff,
            0 0 10px #00e5ff,
            0 0 20px #00e5ff,
            0 0 40px #0088ff;
    }

    .date {
        text-align: center;
        font-size: 28px;
        color: #7df9ff;
        margin-bottom: 40px;
        text-shadow:
            0 0 5px #00e5ff,
            0 0 15px #00e5ff;
    }

    .stCheckbox label {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #00e5ff !important;
        text-shadow: 0 0 5px #00e5ff;
    }

    .stButton > button {
        width: 100%;
        background-color: transparent;
        color: #00e5ff;
        border: 2px solid #00e5ff;
        border-radius: 12px;
        padding: 14px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 0 15px #00e5ff;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #00e5ff;
        color: #020617;
        box-shadow: 0 0 25px #00e5ff;
    }

    .report-box {
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #00e5ff;
        background-color: rgba(0,0,0,0.4);
        box-shadow: 0 0 20px #00e5ff;
    }

    h1, h2, h3 {
        color: #00e5ff !important;
        text-shadow: 0 0 10px #00e5ff;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# LOAD GOOGLE SHEET
# ==========================================

try:
    response = requests.get(CSV_URL)

    df = pd.read_csv(StringIO(response.text))

except:
    df = pd.DataFrame(columns=[
        "Date",
        "Clean Skimmer",
        "Strength Training",
        "Piano Practice",
        "Drink Smoothie"
    ])

# ==========================================
# DATE
# ==========================================

current_date = datetime.now()

today_string = current_date.strftime("%Y-%m-%d")

try:
    pretty_date = current_date.strftime("%A %B %-d, %Y")
except:
    pretty_date = current_date.strftime("%A %B %#d, %Y")

# ==========================================
# TITLE
# ==========================================

st.markdown(
    '<div class="title">⚡ COLTON DAILY CHORES ⚡</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="date">{pretty_date}</div>',
    unsafe_allow_html=True
)

# ==========================================
# CHORES
# ==========================================

chores = [
    "Clean Skimmer",
    "Strength Training",
    "Piano Practice",
    "Drink Smoothie"
]

# ==========================================
# TODAY'S VALUES
# ==========================================

existing_row = None

if not df.empty:

    matches = df[df["Date"] == today_string]

    if not matches.empty:
        existing_row = matches.iloc[0]

# ==========================================
# CHECKBOXES
# ==========================================

st.subheader("Today's Mission Checklist")

chore_values = {}

for chore in chores:

    default_value = False

    if existing_row is not None:
        default_value = bool(existing_row[chore])

    checked = st.checkbox(chore, value=default_value)

    chore_values[chore] = checked

# ==========================================
# SAVE BUTTON
# ==========================================

if st.button("⚡ SAVE CHORES ⚡"):

    st.success(
        "⚡ Chores Updated ⚡\n\n"
        "IMPORTANT:\n"
        "This demo version reads from Google Sheets.\n\n"
        "To enable WRITEBACK syncing, the next deployment step "
        "will connect Streamlit secrets securely."
    )

# ==========================================
# WEEKLY REPORT
# ==========================================

st.markdown("---")

st.header("⚡ Weekly Performance Report ⚡")

if not df.empty:

    df["Date"] = pd.to_datetime(df["Date"])

    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    weekly_df = df[
        (df["Date"] >= pd.Timestamp(start_of_week.date())) &
        (df["Date"] <= pd.Timestamp(end_of_week.date()))
    ]

    report_data = []

    total_completed = 0
    total_missed = 0

    for chore in chores:

        completed = int(weekly_df[chore].sum())

        missed = len(weekly_df) - completed

        total_completed += completed
        total_missed += missed

        percentage = 0

        if len(weekly_df) > 0:
            percentage = round((completed / len(weekly_df)) * 100, 1)

        report_data.append({
            "Chore": chore,
            "Completed": completed,
            "Missed": missed,
            "Completion %": f"{percentage}%"
        })

    report_df = pd.DataFrame(report_data)

    st.dataframe(report_df, use_container_width=True)

    st.markdown(
        f"""
        <div class="report-box">
            <h2>⚡ Weekly Summary ⚡</h2>
            <h3>Total Completed: {total_completed}</h3>
            <h3>Total Missed: {total_missed}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info("No chore data yet.")