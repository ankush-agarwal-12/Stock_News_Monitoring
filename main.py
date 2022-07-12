import requests
from datetime import datetime, timedelta
import pandas as pd
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_kEY = "UNF3ISGZRQPCRK5E"

Parameter = {
    "function" : "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_kEY,
}
response = requests.get(url = STOCK_ENDPOINT,params=Parameter)
data = response.json()['Time Series (Daily)']
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_stock_price = data_list[0]['4. close']

day_before_yesterday_data = data_list[1]
dby_closing_stock_price = data_list[1]["4. close"]

diff_price = float(yesterday_stock_price)-float(dby_closing_stock_price)
pos_diff_price = abs(diff_price)
print(pos_diff_price)
up_down = None
if diff_price<0:
    up_down = "📉"
else:
    up_down = "📈"

diff_percentage = (diff_price/float(dby_closing_stock_price))*100
print(diff_percentage)

if(abs(diff_percentage)>5):
    print("Get News")

NEWS_API_KEY = 'cf043ff266cd4dbe9f9394682eb5f466'
news_parameretr = {
    'qInTitle': STOCK_NAME,
    'apikey': NEWS_API_KEY,
    'language': 'en',
}
new_data = requests.get(url = "https://newsapi.org/v2/everything", params=news_parameretr)
Articles = new_data.json()["articles"]
if len(Articles)>3:
    news_content = Articles[:3]
else:
    news_content = Articles[:len(Articles)]

content = [f"{STOCK_NAME}: {up_down} {abs(diff_percentage)}%\nHeadline: {dict['title']}. \nBrief: {dict['description']} \nURL: {dict['url']}\n" for dict in news_content ]
print(content[0])
from twilio.rest import Client
account_sid = "AC7ba5df540585315bb5f9cf5ba7c91130"
auth_token = '92e00dbed3957749a1226f437f4d648d'
client = Client(account_sid, auth_token)
for info in content:
    message = client.messages.create(
                     body=info,
                     from_='+18456606948',
                     to='+917004252404'
                 )
    print(info)
    print("Message sent")

