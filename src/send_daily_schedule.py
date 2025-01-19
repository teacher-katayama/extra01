# -*- coding: utf-8 -*-
"""本日の予定をLINEに送信する
Note:
    毎朝6時に起動する
        cronで実現
    Notionから情報を取得する
        database_id = 「Task DB」
        状態 = 「完了」以外
        予定日 = 今日以前
        並び替え「予定日」の昇順
    リストを改行で結合し、文字列「mail_body」にする
    「mail_body」が空でなければ、LINEに通知する
"""

# ライブラリのインポート
from datetime import date

from notion_client import Client

import send_line_message
import today_anniversary
import weather_forecast
import weather_to_emoji


class TodaySchedule:
    """本日の予定を管理するクラス"""

    NOTION_API_KEY = (
        "secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Notion APIキー
    )
    DATABASE_ID_My_Task = (
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # データベースID「My Task DB」
    )

    def __init__(self):
        """初期化メソッド"""
        self.notion = Client(auth=self.NOTION_API_KEY)

    def get_today_schedule(self) -> str:
        """本日の予定を取得する

        Returns:
            str: 本日の予定

        Notes:
            フィルター条件: 状態が完了と一致しない
                AND 予定日が今日以前
            並べ替え条件: 予定日の昇順
        """
        today = date.today()
        data = self.notion.databases.query(
            **{
                "database_id": self.DATABASE_ID_My_Task,
                "filter": {
                    "and": [
                        {
                            "property": "状態",
                            "status": {"does_not_equal": "完了"},
                        },
                        {
                            "property": "予定日",
                            "date": {"on_or_before": today.isoformat()},
                        },
                    ]
                },
                "sorts": [{"property": "予定日", "direction": "ascending"}],
            }
        )

        items = [
            item["properties"]["タスク名"]["title"][0]["plain_text"]
            for item in data["results"]
        ]
        today_schedule = "\n".join([f"【{i + 1}】{buf}" for i, buf in enumerate(items)])

        return today_schedule


def main() -> None:
    """メイン処理"""
    # 今日の日付（年表示なし、月日はゼロパディング、曜日表示付き）
    DAY_NAME = "月火水木金土日"
    today = date.today()
    mail_body = (
        f"{date.today().month}/{date.today().day}({DAY_NAME[today.weekday()]})\n"
    )

    # 今日の大阪の天気予報（絵文字付き）
    api_forecast = weather_forecast.WeatherAPI()
    api_emoji = weather_to_emoji.WeatherToEmoji()
    forecast = api_forecast.get_weather_forecast(weather_forecast.Prefecture.OSAKA)
    if forecast:
        mail_body += f"{api_emoji.query(forecast.today)} {forecast.today}\n"

    # 今日は何の日？
    api_today_anniversary = today_anniversary.TodayAnniversary()
    anniversary = api_today_anniversary.get_today_anniversary()
    if anniversary:
        mail_body += f"今日は {anniversary} です。\n\n"

    # 今日の予定（リスト）
    mail_body += TodaySchedule().get_today_schedule()
    if mail_body:
        send_line_message.SendLineMessage().send_line_message(mail_body)


if __name__ == "__main__":
    main()
