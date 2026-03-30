import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="包埋ロータリー・包埋センター予約", layout="wide")
st.title("📦 包埋ロータリー・包埋センター 予約")

equipment_colors = {
    "包埋ロータリー": "#000080",
    "包埋センター": "#4B0082",
}

show_calendar_page("包埋ロータリー・包埋センター", equipment_colors, "embedding_calendar")
