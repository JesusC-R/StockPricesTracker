import requests
import datetime
import smtplib
import random
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# ------------------------- TIME --------------------------- #

yesterday = str(datetime.datetime.today() - datetime.timedelta(days=1))[:10]
day_before_yesterday = str(datetime.datetime.today() - datetime.timedelta(days=2))[:10]

# ------------------------- STOCK -------------------------- #

STOCK_API_KEY = 'Q0YR117F505IOQLH'
STOCK_PARAMS = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': STOCK_API_KEY
}

response = requests.get(url='https://www.alphavantage.co/query?', params=STOCK_PARAMS)
response.raise_for_status()
data = response.json()

yesterday_change = float(data['Time Series (Daily)'][yesterday]['4. close'])
day_before_yesterday_change = float(data['Time Series (Daily)'][day_before_yesterday]['4. close'])

difference_change = abs(round(yesterday_change - day_before_yesterday_change, 2))
percentage = round(difference_change / yesterday_change * 100, 2)


# ------------------------- NEWS -------------------------- #

NEWS_API_KEY = 'ef7fdbe9f16540bf87d6030a5617c477'
NEWS_PARAMS = {
    'q': 'Tesla',
    'from': yesterday,
    'apiKey': 'ef7fdbe9f16540bf87d6030a5617c477'
}

response = requests.get(url='https://newsapi.org/v2/everything', params=NEWS_PARAMS)
response.raise_for_status()
data = response.json()
n = data['articles']

five_news = [i for i in n[:5]]

# ------------------------- SEND EMAIL ---------------------------- #

# if percentage > 5:
#     with smtplib.SMTP('smtp@gmail.com') as connection:
#         connection.starttls()
#         connection.login(user='silentcoder56@gmail.com', password='coding4U')
#         connection.sendmail(from_addr='silentcoder56@gmail.com',
#                             to_addrs='jesuscuevasrodarte@gmail.com',
#                             msg=f'Subject: Tesla Stock\n\n'
#                                 f'The value of the TSLA stock has increased {percentage}.\n\n{random.choice(three_news)}')
# elif percentage < -5:
#     with smtplib.SMTP('smtp@gmail.com') as connection:
#         connection.starttls()
#         connection.login(user='silentcoder56@gmail.com', password='coding4U')
#         connection.sendmail(from_addr='silentcoder56@gmail.com',
#                             to_addrs='jesuscuevasrodarte@gmail.com',
#                             msg=f'Subject: Tesla Stock\n\n'
#                                 f'The value of TSLA stock has decreased {percentage}.\n\n{random.choice(three_news)}')


# ----------------------- SEND SMS ---------------------- #

account_sid = 'AC9e5950b7340450514dd89e85552031a6'
auth_token = 'faa3399bd8e9d0e262d35848633a57b9'

random_news = random.choice(five_news)
if percentage < 5:
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=f'The value of TSLA stock has decreased ▼ {percentage}%.'
                                          f'\n\n{random_news["description"]}\n\nsee more {random_news["url"]}',
                                     from_='+14159385765',
                                     to='+14246751559')
    print(message.status)

else:
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=f'The value of the TSLA stock has increased ▲ {percentage}%.'
                                          f'\n\n{random_news["description"]}\n\nsee more {random_news["url"]}',
                                     from_='+14159385765',
                                     to='+14246751559')
    print(message.status)
    
