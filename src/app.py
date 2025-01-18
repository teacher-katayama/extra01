# -*- coding: utf-8 -*-
"""Webアプリのサンプルです"""

# ライブラリのインポート
from datetime import datetime

from flask import Flask, render_template, request
from markupsafe import Markup

import daily_schedule
import omikuji
import today_anniversary
import weather_forecast
import weather_to_emoji

# Flaskのインスタンス化
application = Flask(__name__, static_folder="static", template_folder="templates")


@application.route("/")
@application.route("/index")
def index() -> str:
    """トップページ

    Returns:
        str: レンダリング結果
    """
    return render_template("./index.html")


@application.route("/today_plan", methods=["GET", "POST"])
def today_plan() -> str:
    """今日の予定を表示する

    Returns:
        str: レンダリング結果
    """
    # 今日の日付（曜日表示付き）
    DAY_NAME = "月火水木金土日"
    today_dt = datetime.now()
    today_dt_str = f"{today_dt.strftime('%Y/%m/%d')}({DAY_NAME[today_dt.weekday()]})"

    # 今日の予定（リスト）
    schedules = daily_schedule.DailySchedule().get_today_schedule()

    # 今日の大阪の天気予報（絵文字付き）
    forecast = weather_forecast.WeatherAPI().get_today_osaka_weather()
    weather_osaka = f"{weather_to_emoji.WeatherToEmoji().query(forecast)} {forecast}\n"

    # 今日は何の日？
    anniversary = today_anniversary.TodayAnniversary().get_today_anniversary()

    # おみくじを引く
    if request.method == "POST":
        fortune = omikuji.draw()
        fortune_result = fortune.result.value
        fortune_advice = fortune.advice
    else:  # GET
        fortune_result = ""
        fortune_advice = ""

    return render_template(
        "./today_plan.html",
        date=today_dt_str,
        schedules=schedules,
        weather_area="大阪",
        weather_result=weather_osaka,
        anniversary=anniversary,
        fortune_result=fortune_result,
        fortune_advice=Markup(fortune_advice.replace("\n", "<br>")),
    )
