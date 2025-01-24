# -*- coding: utf-8 -*-
"""天気予報"""

# ライブラリのインポート
import logging
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

import requests
from requests.exceptions import RequestException

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Prefecture(Enum):
    """主要地域コード"""

    TOKYO = "130000"  # 東京都
    AICHI = "230000"  # 愛知県西部
    KYOTO = "260000"  # 京都府南部
    OSAKA = "270000"  # 大阪府
    HYOGO = "280000"  # 兵庫県南部


@dataclass
class WeatherForecast:
    """天気予報データクラス"""

    today: str  # 今日の天気
    tomorrow: Optional[str] = None  # 明日の天気（取得できない場合はNone）
    day_after_tomorrow: Optional[str] = None  # 明後日の天気（取得できない場合はNone）


class WeatherAPI:
    """気象庁天気予報APIクライアント"""

    BASE_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast"
    TIMEOUT = 10

    @staticmethod
    def normalize_text(text: str) -> str:
        """テキストの正規化"""
        return unicodedata.normalize("NFKC", text)

    def get_weather_forecast(self, prefecture: Prefecture) -> Optional[WeatherForecast]:
        """天気予報を取得する

        Args:
            prefecture (Prefecture): 地域コード

        Returns:
            Optional[WeatherForecast]: 天気予報
        """
        url = f"{self.BASE_URL}/{prefecture.value}.json"

        try:
            response = requests.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()

            time_defines = [
                datetime.fromisoformat(time_define)
                for time_define in data[0]["timeSeries"][0]["timeDefines"]
            ]
            weathers = [
                self.normalize_text(weather)
                for weather in data[0]["timeSeries"][0]["areas"][0]["weathers"]
            ]

            today = ""
            tomorrow = None
            day_after_tomorrow = None
            if time_defines[0].date() == datetime.now().date():
                today = weathers[0]
                tomorrow = weathers[1]
                day_after_tomorrow = weathers[2] if len(weathers) > 2 else None
            elif time_defines[0].date() == (datetime.now() - timedelta(days=1)).date():
                today = weathers[1]
                tomorrow = weathers[2] if len(weathers) > 2 else None
                day_after_tomorrow = None

            return WeatherForecast(today, tomorrow, day_after_tomorrow)

        except RequestException as e:
            logger.error(f"API接続エラー: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"データ解析エラー: {e}")
            return None
        except Exception as e:
            logger.error(f"予期せぬエラー: {e}")
            return None


    def get_today_osaka_weather(self) -> Optional[str]:
        """今日の大阪の天気を取得する

        Returns:
            Optional[str]: 今日の大阪の天気
        """
        forecast = self.get_weather_forecast(Prefecture.OSAKA)  # 大阪の天気予報を取得
        if forecast is None:
            return None

        return forecast.today  # 今日の天気を返す


if __name__ == "__main__":
    forecast = WeatherAPI().get_today_osaka_weather()  # 大阪の天気予報を取得
    if forecast is None:
        print("天気予報の取得に失敗しました")
    else:
        print(f"今日の大阪の天気: {forecast}")
