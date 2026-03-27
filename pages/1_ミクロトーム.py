import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import show_calendar_page

st.set_page_config(page_title="ミクロトーム予約", layout="wide")
st.title("🔪 ミクロトーム 予約")

equipment_colors = {
    "回転式ミクロトーム（旧型）": "#002060",
    "回転式ミクロトーム（新型）": "#0B76A0",
    "滑走型ミクロトーム": "#4E95D9",
}

show_calendar_page("ミクロトーム", equipment_colors, "microtome_calendar")