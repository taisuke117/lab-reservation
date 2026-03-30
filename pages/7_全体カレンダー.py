import streamlit as st
from utils import load_data, USERS
from streamlit_calendar import calendar

st.set_page_config(page_title="全体カレンダー", layout="wide")
st.title("📅 全体カレンダー（すべての機器）")
st.caption("全カテゴリの利用状況をまとめて確認できます。予約・削除は各カテゴリページから行ってください。")

if st.button("🏠 トップに戻る"):
    st.switch_page("Home.py")

# 機器ごとの色定義（全カテゴリ分）
ALL_EQUIPMENT_COLORS = {
    # ミクロトーム
    "回転式ミクロトーム（A）": "#E74C3C",
    "回転式ミクロトーム（B）": "#C0392B",
    "滑走型ミクロトーム":      "#FF6B6B",
    # 実験台
    "実験台１": "#C00000",
    "実験台２": "#78206E",
    "実験台３": "#D86ECC",
    # 包埋
    "包埋ロータリー・包埋センター": "#F39C12",
    # バーチャル
    "バーチャル撮影装置": "#9B59B6",
    # 分生
    "分生エリア": "#27AE60",
    "分生室":     "#1E8449",
    # 培養室
    "安全キャビネット": "#16A085",
    "クリーンベンチ":   "#1ABC9C",
}

df = load_data()

events = []
if not df.empty:
    for _, row in df.iterrows():
        color = ALL_EQUIPMENT_COLORS.get(row["equipment"], "#808080")
        events.append({
            "id": str(row["id"]),
            "title": f"{row['nickname']} ({row['equipment']})",
            "start": row["start_datetime"],
            "end":   row["end_datetime"],
            "backgroundColor": color,
            "borderColor":     color,
        })

calendar_options = {
    "headerToolbar": {
        "left":   "today prev,next",
        "center": "title",
        "right":  "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "initialView": "timeGridWeek",
    "navLinks": True,
    "editable": False,
    "selectable": False,          # 全体カレンダーは閲覧のみ
    "timeZone": "Asia/Tokyo",
    "slotLabelFormat": {"hour": "2-digit", "minute": "2-digit", "hour12": False},
    "eventTimeFormat": {"hour": "2-digit", "minute": "2-digit", "hour12": False},
    "slotDuration": "01:00:00",
    "slotMinTime": "00:00:00",
    "slotMaxTime": "24:00:00",
    "scrollTime": "00:00:00",
    "slotEventOverlap": False, 
    "expandRows": True,
    "contentHeight": "auto",
}

calendar(events=events, options=calendar_options, key="overview_calendar")

st.markdown("---")
st.caption("予約・削除はトップページから各カテゴリを選んで行ってください。")
