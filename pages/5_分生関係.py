import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import show_calendar_page

st.set_page_config(page_title="分生関係予約", layout="wide")
st.title("🧬 分生関係 予約")

equipment_colors = {
    "分生エリア": "#EAB200",
    "分生室": "#C97A07",
}

show_calendar_page("分生関係", equipment_colors, "bunsei_calendar")