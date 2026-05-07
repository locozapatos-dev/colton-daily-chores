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

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at top, #16325f 0%, #0c1f3f 35%, #08152d 70%, #06101f 100%);
    color: white;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.block-container { padding-top: 2rem; max-width: 96%; }

/* TITLE */
.main-title {
    text-align: center;
    font-size: 76px;
    font-weight: 800;
    letter-spacing: 2px;
    color: white;
    margin-bottom: 0;
}
.main-title span { color: #22d3ee; }

/* DATE */
.date-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 26px;
}
.date-line { height: 2px; width: 150px; background: rgba(34,211,238,0.65); }
.date-text { font-size: 24px; color: #67e8f9; font-weight: 600; }

/* PANEL */
.panel {
    background: rgba(8, 18, 40, 0.92);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 18px;
    padding: 20px 22px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02), 0 10px 40px rgba(0,0,0,0.35);
}

/* SECTION TITLE */
.section-title {
    font-size: 16px;
    font-weight: 700;
    color: #22d3ee;
    margin-bottom: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* DATE PICKER */
.stDateInput > div > div > input {
    background: rgba(13, 29, 58, 0.98) !important;
    color: #22d3ee !important;
    border: 1px solid rgba(103,232,249,0.45) !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    text-align: center !important;
    cursor: pointer !important;
}
.stDateInput > div > div > input:focus {
    border-color: #22d3ee !important;
    box-shadow: 0 0 0 2px rgba(34,211,238,0.2) !important;
}

/* CHECKLIST TABLE HEADER */
.cl-header {
    display: flex;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(103,232,249,0.25);
    border-radius: 8px 8px 0 0;
}
.cl-header-chore {
    flex: 1;
    padding: 10px 14px;
    color: #22d3ee;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-right: 1px solid rgba(103,232,249,0.18);
}
.cl-header-done {
    width: 120px;
    padding: 10px 14px;
    color: #22d3ee;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    text-align: center;
}

/* CHECKLIST ROWS WRAPPER */
.cl-rows {
    border-left: 1px solid rgba(103,232,249,0.25);
    border-right: 1px solid rgba(103,232,249,0.25);
    border-bottom: 1px solid rgba(103,232,249,0.25);
    border-radius: 0 0 8px 8px;
}

/* CHECKBOX LABEL */
.stCheckbox label {
    color: white !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    gap: 10px !important;
    align-items: center !important;
}

/* CUSTOM SQUARE CHECKBOX */
.stCheckbox input[type="checkbox"] {
    appearance: none !important;
    -webkit-appearance: none !important;
    width: 20px !important;
    height: 20px !important;
    min-width: 20px !important;
    border: 2px solid rgba(103,232,249,0.55) !important;
    border-radius: 3px !important;
    background: transparent !important;
    cursor: pointer !important;
    margin-top: 0 !important;
    position: relative !important;
}
.stCheckbox input[type="checkbox"]:checked {
    background: #22d3ee !important;
    border-color: #22d3ee !important;
}
.stCheckbox input[type="checkbox"]:checked::after {
    content: '' !important;
    position: absolute !important;
    left: 4px !important;
    top: 1px !important;
    width: 7px !important;
    height: 11px !important;
    border: 2px solid white !important;
    border-left: none !important;
    border-top: none !important;
    transform: rotate(45deg) !important;
}
.stCheckbox { margin: 0 !important; padding: 10px 14px !important; }

/* ROW SEPARATOR */
.cl-row-sep { border-bottom: 1px solid rgba(103,232,249,0.14); margin: 0; }

/* MIRROR BOX (COMPLETED COLUMN) */
.mirror-cb {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 8px 0;
}
.mirror-box {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(103,232,249,0.55);
    border-radius: 3px;
    background: transparent;
}
.mirror-box.checked { background: #22d3ee; border-color: #22d3ee; }

/* BUTTON */
.stButton > button {
    width: 100%;
    background: transparent;
    color: #22d3ee;
    border: 2px solid rgba(34,211,238,0.7);
    border-radius: 10px;
    padding: 13px;
    font-size: 17px;
    font-weight: 700;
    transition: 0.3s;
    margin-top: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.stButton > button:hover { background: #22d3ee; color: #08152d; }

/* KPI BOX */
.kpi-box {
    background: rgba(13, 29, 58, 0.98);
    border: 1px solid rgba(103,232,249,0.25);
    border-radius: 12px;
    padding: 18px 12px;
    text-align: center;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.kpi-title {
    color: #67e8f9;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.kpi-number { font-size: 58px; font-weight: 800; color: #22d3ee; line-height: 1; }
.kpi-sub { color: white; font-size: 14px; margin-top: 6px; }
.kpi-date-val { font-size: 14px; font-weight: 700; color: white; margin-top: 12px; }

/* PERFORMANCE TABLE */
.perf-table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid rgba(103,232,249,0.25);
    border-radius: 8px;
    overflow: hidden;
}
.perf-table th {
    padding: 11px 16px;
    background: rgba(15, 23, 42, 0.95);
    color: #22d3ee;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: 1px solid rgba(103,232,249,0.18);
}
.perf-table th:not(:first-child) { text-align: center; }
.perf-table td {
    padding: 12px 16px;
    border: 1px solid rgba(103,232,249,0.14);
    font-size: 15px;
    font-weight: 600;
    color: white;
}
.perf-table td:not(:first-child) { text-align: center; }
.perf-table tr.total-row td { color: #22d3ee; font-weight: 700; text-transform: uppercase; }

/* FOOTER */
.footer-note {
    text-align: center;
    color: rgba(103,232,249,0.85);
    font-size: 15px;
    margin-top: 18px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD GOOGLE SHEET
# =====================================================

try:
    response = requests.get(CSV_URL)
    df = pd.read_csv(StringIO(response.text))
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
except Exception:
    df = pd.DataFrame(columns=[
        "Date", "Clean Skimmer", "Strength Training",
        "Piano Practice", "Drink Smoothie", "Golf Practice"
    ])

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
# SELECTED DATE (persisted in session state)
# =====================================================

current_date = datetime.now()

if "selected_date" not in st.session_state:
    st.session_state.selected_date = current_date.date()

selected_date = st.session_state.selected_date
selected_date_str = selected_date.strftime("%Y-%m-%d")

try:
    pretty_date = selected_date.strftime("%A, %B %-d, %Y")
except ValueError:
    pretty_date = selected_date.strftime("%A, %B %#d, %Y")

# =====================================================
# WEEK BOUNDS (based on selected date)
# =====================================================

selected_dt = datetime(selected_date.year, selected_date.month, selected_date.day)
start_of_week = selected_dt - timedelta(days=selected_dt.weekday())
end_of_week = start_of_week + timedelta(days=6)

try:
    week_start_str = start_of_week.strftime("%a, %b %-d, %Y")
    week_end_str = end_of_week.strftime("%a, %b %-d, %Y")
except ValueError:
    week_start_str = start_of_week.strftime("%a, %b %#d, %Y")
    week_end_str = end_of_week.strftime("%a, %b %#d, %Y")

# =====================================================
# FIND DATA FOR SELECTED DATE & WEEK
# =====================================================

existing_row = None
weekly_df = pd.DataFrame()

if not df.empty and "Date" in df.columns:
    mask = df["Date"].dt.strftime("%Y-%m-%d") == selected_date_str
    matches = df[mask]
    if not matches.empty:
        existing_row = matches.iloc[0]

    weekly_df = df[
        (df["Date"] >= pd.Timestamp(start_of_week.date())) &
        (df["Date"] <= pd.Timestamp(end_of_week.date()))
    ]

# =====================================================
# RELOAD CHECKBOXES WHEN DATE CHANGES OR AFTER SAVE
# Both must happen before any widget is instantiated
# =====================================================

if st.session_state.pop("reset_checkboxes", False):
    # After a successful save — clear all boxes
    for chore in chores:
        st.session_state[f"cb_{chore}"] = False
    st.session_state.prev_date = selected_date_str

elif st.session_state.get("prev_date") != selected_date_str:
    # Date changed — load that date's saved values
    st.session_state.prev_date = selected_date_str
    for chore in chores:
        default = False
        if existing_row is not None:
            try:
                val = existing_row[chore]
                default = bool(val) if pd.notna(val) else False
            except Exception:
                pass
        st.session_state[f"cb_{chore}"] = default

else:
    # First-time initialization only
    for chore in chores:
        key = f"cb_{chore}"
        if key not in st.session_state:
            default = False
            if existing_row is not None:
                try:
                    val = existing_row[chore]
                    default = bool(val) if pd.notna(val) else False
                except Exception:
                    pass
            st.session_state[key] = default

# =====================================================
# TITLE
# =====================================================

st.markdown(
    '<div class="main-title">COLTON DAILY <span>CHORES</span></div>',
    unsafe_allow_html=True
)
st.markdown(
    f'<div class="date-container">'
    f'<div class="date-line"></div>'
    f'<div class="date-text">{pretty_date}</div>'
    f'<div class="date-line"></div>'
    f'</div>',
    unsafe_allow_html=True
)

# =====================================================
# LAYOUT
# =====================================================

left_col, right_col = st.columns([2.2, 1])

# =====================================================
# LEFT PANEL — TODAY'S CHECKLIST
# =====================================================

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    # Section title + date picker side by side
    title_col, picker_col = st.columns([3, 1])
    with title_col:
        st.markdown('<div class="section-title">📋 TODAY\'S CHECKLIST</div>', unsafe_allow_html=True)
    with picker_col:
        st.date_input(
            "date",
            key="selected_date",
            max_value=current_date.date(),
            label_visibility="collapsed"
        )

    # Table header
    st.markdown(
        '<div class="cl-header">'
        '<div class="cl-header-chore">CHORE</div>'
        '<div class="cl-header-done">COMPLETED</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Rows wrapper open
    st.markdown('<div class="cl-rows">', unsafe_allow_html=True)

    chore_values = {}
    for i, chore in enumerate(chores):
        key = f"cb_{chore}"
        is_checked = st.session_state.get(key, False)

        col1, col2 = st.columns([5, 1])
        with col1:
            val = st.checkbox(chore, key=key)
            chore_values[chore] = val
        with col2:
            box_class = "mirror-box checked" if is_checked else "mirror-box"
            st.markdown(
                f'<div class="mirror-cb"><div class="{box_class}"></div></div>',
                unsafe_allow_html=True
            )

        if i < len(chores) - 1:
            st.markdown('<div class="cl-row-sep"></div>', unsafe_allow_html=True)

    # Rows wrapper close
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("SAVE CHORES"):
        try:
            payload = {
                "date":               selected_date_str,
                "clean_skimmer":      1 if chore_values["Clean Skimmer"] else 0,
                "strength_training":  1 if chore_values["Strength Training"] else 0,
                "piano_practice":     1 if chore_values["Piano Practice"] else 0,
                "drink_smoothie":     1 if chore_values["Drink Smoothie"] else 0,
                "golf_practice":      1 if chore_values["Golf Practice"] else 0,
            }
            resp = requests.post(
                "https://script.google.com/macros/s/AKfycbx8ag41V4lHwP3_FQwygXxX-HgD4f-zZnifFFgStnCkBOe7XQ_Yte6SuG-MdElWgq3m/exec",
                json=payload,
                timeout=15
            )
            resp.raise_for_status()

            # Flag reset — applied at top of next run before widgets render
            st.session_state["reset_checkboxes"] = True
            st.toast("✓ Chores saved!", icon="✅")
            st.rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# RIGHT PANEL — WEEKLY SUMMARY
# =====================================================

with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 WEEKLY SUMMARY</div>', unsafe_allow_html=True)

    total_completed = 0
    total_missed = 0

    if not weekly_df.empty:
        for chore in chores:
            if chore in weekly_df.columns:
                completed = int(weekly_df[chore].sum())
                missed = len(weekly_df) - completed
                total_completed += completed
                total_missed += missed

    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.markdown(
            f'<div class="kpi-box">'
            f'<div class="kpi-title">TOTAL COMPLETED</div>'
            f'<div class="kpi-number">{total_completed}</div>'
            f'<div class="kpi-sub">chores</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with kpi2:
        st.markdown(
            f'<div class="kpi-box">'
            f'<div class="kpi-title">TOTAL MISSED</div>'
            f'<div class="kpi-number">{total_missed}</div>'
            f'<div class="kpi-sub">chores</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    week1, week2 = st.columns(2)
    with week1:
        st.markdown(
            f'<div class="kpi-box">'
            f'<div class="kpi-title">WEEK START</div>'
            f'<div class="kpi-date-val">{week_start_str}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with week2:
        st.markdown(
            f'<div class="kpi-box">'
            f'<div class="kpi-title">WEEK END</div>'
            f'<div class="kpi-date-val">{week_end_str}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# WEEKLY PERFORMANCE REPORT
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 WEEKLY PERFORMANCE REPORT</div>', unsafe_allow_html=True)

report_rows = []
total_comp = 0
total_miss = 0

for chore in chores:
    if not weekly_df.empty and chore in weekly_df.columns:
        comp = int(weekly_df[chore].sum())
        miss = len(weekly_df) - comp
        pct = round((comp / len(weekly_df)) * 100, 1) if len(weekly_df) > 0 else 0
    else:
        comp, miss, pct = 0, 0, 0
    total_comp += comp
    total_miss += miss
    report_rows.append((chore, comp, miss, f"{pct}%"))

total_possible = total_comp + total_miss
overall_pct = round((total_comp / total_possible) * 100, 1) if total_possible > 0 else 0

rows_html = "".join(
    f"<tr><td>{c}</td><td>{co}</td><td>{m}</td><td>{p}</td></tr>"
    for c, co, m, p in report_rows
)

st.markdown(f"""
<table class="perf-table">
  <thead>
    <tr>
      <th>CHORE</th>
      <th>COMPLETED</th>
      <th>MISSED</th>
      <th>COMPLETION %</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
    <tr class="total-row">
      <td>TOTAL</td>
      <td>{total_comp}</td>
      <td>{total_miss}</td>
      <td>{overall_pct}%</td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">Stay consistent. Small daily actions lead to big results.</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
