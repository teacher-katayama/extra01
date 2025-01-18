# -*- coding: utf-8 -*-
"""天気を絵文字に変換する"""

# ライブラリのインポート
from openai import APITimeoutError, OpenAI


class WeatherToEmoji:
    """天気を絵文字に変換する"""

    API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # OpenAI APIキー
    MODEL_NAME = "gpt-4o-mini"  # モデル名

    def __init__(self):
        self.client = OpenAI(api_key=self.API_KEY)
        self.model_name = self.MODEL_NAME

    def query(self, weather: str) -> str:
        """ChatGPTに質問し、回答を得る

        Args:
            weather (str): 天気情報

        Returns:
            str: 絵文字
        """
        if not weather:
            return ""

        messages = [
            {
                "role": "system",
                "content": 'お伝えした天気を絵文字1文字で表現すると何ですか？晴れなら"☀️"、曇りなら"☁️"、雨なら"☔"、雪なら"☃️"と答えて下さい。',
            },
            {"role": "user", "content": weather},
        ]

        try:
            res = self.client.chat.completions.create(
                model=self.model_name, messages=messages, timeout=15.0
            )
        except APITimeoutError:
            return ""

        answer = res.choices[0].message.content

        return answer


if __name__ == "__main__":
    weather = "くもり 所により 夜のはじめ頃 まで 雨"
    api = WeatherToEmoji()
    print(api.query(weather))
