"""Streamlit Community Cloud のアプリをヘッドレスブラウザで開いて起こしておく。

curl などで URL に GET するだけでは「アクセスあり」と見なされず、スリープ中でも
HTTP 200 が返るので失敗に気づけない。ブラウザで実際にページを開き、アプリの
Python 側が動いてログイン画面が出るところまで確かめる。スリープ画面が出ていたら
起動ボタンを押して待つ。

GitHub Actions（.github/workflows/keep-awake.yml）から実行する::

    APP_URL=https://xxx.streamlit.app/ python tools/wake_app.py

起動を確認できなければ終了コード 1 で終わり、ワークフローが失敗表示になる。
"""

import os
import re
import sys
import time

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

# スリープ画面のボタン（Streamlit Community Cloud の英語表記）
WAKE_BUTTON = re.compile(r"get this app back up", re.I)
# アプリの Python が動いた証拠になる文言（ログイン画面のパスワード欄のラベル）。
# 画面の枠だけなら Python を動かさなくても表示されるので、枠の有無では判定しない。
READY_TEXT = "パスワードを入力"
TIMEOUT_SEC = 300
POLL_MS = 5_000
# 起動を確認したあと、接続をしばらく保ってアクセスとして記録されるようにする
STAY_MS = 15_000


def app_is_ready(page):
    # Community Cloud はアプリ本体を iframe の中に表示するので、全フレームを探す
    for frame in page.frames:
        try:
            if frame.get_by_text(READY_TEXT).count() > 0:
                return True
        except PlaywrightError:
            continue
    return False


def click_wake_button(page):
    for frame in page.frames:
        try:
            button = frame.get_by_role("button", name=WAKE_BUTTON)
            if button.count() > 0 and button.first.is_visible():
                button.first.click()
                return True
        except PlaywrightError:
            continue
    return False


def main():
    url = os.environ.get("APP_URL", "").strip()
    if not url:
        print("::error::APP_URL が設定されていません（GitHub Secrets を確認してください）")
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=120_000)

        woke = False
        deadline = time.monotonic() + TIMEOUT_SEC
        while time.monotonic() < deadline:
            if app_is_ready(page):
                note = "（スリープ中だったので起こしました）" if woke else ""
                print(f"アプリが起動していることを確認しました{note}")
                page.wait_for_timeout(STAY_MS)
                browser.close()
                return 0
            if click_wake_button(page):
                print("スリープ中だったので起動ボタンを押しました。起動を待ちます")
                woke = True
            page.wait_for_timeout(POLL_MS)

        print(f"::error::{TIMEOUT_SEC} 秒以内にアプリの起動を確認できませんでした")
        browser.close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
