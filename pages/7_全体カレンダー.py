import streamlit as st
from utils import load_data
from streamlit_calendar import calendar

st.set_page_config(page_title="全体カレンダー", layout="wide")
st.title("📅 全体カレンダー（すべての機器）")
st.caption("全カテゴリの利用状況をまとめて確認できます。予約・削除は各カテゴリページから行ってください。")

if st.button("🏠 トップに戻る"):
    st.switch_page("Home.py")

ALL_EQUIPMENT_COLORS = {
    "回転式ミクロトーム（A）": "#E74C3C",
    "回転式ミクロトーム（B）": "#C0392B",
    "滑走型ミクロトーム":      "#FF6B6B",
    "実験台１": "#C00000",
    "実験台２": "#78206E",
    "実験台３": "#D86ECC",
    "包埋ロータリー": "#8B0000",
    "包埋センター": "#CD5C5C",
    "バーチャル撮影装置": "#9B59B6",
    "分生エリア": "#27AE60",
    "分生室":     "#1E8449",
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
    "selectable": False,
    "slotEventOverlap": False,
    "timeZone": "Asia/Tokyo",
    "slotLabelFormat": {"hour": "2-digit", "minute": "2-digit", "hour12": False},
    "eventTimeFormat": {"hour": "2-digit", "minute": "2-digit", "hour12": False},
    "slotDuration": "01:00:00",
    "slotMinTime": "00:00:00",
    "slotMaxTime": "24:00:00",
    "scrollTime": "00:00:00",
    "expandRows": True,
    "contentHeight": "auto",
}

cal_result = calendar(events=events, options=calendar_options, key="overview_calendar")

@st.dialog("📋 予約の詳細")
def show_detail_dialog(row):
    st.markdown(f"**利用者：** {row['nickname']}")
    st.markdown(f"**機器：** {row['equipment']}")
    st.markdown(f"**開始：** {row['start_datetime']}")
    st.markdown(f"**終了：** {row['end_datetime']}")

if cal_result and cal_result.get("eventClick"):
    clicked_id = int(cal_result["eventClick"]["event"]["id"])
    df_reload = load_data()
    df_click = df_reload[df_reload["id"] == clicked_id]
    if not df_click.empty:
        show_detail_dialog(df_click.iloc[0])

st.markdown("---")
st.caption("予約・削除はトップページから各カテゴリを選んで行ってください。")
