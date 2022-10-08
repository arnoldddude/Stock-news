import math
import os
from twilio.rest import Client
import requests
import datetime as dt
import html

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc."
stock_api_key = "412LOAOCBLE7I8C8"
news_api_key = "7de792b03aca4888b6c0e7ca53744a22"
today_date = dt.date.today()
ACC_SID = "AC5e2c60806d7fcb4e1063ceeaa0289cfc"
AUTH_TOKEN = "03e3bfa42368fa22e939e722f16f5dee"
PHONE_NUMBER = "+14582363846"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}

param = {
    "q": COMPANY_NAME,
    "from": str(today_date),
    "sortBy": COMPANY_NAME,
    "apiKey": news_api_key
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


stock_connect = requests.get(url=STOCK_ENDPOINT, params=parameters)
stock_connect.raise_for_status()
data = stock_connect.json()

yesterday_date = today_date - dt.timedelta(days=1)
two_days_ago = yesterday_date - dt.timedelta(days=1)

yesterday_closing_price = data["Time Series (Daily)"][str(yesterday_date)]["4. close"]
closing_price_2days = data["Time Series (Daily)"][str(two_days_ago)]["4. close"]

positive_diff = abs(float(yesterday_closing_price) - float(closing_price_2days))

closing_stock_percentage = round((positive_diff / float(yesterday_closing_price) * 100), 2)

if closing_stock_percentage >= 5:

    news_connect = requests.get(url=NEWS_ENDPOINT, params=param)
    news_connect.raise_for_status()
    data = news_connect.json()
    news_articles = data["articles"][:3]

    news_list_headline = [num["title"] for num in news_articles]
    news_list_brief = [num["description"] for num in news_articles]
    news_list_link = [num["url"] for num in news_articles]

    for num in range(0, len(news_list_link)):
        if float(yesterday_closing_price) > float(closing_price_2days):
            client = Client(ACC_SID, AUTH_TOKEN)
            message = client.messages \
                .create(
                body=f"{STOCK}: 🔺{closing_stock_percentage}%\n"
                     f"Headline: {html.unescape(news_list_headline[num])} (TSLA)?. \n"
                     f"Brief: {html.unescape(news_list_brief[num])}\n"
                     f"Link: {html.unescape(news_list_link[num])}\n",
                from_=PHONE_NUMBER,
                to="+19099400150"
            )
            print(message.status)
        elif float(closing_price_2days) > float(yesterday_closing_price):
            client = Client(str(ACC_SID), str(AUTH_TOKEN))
            message = client.messages \
                .create(
                body=f"{STOCK}: 🔻{closing_stock_percentage}%\n"
                     f"Headline: {html.unescape(news_list_headline[num])} (TSLA)?. \n"
                     f"Brief: {html.unescape(news_list_brief[num])}\n"
                     f"Link: {html.unescape(news_list_link[num])}\n",
                from_=PHONE_NUMBER,
                to="+19099400150"
            )
            print(message.status)





