import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from streamlit_calendar import calendar
from supabase import create_client

# --- 設定読み込み ---
USERS = json.loads(st.secrets["USERS"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def load_data():
    response = supabase.table("reservations").select("*").order("start_datetime").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame(columns=["id", "nickname", "equipment", "start_datetime", "end_datetime"])

def insert_reservation(nickname, equipment, start_dt, end_dt):
    supabase.table("reservations").insert({
        "nickname": nickname,
        "equipment": equipment,
        "start_datetime": str(start_dt),
        "end_datetime": str(end_dt)
    }).execute()

def delete_reservation(reservation_id):
    supabase.table("reservations").delete().eq("id", reservation_id).execute()

def check_conflict(equipment, start_dt, end_dt):
    response = supabase.table("reservations").select("*").eq("equipment", equipment).execute()
    for r in response.data:
        if r["start_datetime"] < str(end_dt) and r["end_datetime"] > str(start_dt):
            return True
    return False

def show_calendar_page(title, equipment_colors, page_key):
    equipment_list = list(equipment_colors.keys())
    st.caption("📌 空き時間をクリック → 新規予約　／　既存の予約をクリック → 詳細・削除")
    if st.button("🏠 トップに戻る"):
        st.switch_page("Home.py")

    df_all = load_data()
    df = df_all[df_all["equipment"].isin(equipment_list)] if not df_all.empty else df_all

    events = []
    if not df.empty:
        for _, row in df.iterrows():
            events.append({
                "id": str(row['id']),
                "title": f"{row['nickname']} ({row['equipment']})",
                "start": row['start_datetime'],
                "end": row['end_datetime'],
                "backgroundColor": equipment_colors.get(row['equipment'], "#808080"),
                "borderColor": equipment_colors.get(row['equipment'], "#808080")
            })

    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
        "initialView": "timeGridWeek",
        "navLinks": True,
        "editable": False,
        "selectable": True,
        "selectMinDistance": 0,
        "timeZone": "Asia/Tokyo",
        "slotLabelFormat": {"hour": "2-digit", "minute": "2-digit", "hour12": False},
        "eventTimeFormat": {"hour": "2-digit", "minute": "2-digit", "hour12": False},
        "slotDuration": "01:00:00",
        "slotLabelInterval": "01:00:00",
        "slotMinTime": "07:00:00",
        "slotMaxTime": "31:00:00",
        "scrollTime": "07:00:00",
        "expandRows": True,
        "contentHeight": "auto",
    }

    cal_result = calendar(events=events, options=calendar_options, key=page_key)

    trigger = None
    init_start = None
    init_end = None

    if cal_result and cal_result.get("select"):
        selected = cal_result["select"]
        try:
            init_start = datetime.fromisoformat(selected.get("start", "")[:16])
            init_end = datetime.fromisoformat(selected.get("end", "")[:16])
        except Exception:
            init_start = datetime.now().replace(minute=0, second=0, microsecond=0)
            init_end = init_start + timedelta(hours=1)
        trigger = "new"

    elif cal_result and cal_result.get("dateClick"):
        try:
            init_start = datetime.fromisoformat(cal_result["dateClick"].get("date", "")[:16])
            init_end = init_start + timedelta(hours=1)
        except Exception:
            init_start = datetime.now().replace(minute=0, second=0, microsecond=0)
            init_end = init_start + timedelta(hours=1)
        trigger = "new"

    if trigger == "new" and init_start and init_end:
        @st.dialog("🆕 新規予約")
        def show_new_reservation_dialog(init_start, init_end):
            st.markdown(f"選択時間：**{init_start.strftime('%Y-%m-%d %H:%M')}** 〜 **{init_end.strftime('%Y-%m-%d %H:%M')}**")
            nickname = st.selectbox("利用者", list(USERS.keys()))
            equipment = st.selectbox("機器を選択", equipment_list)
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("開始日", init_start.date())
                start_time = st.time_input("開始時間", init_start.time(), step=3600)
            with col2:
                end_date = st.date_input("終了日", init_end.date())
                end_time = st.time_input("終了時間", init_end.time(), step=3600)
            if st.button("✅ 予約する", type="primary"):
                start_dt = datetime.combine(start_date, start_time)
                end_dt = datetime.combine(end_date, end_time)
                if start_dt >= end_dt:
                    st.error("終了日時は開始日時より後に設定してください。")
                else:
                    if check_conflict(equipment, start_dt, end_dt):
                        st.error("⚠️ その時間は既に別の予約が入っています。")
                    else:
                        insert_reservation(nickname, equipment, start_dt, end_dt)
                        st.success("予約完了！")
                        st.rerun()
        show_new_reservation_dialog(init_start, init_end)

    if cal_result and cal_result.get("eventClick"):
        clicked_id = int(cal_result["eventClick"]["event"]["id"])
        df_reload = load_data()
        df_click = df_reload[df_reload["id"] == clicked_id]
        if not df_click.empty:
            row = df_click.iloc[0]
            @st.dialog("📋 予約の詳細")
            def show_reservation_dialog(row):
                st.markdown(f"**利用者：** {row['nickname']}")
                st.markdown(f"**機器：** {row['equipment']}")
                st.markdown(f"**開始：** {row['start_datetime']}")
                st.markdown(f"**終了：** {row['end_datetime']}")
                st.markdown("---")
                confirm = st.checkbox("本当に削除してよいですか？")
                if st.button("🗑️ 削除する", disabled=not confirm, type="primary"):
                    delete_reservation(int(row["id"]))
                    st.rerun()
            show_reservation_dialog(row)
