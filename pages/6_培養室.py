import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page
from utils import add_noindex
from utils import check_password


st.set_page_config(page_title="Cell Culture", layout="wide")
add_noindex()
check_password() 
st.title("🧫 培養室 予約")

equipment_colors = {
    "安全キャビネット": "#B8860B",
    "クリーンベンチ": "#E65100",
    "その他の作業1（培養室）": "#708090",
    "その他の作業2（培養室）": "#696969",
}

show_calendar_page("培養室", equipment_colors, "culture_calendar")
