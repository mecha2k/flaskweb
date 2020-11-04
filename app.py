from flask import Flask, render_template, request, make_response
from forex_python.converter import CurrencyRates
from dotenv import load_dotenv
import feedparser
import datetime
import json
import urllib
import os

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

app = Flask(__name__)

DEFAULTS = {"publication": "bbc", "city": "Seoul, KR", "currency_from": "USD", "currency_to": "KRW"}

RSS_FEEDS = {
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "cnn": "http://rss.cnn.com/rss/edition.rss",
    "fox": "http://feeds.foxnews.com/foxnews/latest",
    "iol": "http://www.iol.co.za/cmlink/1.640",
}


def get_rate(frm, to):
    return CurrencyRates().get_rate(frm, to)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed["entries"]


def get_weather(query):
    load_dotenv(verbose=True)
    owm = OWM(os.getenv("API_KEY"))
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(query)
    w = observation.weather

    weather = None
    if w is not None:
        weather = {
            "description": w.detailed_status,
            "temperature": w.temperature("celsius"),
            "city": query,
        }
    return weather


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


@app.route("/")
def home():
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    city = get_value_with_fallback("city")
    weather = get_weather(city)
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate = get_rate(currency_from, currency_to)
    currencies = ["USD", "KRW", "EUR", "GBP"]

    response = make_response(
        render_template(
            "home.html",
            articles=articles,
            weather=weather,
            currency_from=currency_from,
            currency_to=currency_to,
            rate=rate,
            currencies=sorted(currencies),
        )
    )
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
