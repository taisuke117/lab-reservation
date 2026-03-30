import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="バーチャル撮影装置予約", layout="wide")
st.title("🎥 バーチャル撮影装置 予約")

equipment_colors = {
    "バーチャル撮影装置": "#8B008B",
}

show_calendar_page("バーチャル撮影装置", equipment_colors, "virtual_calendar")
