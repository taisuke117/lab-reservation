import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="ミクロトーム予約", layout="wide")
st.title("🔪 ミクロトーム 予約")

equipment_colors = {
    "回転式ミクロトーム（A）": "#8B0000",
    "回転式ミクロトーム（B）": "#A0522D",
    "滑走型ミクロトーム": "#556B2F",
}

show_calendar_page("ミクロトーム", equipment_colors, "microtome_calendar")
