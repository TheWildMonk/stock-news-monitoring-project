import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv("/Volumes/Workstation/Learning Center/Data Science"
            "/100 Days of Code - Complete Python Pro Bootcamp 2021/Projects/@CREDENTIALS/.env")

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

# Request to Alpha Vantage API and
# retrieve closing stock price of yesterday and day before yesterday.
av_request = requests.get(AV_ENDPOINT, params=AV_PARAMS)
av_request.raise_for_status()
av_data = av_request.json()
recent_date = list(av_data["Time Series (Daily)"].keys())[0]
prev_date = list(av_data["Time Series (Daily)"].keys())[1]
recent_close = round(float(av_data["Time Series (Daily)"][recent_date]["4. close"]))
prev_close = round(float(av_data["Time Series (Daily)"][prev_date]["4. close"]))+60

# Find out percentage change
stock_price_diff = recent_close - prev_close
percentage_change = round(stock_price_diff/prev_close*100)
# print(f"{percentage_change}%")

# Check whether the stock price increased/decreased by 5%
if percentage_change >= 5 or percentage_change <= -5:
    # Request to News API to retrieve first 3 news of the company
    news_api_request = requests.get(NEWS_API_ENDPOINT, params=NEWS_API_PARAMS)
    news_api_request.raise_for_status()
    news_api_data = news_api_request.json()

    # Retrieve first 3 news of the company
    news = [each_news for each_news in news_api_data["articles"][0:3]]


else:
    print("There was no significant change in the stock price.")

# TODO: STEP 3: Use https://www.twilio.com
#  Send a separate message with the percentage change and each article's title and description to your phone number.


# TODO: Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file 
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file 
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
"""
