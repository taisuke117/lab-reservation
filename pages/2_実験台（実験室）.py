import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page
from utils import add_noindex

st.set_page_config(page_title="Lab Bench", layout="wide")
add_noindex()
st.title("🎨 実験台（実験室） 予約")

equipment_colors = {
    "実験台１": "#006400",
    "実験台２": "#008080",
    "実験台３": "#0056B3",
}

show_calendar_page("実験台（実験室）", equipment_colors, "staining_calendar")
