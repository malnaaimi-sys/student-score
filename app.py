import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Simple Streamlit App", layout="centered")
st.title("🎓 Student Score Tracker (Simple Example)")

# ---- Sidebar settings
with st.sidebar:
    st.header("Settings")
    pass_mark = st.slider("Pass mark", min_value=0, max_value=100, value=60)
    today = st.date_input("Date", value=date.today())

# ---- Session state: store entries
if "log" not in st.session_state:
    st.session_state.log = pd.DataFrame(columns=["Date", "Name", "Score", "Result", "Note"])

st.subheader("Add a new entry")

name = st.text_input("Student name", placeholder="e.g., Ali")
score = st.number_input("Score (0–100)", min_value=0, max_value=100, value=75, step=1)
note = st.text_input("Note (optional)", placeholder="e.g., makeup exam")

result = "PASS ✅" if score >= pass_mark else "FAIL ❌"

col1, col2 = st.columns(2)
col1.metric("Pass mark", pass_mark)
col2.metric("Result", result)

if st.button("Add to log", type="primary"):
    new_row = {
        "Date": today,
        "Name": name.strip() if name else "",
        "Score": int(score),
        "Result": result,
        "Note": note.strip() if note else ""
    }
    st.session_state.log = pd.concat([st.session_state.log, pd.DataFrame([new_row])], ignore_index=True)
    st.toast("Added ✅")

st.divider()

st.subheader("Log")
st.dataframe(st.session_state.log, use_container_width=True)

# ---- Simple stats
if not st.session_state.log.empty:
    avg_score = st.session_state.log["Score"].mean()
    pass_rate = (st.session_state.log["Result"].str.contains("PASS").mean()) * 100

    c1, c2 = st.columns(2)
    c1.metric("Average score", f"{avg_score:.1f}")
    c2.metric("Pass rate", f"{pass_rate:.0f}%")

st.divider()

# ---- Download
csv_bytes = st.session_state.log.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download CSV",
    data=csv_bytes,
    file_name="student_scores.csv",
    mime="text/csv"
)
