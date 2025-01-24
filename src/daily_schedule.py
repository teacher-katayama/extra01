# -*- coding: utf-8 -*-
"""本日の予定をメールで送信する
Note:
    Notionから情報を取得する
        database_id = 「Task DB」
        状態 = 「完了」以外
        予定日 = 今日以前
        並び替え「予定日」の昇順
"""

# ライブラリのインポート
from datetime import date

from notion_client import Client


class DailySchedule:
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

    def get_today_schedule(self) -> list:
        """本日の予定を取得する

        Returns:
            list: 本日の予定

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

        return [f"【{i + 1}】{buf}" for i, buf in enumerate(items)]


if __name__ == "__main__":
    daily_schedule = DailySchedule()
    print("\n".join(daily_schedule.get_today_schedule()))
