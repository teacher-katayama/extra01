# -*- coding: utf-8 -*-
"""LINEにメッセージを送信する"""

# ライブラリのインポート
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)


class SendLineMessage:
    """LINEにメッセージを送信するクラス"""

    CHANNEL_ACCESS_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    USER_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    def __init__(self):
        """コンストラクタ"""
        self.configuration = Configuration(access_token=self.CHANNEL_ACCESS_TOKEN)

    def send_line_message(self, msg: str) -> None:
        """LINEにメッセージを送信する

        Args:
            msg (str): 送信するメッセージ
        """

        # メッセージを送信
        with ApiClient(self.configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            message = TextMessage(text=msg)
            push_message_request = PushMessageRequest(
                to=self.USER_ID, messages=[message]
            )
            messaging_api.push_message(push_message_request)
