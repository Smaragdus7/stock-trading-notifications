import requests
import os
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "virtual twilio number"
VERIFIED_NUMBER = "own phone number verified with Twilio"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STCKEP_API = os.environ.get("STCKEP_API_KEY")
NWSEP_API = os.environ.get("NWSEP_API_KEY")
TWILIO_SID = "TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "TWILIO AUTH TOKEN"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STCKEP_API,
}

parameters_news = {
    "apiKey": NWSEP_API,
    "qInTitle": COMPANY_NAME,
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_close = yesterday_data["4. close"]

df_yesterday_data = data_list[1]
df_yesterday_close = df_yesterday_data["4. close"]

positive_diff = float(yesterday_close) - float(df_yesterday_close)
up_down = None
if positive_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((positive_diff / float(yesterday_close)) * 100)

if diff_percent > 5:
    response_news = requests.get(NEWS_ENDPOINT, params=parameters_news)
    response_news.raise_for_status()
    data_news = response_news.json()["articles"]
    three_articles = data_news[:3]

    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in three_articles]
    print(formatted_articles)
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
