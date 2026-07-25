"""バージョン表記を app_version.py から他のファイルへ反映する。

.py 側は app_version.py を import しているので書き換え不要だが、README は
Markdown なので import できない。このスクリプトが README のバージョン欄
（``<!--VERSION-->`` 〜 ``<!--/VERSION-->`` で囲まれた部分）を同期する。

使い方（リポジトリ直下で実行）::

    python tools/update_version.py             # 当日の日付でバージョンを上げる
    python tools/update_version.py v2.260801   # バージョンを明示指定する
    python tools/update_version.py --check     # 書き換えずにズレの有無だけ見る
"""

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "app_version.py"
README = ROOT / "README.md"

VERSION_PATTERN = re.compile(r'^APP_VERSION\s*=\s*"(?P<version>[^"]+)"', re.MULTILINE)
README_PATTERN = re.compile(r"(<!--VERSION-->)(?P<version>.*?)(<!--/VERSION-->)", re.DOTALL)


def read_current_version():
    match = VERSION_PATTERN.search(VERSION_FILE.read_text(encoding="utf-8"))
    if not match:
        sys.exit(f"APP_VERSION が {VERSION_FILE.name} に見つかりません。")
    return match.group("version")


def build_today_version(current):
    """現在のメジャー番号を保ったまま、日付部分を今日にする。"""
    major = current.lstrip("v").split(".")[0] if "." in current else "1"
    return f"v{major}.{date.today():%y%m%d}"


def write_version_file(new_version):
    text = VERSION_FILE.read_text(encoding="utf-8")
    updated = VERSION_PATTERN.sub(f'APP_VERSION = "{new_version}"', text, count=1)
    if updated != text:
        VERSION_FILE.write_text(updated, encoding="utf-8")
        return True
    return False


def write_readme(new_version):
    text = README.read_text(encoding="utf-8")
    if not README_PATTERN.search(text):
        sys.exit(
            "README.md にバージョン欄のマーカーがありません。"
            " 見出し行を `<!--VERSION-->v2.260725<!--/VERSION-->` の形にしてください。"
        )
    # 説明文などにマーカーを書いても巻き込まないよう、最初の1か所だけ置換する
    updated = README_PATTERN.sub(rf"\g<1>{new_version}\g<3>", text, count=1)
    if updated != text:
        README.write_text(updated, encoding="utf-8")
        return True
    return False


def readme_version():
    match = README_PATTERN.search(README.read_text(encoding="utf-8"))
    return match.group("version") if match else None


def main(argv):
    check_only = "--check" in argv
    args = [a for a in argv if not a.startswith("--")]

    current = read_current_version()

    if check_only:
        in_readme = readme_version()
        print(f"app_version.py : {current}")
        print(f"README.md      : {in_readme}")
        if current != in_readme:
            print("→ ズレています。`python tools/update_version.py` で同期してください。")
            return 1
        print("→ 一致しています。")
        return 0

    new_version = args[0] if args else build_today_version(current)
    if not new_version.startswith("v"):
        new_version = "v" + new_version

    changed_py = write_version_file(new_version)
    changed_md = write_readme(new_version)

    print(f"バージョン: {current} → {new_version}")
    print(f"  app_version.py : {'更新' if changed_py else '変更なし'}")
    print(f"  README.md      : {'更新' if changed_md else '変更なし'}")
    print("  各 .py は app_version.py を import しているので書き換え不要です。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
