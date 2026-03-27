import streamlit as st
import pandas as pd
import sqlite3
import yagmail
from datetime import datetime, date, time, timedelta
from streamlit_calendar import calendar

# --- 1. ユーザー設定とメール送信設定 ---

# 機密情報はst.secretsから読み込む
import json
USERS = json.loads(st.secrets["USERS"])
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]

# --- メール送信関数 ---
def send_confirmation_email(to_email, nickname, equipment, start_dt, end_dt):
    subject = f"【予約完了】{equipment} のご予約"
    body = f"""
{nickname} 先生

以下の内容でラボ機器の予約が完了しました。

機器: {equipment}
開始: {start_dt.strftime('%Y-%m-%d %H:%M')}
終了: {end_dt.strftime('%Y-%m-%d %H:%M')}

---
本メールは予約システムからの自動送信です。
"""
    try:
        yag = yagmail.SMTP(user=SENDER_EMAIL, password=APP_PASSWORD)
        yag.send(to=to_email, subject=subject, contents=[body])
        return True
    except Exception as e:
        st.error(f"メール送信エラー: {type(e).__name__}: {e}")
        return False

def send_cancellation_email(to_email, nickname, equipment, start_dt, end_dt):
    subject = f"【予約キャンセル】{equipment} のご予約が削除されました"
    body = f"""
{nickname} 先生

以下の予約が削除されました。

機器: {equipment}
開始: {start_dt}
終了: {end_dt}

ご不明な点があれば管理者にお問い合わせください。

---
本メールは予約システムからの自動送信です。
"""
    try:
        yag = yagmail.SMTP(user=SENDER_EMAIL, password=APP_PASSWORD)
        yag.send(to=to_email, subject=subject, contents=[body])
        return True
    except Exception as e:
        st.error(f"キャンセルメール送信エラー: {type(e).__name__}: {e}")
        return False

# --- 2. データベースの初期設定 ---
DB_FILE = 'lab_reservations_v2.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            equipment TEXT,
            start_datetime TEXT,
            end_datetime TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM reservations", conn)
    conn.close()
    return df

# --- 3. UIと画面描画 ---
st.set_page_config(page_title="ラボ機器 予約システム", layout="wide")
st.title("ラボ機器 予約システム")
st.caption("📌 カレンダーの空き時間をクリック → 新規予約　／　既存の予約をクリック → 詳細・削除")

equipment_colors = {
    "リアルタイムPCR": "#FF4B4B",
    "安全キャビネット": "#0068C9",
    "CO2インキュベーター": "#83C9FF",
    "化学発光撮影装置": "#FFABAB",
    "共焦点レーザー顕微鏡": "#29B09D",
    "共焦点レーザー顕微鏡2": "#29B07D"
}
equipment_list = list(equipment_colors.keys())

# --- 4. カレンダー表示 ---
df = load_data()
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
    "slotDuration": "01:00:00",
    "slotMinTime": "07:00:00",   # 表示開始：朝7時
    "slotMaxTime": "31:00:00",   # 表示終了：翌朝6時（24+6=30）
    "scrollTime": "07:00:00",
    "expandRows": True,
    "contentHeight": "auto",
}

cal_result = calendar(events=events, options=calendar_options, key="main_calendar")

# --- 5. クリック or ドラッグ → 新規予約ダイアログ ---
trigger = None
init_start = None
init_end = None

if cal_result and cal_result.get("select"):
    selected = cal_result["select"]
    raw_start = selected.get("start", "")
    raw_end = selected.get("end", "")
    try:
        init_start = datetime.fromisoformat(raw_start[:16])
        init_end = datetime.fromisoformat(raw_end[:16])
    except Exception:
        init_start = datetime.now().replace(minute=0, second=0, microsecond=0)
        init_end = init_start + timedelta(hours=1)
    trigger = "new"

elif cal_result and cal_result.get("dateClick"):
    raw = cal_result["dateClick"].get("date", "")
    try:
        init_start = datetime.fromisoformat(raw[:16])
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
            start_time = st.time_input("開始時間", init_start.time())
        with col2:
            end_date = st.date_input("終了日", init_end.date())
            end_time = st.time_input("終了時間", init_end.time())

        col3, col4 = st.columns(2)
        with col3:
            if st.button("✅ 予約する", type="primary"):
                start_dt = datetime.combine(start_date, start_time)
                end_dt = datetime.combine(end_date, end_time)

                if start_dt >= end_dt:
                    st.error("終了日時は開始日時より後に設定してください。")
                else:
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute('''
                        SELECT * FROM reservations
                        WHERE equipment=? AND (start_datetime < ? AND end_datetime > ?)
                    ''', (equipment, str(end_dt), str(start_dt)))
                    conflict = c.fetchone()

                    if conflict:
                        st.error("⚠️ その時間は既に別の予約が入っています。")
                        conn.close()
                    else:
                        c.execute('''
                            INSERT INTO reservations (nickname, equipment, start_datetime, end_datetime)
                            VALUES (?, ?, ?, ?)
                        ''', (nickname, equipment, str(start_dt), str(end_dt)))
                        conn.commit()
                        conn.close()
                        user_email = USERS[nickname]
                        mail_success = send_confirmation_email(user_email, nickname, equipment, start_dt, end_dt)
                        if mail_success:
                            st.success(f"予約完了！{user_email} 宛にメールを送信しました。")
                        else:
                            st.warning("予約は完了しましたが、メール送信でエラーが発生しました。")
                        st.rerun()
        with col4:
            if st.button("✖ キャンセル"):
                st.rerun()

    show_new_reservation_dialog(init_start, init_end)

# --- 6. 既存予約クリック → 詳細・削除ダイアログ ---
if cal_result and cal_result.get("eventClick"):
    clicked = cal_result["eventClick"]["event"]
    clicked_id = int(clicked["id"])

    conn = sqlite3.connect(DB_FILE)
    result_df = pd.read_sql_query(
        "SELECT * FROM reservations WHERE id=?", conn, params=(clicked_id,)
    )
    conn.close()

    if not result_df.empty:
        row = result_df.iloc[0]

        @st.dialog("📋 予約の詳細")
        def show_reservation_dialog(row):
            st.markdown(f"**利用者：** {row['nickname']}")
            st.markdown(f"**機器：** {row['equipment']}")
            st.markdown(f"**開始：** {row['start_datetime']}")
            st.markdown(f"**終了：** {row['end_datetime']}")
            st.markdown("---")
            confirm = st.checkbox("本当に削除してよいですか？")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ 削除する", disabled=not confirm, type="primary"):
                    conn2 = sqlite3.connect(DB_FILE)
                    c = conn2.cursor()
                    c.execute("DELETE FROM reservations WHERE id=?", (int(row["id"]),))
                    conn2.commit()
                    conn2.close()

                    owner_email = USERS.get(row["nickname"])
                    if owner_email:
                        mail_ok = send_cancellation_email(
                            to_email=owner_email,
                            nickname=row["nickname"],
                            equipment=row["equipment"],
                            start_dt=row["start_datetime"],
                            end_dt=row["end_datetime"],
                        )
                        if mail_ok:
                            st.success(f"{owner_email} に通知しました。")
                        else:
                            st.warning("削除しましたが、通知メールの送信に失敗しました。")
                    st.rerun()
            with col2:
                if st.button("✖ キャンセル"):
                    st.rerun()

        show_reservation_dialog(row)