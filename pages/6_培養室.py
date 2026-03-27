import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import show_calendar_page

st.set_page_config(page_title="培養室予約", layout="wide")
st.title("🧫 培養室 予約")

equipment_colors = {
    "安全キャビネット": "#059349",
    "クリーンベンチ": "#00B050",
}

show_calendar_page("培養室", equipment_colors, "culture_calendar")
