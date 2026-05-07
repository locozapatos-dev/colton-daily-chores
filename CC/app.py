import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
from io import StringIO

# ==========================================
# GOOGLE SHEET CONFIG
# ==========================================

SHEET_ID = "1NLgLsiF_93aELUiGbptvMNZs8BunWc0L0K_gmCTBy68"

CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Colton Daily Chores",
    layout="wide",
    page_icon="✓"
)

# ==========================================
# CLEAN PROFESSIONAL CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top, #0b1d3a 0%, #020617 55%);
    color: #ffffff;
}

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 64px;
    font-weight: 700;
    letter-spacing: 4px;
    margin-top: 10px;
    margin-bottom: 0px;
    color: #f8fafc;
}

.main-title span {
    color: #22d3ee;
}

/* DATE */

.date-text {
    text-align: center;
    font-size: 28px;
    color: #67e8f9;
    margin-bottom: 40px;
}

/* SECTION CARDS */

.dashboard-card {
    background: rgba(5, 15, 35, 0.95);
    border: 1px solid rgba(34, 211, 238, 0.25);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 0 30px rgba(0,0,0,0.35);
}

/* SECTION HEADERS */

.section-header {
    font-size: 34px;
    font-weight: 700;
    color: #22d3ee;
    margin-bottom: 25px;
}

/* TABLE */

table {
    width: 100%;
    border-collapse: collapse;
}

thead tr {
    background-color: rgba(15, 23, 42, 1);
}

thead th {
    padding: 14px;
    color: #22d3ee;
    border: 1px solid rgba(255,255,255,0.08);
    text-align: left;
    font-size: 20px;
}

tbody td {
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 22px;
}

/* KPI BOXES */

.kpi-box {
    background: rgba(10, 25, 50, 0.95);
    border: 1px solid rgba(34, 211, 238, 0.25);
    border-radius: 14px;
    padding: 25px;
    text-align: center;
    margin-bottom: 20px;
    height: 180px;
}

.kpi-title {
    color: #67e8f9;
    font-size: 24px;
    margin-bottom: 20px;
}

.kpi-number {
    color: #22d3ee;
    font-size: 64px;
    font-weight: 700;
    line-height: 1;
}

.kpi-sub {
    margin-top: 10px;
    color: #cbd5e1;
    font-size: 22px;
}

/* BUTTON */

.stButton > button {
    width: 100%;
    background: transparent;
    color: #22d3ee;
    border: 2px solid #22d3ee;
    border-radius: 10px;
    padding: 16px;
    font-size: 24px;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #22d3ee;
    color: #020617;
}

/* CHECKBOXES */

.stCheckbox label {
    color: #ffffff !important;
    font-size: 22px !important;
}

/* DATAFRAME */

div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* HIDE STREAMLIT MENU */

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

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
        "Drink Smoothie",
        "Golf Practice"
    ])

# ==========================================
# DATE
# ==========================================

current_date = datetime.now()

today_string = current_date.strftime("%Y-%m-%d")

try:
    pretty_date = current_date.strftime("%A, %B %-d, %Y")
except:
    pretty_date = current_date.strftime("%A, %B %#d, %Y")

# ==========================================
# TITLE
# ==========================================

st.markdown(
    """
    <div class="main-title">
        COLTON DAILY <span>CHORES</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="date-text">{pretty_date}</div>',
    unsafe_allow_html=True
)

# ==========================================
# CHORES
# ==========================================

chores = [
    "Clean Skimmer",
    "Strength Training",
    "Piano Practice",
    "Drink Smoothie",
    "Golf Practice"
]

# ==========================================
# FIND TODAY'S DATA
# ==========================================

existing_row = None

if not df.empty:

    matches = df[df["Date"] == today_string]

    if not matches.empty:
        existing_row = matches.iloc[0]

# ==========================================
# TOP LAYOUT
# ==========================================

left_col, right_col = st.columns([2.2, 1])

# ==========================================
# LEFT PANEL
# ==========================================

with left_col:

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-header">TODAY\'S CHECKLIST</div>',
        unsafe_allow_html=True
    )

    chore_values = {}

    for chore in chores:

        default_value = False

        if existing_row is not None:
            default_value = bool(existing_row[chore])

        checked = st.checkbox(chore, value=default_value)

        chore_values[chore] = checked

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("SAVE CHORES"):

        st.success(
            "Dashboard currently deployed in read-only demo mode."
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# RIGHT PANEL
# ==========================================

with right_col:

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-header">WEEKLY SUMMARY</div>',
        unsafe_allow_html=True
    )

    total_completed = 0
    total_missed = 0

    if not df.empty:

        df["Date"] = pd.to_datetime(df["Date"])

        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        weekly_df = df[
            (df["Date"] >= pd.Timestamp(start_of_week.date())) &
            (df["Date"] <= pd.Timestamp(end_of_week.date()))
        ]

        for chore in chores:

            completed = int(weekly_df[chore].sum())

            missed = len(weekly_df) - completed

            total_completed += completed
            total_missed += missed

    kpi1, kpi2 = st.columns(2)

    with kpi1:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">TOTAL COMPLETED</div>
            <div class="kpi-number">{total_completed}</div>
            <div class="kpi-sub">chores</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">TOTAL MISSED</div>
            <div class="kpi-number">{total_missed}</div>
            <div class="kpi-sub">chores</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# WEEKLY REPORT
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-header">WEEKLY PERFORMANCE REPORT</div>',
    unsafe_allow_html=True
)

report_data = []

if not df.empty:

    for chore in chores:

        completed = int(weekly_df[chore].sum())

        missed = len(weekly_df) - completed

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

st.dataframe(
    report_df,
    use_container_width=True,
    hide_index=True
)

st.markdown('</div>', unsafe_allow_html=True)