import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta, date
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

def _combine_with_hour(d, hour):
    if hour == 24:
        return datetime.combine(d + timedelta(days=1), datetime.min.time())
    return datetime.combine(d, datetime.min.time().replace(hour=hour))

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
        "slotMinTime": "00:00:00",
        "slotMaxTime": "24:00:00",
        "scrollTime": "00:00:00",
        "expandRows": True,
        "contentHeight": "auto",
    }

    cal_result = calendar(events=events, options=calendar_options, key=page_key)

    slot_min_h = int(calendar_options["slotMinTime"][:2])
    slot_max_h = int(calendar_options["slotMaxTime"][:2])

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
            raw = cal_result["dateClick"].get("date", "")
            is_all_day = cal_result["dateClick"].get("allDay", False)
            init_start = datetime.fromisoformat(raw[:16])
            if is_all_day:
                init_start = init_start.replace(hour=slot_min_h, minute=0, second=0)
                if slot_max_h >= 24:
                    extra_days = slot_max_h // 24
                    end_h = slot_max_h % 24
                    end_date = init_start.date() + timedelta(days=extra_days)
                    init_end = datetime.combine(end_date, datetime.min.time().replace(hour=end_h))
                else:
                    init_end = init_start.replace(hour=slot_max_h, minute=0, second=0)
            else:
                init_end = init_start + timedelta(hours=1)
        except Exception:
            init_start = datetime.now().replace(minute=0, second=0, microsecond=0)
            init_end = init_start + timedelta(hours=1)
        trigger = "new"

    if trigger == "new" and init_start and init_end:
        @st.dialog("🆕 新規予約")
        def show_new_reservation_dialog(init_start, init_end):
            st.markdown(f"選択時間：**{init_start.strftime('%Y-%m-%d %H:%M')}** 〜 **{init_end.strftime('%Y-%m-%d %H:%M')}**")

            # 先頭に「名前を選択してください」を追加
            user_options = ["名前を選択してください"] + USERS
            saved = st.session_state.get("lab_user", "")
            default_index = user_options.index(saved) if saved and saved in user_options else 0

            nickname = st.selectbox("利用者", user_options, index=default_index)
            equipment = st.selectbox("機器を選択", equipment_list)
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("開始日", init_start.date())
                start_hour = st.selectbox(
                    "開始時間",
                    list(range(25)),
                    index=init_start.hour,
                    format_func=lambda h: f"{h:02d}:00"
                )
            with col2:
                end_date = st.date_input("終了日", init_end.date())
                end_hour = st.selectbox(
                    "終了時間",
                    list(range(25)),
                    index=min(init_end.hour, 24),
                    format_func=lambda h: f"{h:02d}:00"
                )
            _, col_center, _ = st.columns([1, 2, 1])
            with col_center:
                if st.button("✅ 予約する", type="primary", use_container_width=True):
                    if nickname == "名前を選択してください":
                        st.error("利用者名を選択してください。")
                    else:
                        start_dt = _combine_with_hour(start_date, start_hour)
                        end_dt = _combine_with_hour(end_date, end_hour)
                        if start_dt >= end_dt:
                            st.error("終了日時は開始日時より後に設定してください。")
                        else:
                            if check_conflict(equipment, start_dt, end_dt):
                                st.error("⚠️ その時間は既に別の予約が入っています。")
                            else:
                                insert_reservation(nickname, equipment, start_dt, end_dt)
                                st.session_state["lab_user"] = nickname
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
                _, col_center, _ = st.columns([1, 2, 1])
                with col_center:
                    if st.button("🗑️ 削除する", disabled=not confirm, type="primary", use_container_width=True):
                        delete_reservation(int(row["id"]))
                        st.rerun()
            show_reservation_dialog(row)
