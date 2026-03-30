import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="実験台（実験室）予約", layout="wide")
st.title("🎨 実験台（実験室） 予約")

equipment_colors = {
    "実験台１": "#C00000",
    "実験台２": "#78206E",
    "実験台３": "#D86ECC",
}

show_calendar_page("実験台（実験室）", equipment_colors, "staining_calendar")
