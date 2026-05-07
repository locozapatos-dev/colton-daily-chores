import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
from io import StringIO

# =====================================================
# GOOGLE SHEET CONFIG
# =====================================================

SHEET_ID = "1NLgLsiF_93aELUiGbptvMNZs8BunWc0L0K_gmCTBy68"

CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Colton Daily Chores",
    page_icon="✓",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* BACKGROUND */

.stApp {
    background:
        radial-gradient(circle at top,
        #16325f 0%,
        #0c1f3f 35%,
        #08152d 70%,
        #06101f 100%);
    color: white;
}

/* REMOVE STREAMLIT DEFAULTS */

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* MAIN CONTAINER */

.block-container {
    padding-top: 2rem;
    max-width: 96%;
}

/* TITLE */

.main-title {
    text-align: center;
    font-size: 82px;
    font-weight: 800;
    letter-spacing: 2px;
    color: white;
    margin-bottom: 0px;
}

.main-title span {
    color: #22d3ee;
}

/* DATE */

.date-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 30px;
}

.date-line {
    height: 2px;
    width: 170px;
    background: rgba(34,211,238,0.65);
}

.date-text {
    font-size: 28px;
    color: #67e8f9;
    font-weight: 600;
}

/* PANELS */

.panel {
    background: rgba(8, 18, 40, 0.92);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 18px;
    padding: 18px;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.02),
        0 10px 40px rgba(0,0,0,0.35);
}

/* SECTION TITLES */

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #22d3ee;
    margin-bottom: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* TABLE */

.custom-table {
    width: 100%;
    border-collapse: collapse;
    overflow: hidden;
    border-radius: 12px;
    border: 1px solid rgba(103,232,249,0.25);
}

.custom-table thead tr {
    background: rgba(15, 23, 42, 0.95);
}

.custom-table th {
    padding: 18px;
    border: 1px solid rgba(103,232,249,0.18);
    color: #22d3ee;
    font-size: 22px;
    font-weight: 700;
    text-align: left;
}

.custom-table td {
    padding: 18px;
    border: 1px solid rgba(103,232,249,0.14);
    font-size: 22px;
    color: white;
}

/* CHECKBOX LABELS */

.stCheckbox label {
    color: white !important;
    font-size: 28px !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* CHECKBOX SIZE */

.stCheckbox input {
    transform: scale(1.6);
}

/* BUTTON */

.stButton > button {
    width: 100%;
    background: transparent;
    color: #22d3ee;
    border: 2px solid #22d3ee;
    border-radius: 10px;
    padding: 18px;
    font-size: 28px;
    font-weight: 700;
    transition: 0.3s;
    margin-top: 10px;
}

.stButton > button:hover {
    background: #22d3ee;
    color: #08152d;
}

/* KPI BOX */

.kpi-box {
    background: rgba(13, 29, 58, 0.98);
    border: 1px solid rgba(103,232,249,0.25);
    border-radius: 14px;
    padding: 26px;
    text-align: center;
    min-height: 180px;
}

.kpi-title {
    color: #67e8f9;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 20px;
}

.kpi-number {
    font-size: 72px;
    font-weight: 800;
    color: #22d3ee;
    line-height: 1;
}

.kpi-sub {
    color: white;
    font-size: 22px;
    margin-top: 12px;
}

/* REPORT TABLE */

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(103,232,249,0.25);
    border-radius: 12px;
    overflow: hidden;
}

/* FOOTER */

.footer-note {
    text-align: center;
    color: #67e8f9;
    font-size: 20px;
    margin-top: 22px;
    opacity: 0.9;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD GOOGLE SHEET
# =====================================================

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

# =====================================================
# DATE
# =====================================================

current_date = datetime.now()

today_string = current_date.strftime("%Y-%m-%d")

try:
    pretty_date = current_date.strftime("%A, %B %-d, %Y")
except:
    pretty_date = current_date.strftime("%A, %B %#d, %Y")

# =====================================================
# TITLE
# =====================================================

st.markdown(
    """
    <div class="main-title">
        COLTON DAILY <span>CHORES</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="date-container">
        <div class="date-line"></div>
        <div class="date-text">{pretty_date}</div>
        <div class="date-line"></div>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# CHORES
# =====================================================

chores = [
    "Clean Skimmer",
    "Strength Training",
    "Piano Practice",
    "Drink Smoothie",
    "Golf Practice"
]

# =====================================================
# FIND TODAY DATA
# =====================================================

existing_row = None

if not df.empty:

    matches = df[df["Date"] == today_string]

    if not matches.empty:
        existing_row = matches.iloc[0]

# =====================================================
# LAYOUT
# =====================================================

left_col, right_col = st.columns([2.2, 1])

# =====================================================
# LEFT PANEL
# =====================================================

with left_col:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">TODAY\'S CHECKLIST</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <table class="custom-table">
        <thead>
            <tr>
                <th>CHORE</th>
                <th style="width:200px;text-align:center;">COMPLETED</th>
            </tr>
        </thead>
    </table>
    """, unsafe_allow_html=True)

    chore_values = {}

    for chore in chores:

        default_value = False

        if existing_row is not None:
            default_value = bool(existing_row[chore])

        col1, col2 = st.columns([5, 1])

        with col1:
            checked = st.checkbox(chore, value=default_value)

        with col2:
            st.write("")

        chore_values[chore] = checked

    if st.button("SAVE CHORES"):

        st.success(
            "Dashboard currently deployed in read-only demo mode."
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# RIGHT PANEL
# =====================================================

with right_col:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">WEEKLY SUMMARY</div>',
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

    else:

        start_of_week = current_date
        end_of_week = current_date

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

    st.markdown("<br>", unsafe_allow_html=True)

    week1, week2 = st.columns(2)

    with week1:

        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">WEEK START</div>
            <div style="font-size:18px;font-weight:700;color:white;margin-top:30px;">
                {start_of_week.strftime("%a, %b %d, %Y")}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with week2:

        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">WEEK END</div>
            <div style="font-size:18px;font-weight:700;color:white;margin-top:30px;">
                {end_of_week.strftime("%a, %b %d, %Y")}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# WEEKLY REPORT
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">WEEKLY PERFORMANCE REPORT</div>',
    unsafe_allow_html=True
)

report_data = []

if not df.empty:

    for chore in chores:

        completed = int(weekly_df[chore].sum())

        missed = len(weekly_df) - completed

        percentage = 0

        if len(weekly_df) > 0:
            percentage = round(
                (completed / len(weekly_df)) * 100,
                1
            )

        report_data.append({
            "Chore": chore,
            "Completed": completed,
            "Missed": missed,
            "Completion %": f"{percentage}%"
        })

    total_completed_report = sum(
        row["Completed"] for row in report_data
    )

    total_missed_report = sum(
        row["Missed"] for row in report_data
    )

    overall_percentage = 0

    total_possible = total_completed_report + total_missed_report

    if total_possible > 0:

        overall_percentage = round(
            (total_completed_report / total_possible) * 100,
            1
        )

    report_data.append({
        "Chore": "TOTAL",
        "Completed": total_completed_report,
        "Missed": total_missed_report,
        "Completion %": f"{overall_percentage}%"
    })

report_df = pd.DataFrame(report_data)

st.dataframe(
    report_df,
    use_container_width=True,
    hide_index=True
)

st.markdown(
    """
    <div class="footer-note">
        Stay consistent. Small daily actions lead to big results.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)