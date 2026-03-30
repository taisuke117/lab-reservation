import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="分生関係予約", layout="wide")
st.title("🧬 分生関係 予約")

equipment_colors = {
    "分生エリア": "#C71585",
    "分生室": "#3E2723",
}

show_calendar_page("分生関係", equipment_colors, "bunsei_calendar")
