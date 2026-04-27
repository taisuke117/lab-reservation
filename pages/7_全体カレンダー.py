import streamlit as st
from utils import load_data
from streamlit_calendar import calendar
import streamlit as st

st.set_page_config(layout="wide")

# ↓↓↓ これを追加 ↓↓↓
st.markdown("""
<style>
/* streamlit-calendar のiframe高さを内容に合わせて伸ばす */
div[data-testid="stCustomComponentV1"] > iframe {
    min-height: 900px;
    height: auto !important;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="全体カレンダー", layout="wide")
st.title("📅 全体カレンダー（すべての機器）")
st.caption("全カテゴリの利用状況をまとめて確認できます。予約・削除は各カテゴリページから行ってください。")

if st.button("🏠 トップに戻る"):
    st.switch_page("Home.py")

ALL_EQUIPMENT_COLORS = {
    "回転式ミクロトーム（A）": "#8B0000",
    "回転式ミクロトーム（B）": "#A0522D",
    "滑走型ミクロトーム":      "#556B2F",
    "実験台１": "#006400",
    "実験台２": "#008080",
    "実験台３": "#0056B3",
    "包埋ロータリー": "#000080",
    "包埋センター": "#4B0082",
    "バーチャル撮影装置": "#8B008B",
    "分生エリア": "#C71585",
    "分生室":     "#3E2723",
    "安全キャビネット": "#2F4F4F",
    "クリーンベンチ":   "#333333",
}

df = load_data()

events = []
if not df.empty:
    for _, row in df.iterrows():
        color = ALL_EQUIPMENT_COLORS.get(row["equipment"], "#808080")
        notes_val = str(row.get('notes', '')).strip()
        if notes_val and notes_val != "nan":
            title_str = f"{row['nickname']} ({row['equipment']}) 📝{notes_val}"
        else:
            title_str = f"{row['nickname']} ({row['equipment']})"
        events.append({
            "id": str(row["id"]),
            "title": title_str,
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
    "initialView": "dayGridMonth",   # ← ここを変更（timeGridWeek → dayGridMonth）
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
    "expandRows": False,             # ← False のまま維持
    "contentHeight": "auto",
}

custom_css = """
.fc-scroller {
    overflow: visible !important;
}
.fc-scroller-harness {
    overflow: visible !important;
}
.fc-daygrid-body {
    width: 100% !important;
}
"""

cal_result = calendar(
    events=events,
    options=calendar_options,
    custom_css=custom_css,   # ← 追加
    key="overview_calendar",
)

@st.dialog("📋 予約の詳細")
def show_detail_dialog(row):
    st.markdown(f"**利用者：** {row['nickname']}")
    st.markdown(f"**機器：** {row['equipment']}")
    st.markdown(f"**開始：** {row['start_datetime']}")
    st.markdown(f"**終了：** {row['end_datetime']}")
    notes_val = str(row.get('notes', '')).strip()
    if notes_val and notes_val != "nan":
        st.markdown(f"**備考：** {notes_val}")

if cal_result and cal_result.get("eventClick"):
    clicked_id = int(cal_result["eventClick"]["event"]["id"])
    df_reload = load_data()
    df_click = df_reload[df_reload["id"] == clicked_id]
    if not df_click.empty:
        show_detail_dialog(df_click.iloc[0])

st.markdown("---")
st.caption("予約・削除はトップページから各カテゴリを選んで行ってください。")
