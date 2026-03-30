import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="培養室予約", layout="wide")
st.title("🧫 培養室 予約")

equipment_colors = {
    "安全キャビネット": "#2F4F4F",
    "クリーンベンチ": "#333333",
}

show_calendar_page("培養室", equipment_colors, "culture_calendar")
