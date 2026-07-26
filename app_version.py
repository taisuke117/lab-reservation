"""バージョン情報の唯一の定義場所。

バージョンを上げるときは、このファイルの ``APP_VERSION`` だけを書き換えて
``python tools/update_version.py`` を実行する（README にも自動で反映される）。
日付から自動採番したい場合は、引数なしで実行すれば当日の日付になる。

表記は ``v<メジャー>.<YYMMDD>``（例: ``v2.260725`` = メジャー2・2026-07-25 更新）。
"""

APP_NAME = "NDUP機器 予約システム"
APP_VERSION = "v2.260726"
AUTHOR = "Taisuke Hani"
REPO_URL = "https://github.com/taisuke117/lab-reservation"
