import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="ミクロトーム予約", layout="wide")
st.title("🔪 ミクロトーム 予約")

equipment_colors = {
    "回転式ミクロトーム（A）": "#002060",
    "回転式ミクロトーム（B）": "#0B76A0",
    "滑走型ミクロトーム": "#4E95D9",
}

show_calendar_page("ミクロトーム", equipment_colors, "microtome_calendar")
