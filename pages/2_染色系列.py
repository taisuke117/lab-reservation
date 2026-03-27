import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page

st.set_page_config(page_title="染色系列予約", layout="wide")
st.title("🎨 染色系列 予約")

equipment_colors = {
    "染色系列": "#D86ECC",
}

show_calendar_page("染色系列", equipment_colors, "staining_calendar")
