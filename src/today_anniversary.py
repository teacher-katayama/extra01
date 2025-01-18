# -*- coding: utf-8 -*-
"""今日の記念日を取得する

利用しているWeb APIのリファレンス
https://www.whatistoday.cyou/index.cgi/

作者様のNotes
https://note.com/sooz/n/naffb68c7f53b
"""

# ライブラリのインポート
import datetime

import requests


class TodayAnniversary:
    """今日は何の日APIを利用して記念日を取得する"""

    def __init__(self):
        self.base_url = "https://api.whatistoday.cyou/v3/anniv/"  # APIのベースURL

    def get_today_anniversary(self) -> str:
        """今日の記念日を取得する

        Returns:
            str: 今日の記念日
        """
        mmdd = datetime.date.today().strftime("%m%d")
        url = self.base_url + mmdd

        try:
            r = requests.get(url)
            r.raise_for_status()  # HTTPエラーが発生した場合に例外を送出
            data = r.json()
            return data["anniv1"]
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
        except KeyError:
            return "Error: 'anniv1' not found in the response"


if __name__ == "__main__":
    api = TodayAnniversary()
    print(api.get_today_anniversary())
