import streamlit as st

st.set_page_config(page_title="NDUP機器 予約システム", layout="wide")
st.title("🔬 NDUP機器 予約システム")
st.markdown("---")
st.subheader("予約したい機器のカテゴリを選んでください")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔪 ミクロトーム", use_container_width=True, type="primary"):
        st.switch_page("pages/1_ミクロトーム.py")
    st.caption("回転式ミクロトーム（旧型）／回転式ミクロトーム（新型）／滑走型ミクロトーム")

    st.markdown("")

    if st.button("📦 包埋ロータリー・包埋センター", use_container_width=True, type="primary"):
        st.switch_page("pages/3_包埋ロータリー・包埋センター.py")
    st.caption("包埋ロータリー／包埋センター")

    st.markdown("")

    if st.button("🧬 分生関係", use_container_width=True, type="primary"):
        st.switch_page("pages/5_分生関係.py")
    st.caption("分生エリア／分生室")

with col2:
    if st.button("🎨 染色系列", use_container_width=True, type="primary"):
        st.switch_page("pages/2_染色系列.py")
    st.caption("染色系列")

    st.markdown("")

    if st.button("🎥 バーチャル撮影装置", use_container_width=True, type="primary"):
        st.switch_page("pages/4_バーチャル撮影装置.py")
    st.caption("バーチャル撮影装置")

    st.markdown("")

    if st.button("🧫 培養室", use_container_width=True, type="primary"):
        st.switch_page("pages/6_培養室.py")
    st.caption("安全キャビネット／クリーンベンチ")

st.markdown("---")
st.caption("📌 各カテゴリページでカレンダーの空き時間をクリック → 新規予約　／　既存の予約をクリック → 詳細・削除")
st.caption("📌 作成者・管理者　Taisuke Hani https://github.com/taisuke117")
