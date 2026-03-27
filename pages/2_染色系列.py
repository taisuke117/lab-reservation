import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import show_calendar_page

st.set_page_config(page_title="染色系列予約", layout="wide")
st.title("🎨 染色系列 予約")

equipment_colors = {
    "染色系列": "#D86ECC",
}

show_calendar_page("染色系列", equipment_colors, "staining_calendar")