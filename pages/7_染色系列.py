import streamlit as st
import sys
sys.path.append("/mount/src/lab-reservation")
from utils import show_calendar_page
from utils import add_noindex
from utils import check_password

st.set_page_config(page_title="Staining", layout="wide")
add_noindex()
check_password()
st.title("🎨 染色系列 予約")

equipment_colors = {
    "染色": "#D81B60",
    "その他の作業1（染色）": "#708090",
    "その他の作業2（染色）": "#696969",
}

# 染色は複数人が同時に別々の作業をすることがあるので、同じ時間帯の重複予約を許可する
show_calendar_page("染色系列", equipment_colors, "staining_series_calendar", allow_overlap=True)
