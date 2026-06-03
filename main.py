import requests
import smtplib
import os
from dotenv import load_dotenv

#from twilio.rest import Client
#from gi.overrides.Gtk import stock_lookup
load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "TESLA Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}


#GET THE DATA FROM THE STOCK AND PROCESS THE DIFFERENCE
response = requests.get(STOCK_ENDPOINT, stock_params)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
yesterday_data = data_list[0]
yesterday_data_closing = yesterday_data["4. close"]
day_before_data = data_list[1]
day_before_data_closing = day_before_data["4. close"]
print(yesterday_data_closing)
print(day_before_data_closing)
differ = abs(float(yesterday_data_closing)-float(day_before_data_closing))
diff_percent = (differ/float(yesterday_data_closing)*100)
print(f"{round(diff_percent, 2)}%")
if differ > 0:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }
    response_news = requests.get(NEWS_ENDPOINT, news_params)

    articles = response_news.json()["articles"]
    print(articles)
    three_articles = articles[:3]

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

    formated_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formated_articles)
    #TODO 9. - Send each article as a separate message via Twilio.
  #  client = Client(TWILLIO_SID, TWILLIO_AUTH_TOKEN)


    for article in formated_articles:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="jkayabas@gmail.com",
                msg=f"Subject: Tesla stock \n\n {article}")

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

