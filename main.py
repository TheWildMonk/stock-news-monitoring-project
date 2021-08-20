# Required libraries
import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client


# Load .env file
load_dotenv(".env_FILE_PATH/.env")

# Constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Alpha Vantage API Constants
AV_ENDPOINT = "https://www.alphavantage.co/query"
AV_API_KEY = os.getenv("AV_API_KEY")
AV_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "60min",
    "outputsize": "compact",
    "datatype": "json",
    "apikey": AV_API_KEY,
}

# News API Constants
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API")
NEWS_API_PARAMS = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

# Twilio API Constants
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NO = "+123456789"
RECEIVER = "+1234567890"

# Request to Alpha Vantage API and
# retrieve closing stock price of yesterday and day before yesterday.
av_request = requests.get(AV_ENDPOINT, params=AV_PARAMS)
av_request.raise_for_status()
av_data = av_request.json()
recent_date = list(av_data["Time Series (Daily)"].keys())[0]
prev_date = list(av_data["Time Series (Daily)"].keys())[1]
recent_close = round(float(av_data["Time Series (Daily)"][recent_date]["4. close"]))
prev_close = round(float(av_data["Time Series (Daily)"][prev_date]["4. close"]))

# Find out percentage change
stock_price_diff = recent_close - prev_close
percentage_change = round(stock_price_diff/prev_close*100)

# Check whether the stock price increased/decreased by 5%
if percentage_change >= 5 or percentage_change <= -5:

    # Request to News API to retrieve first 3 news of the company
    news_api_request = requests.get(NEWS_API_ENDPOINT, params=NEWS_API_PARAMS)
    news_api_request.raise_for_status()
    news_api_data = news_api_request.json()

    # Retrieve first 3 news of the company
    news = [each_news for each_news in news_api_data["articles"][:3]]
    news_body = ""
    for msg in news:
        news_body += "".join(f"Headline: {msg['title']}\n"
                             f"Brief: {msg['description']}\n\n")

    # Request to Twilio API for sending message to the user
    if stock_price_diff > 0:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
                body=f"{STOCK} 🔺{percentage_change}%\n"
                     f"{news_body}",
                from_=TWILIO_PHONE_NO,
                to=RECEIVER
            )

        print(message.status)
    elif stock_price_diff < 0:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
                body=f"{STOCK} 🔻{abs(percentage_change)}%\n"
                     f"{news_body}",
                from_=TWILIO_PHONE_NO,
                to=RECEIVER
            )

        print(message.status)
    else:
        print("There was no change in stock price today.")
else:
    print("There was no significant change in the stock price.")
