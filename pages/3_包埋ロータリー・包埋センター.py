import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="包埋ロータリー・包埋センター予約", layout="wide")
st.title("📦 包埋ロータリー・包埋センター 予約")

equipment_colors = {
    "包埋ロータリー": "#8B0000",
    "包埋センター": "#CD5C5C",
}

show_calendar_page("包埋ロータリー・包埋センター", equipment_colors, "embedding_calendar")
