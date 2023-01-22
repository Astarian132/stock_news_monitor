import requests
import dotenv
from datetime import datetime, timedelta
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
alphavantage_api_key = dotenv.dotenv_values("python.env").get('alphavantage_api_key')
newsapi_key = dotenv.dotenv_values("python.env").get('newsapi_key')
DAYS_BEFORE = 2
main_email = "mipysmtp@gmail.com"
mail_password = dotenv.dotenv_values("python.env").get("mail_password")
secondary_email = "mipysmpt@gmail.com"



params = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'outputsize': 'compact',
    'apikey': alphavantage_api_key
}

news_params = {
    'apiKey': newsapi_key,
    'q': COMPANY_NAME,
    'pageSize': 3,
    'page': 1

}

stock_response = requests.get('https://www.alphavantage.co/query', params=params)
try:
    closing_yesterday = stock_response.json()['Time Series (Daily)'][str(datetime.now().date() - timedelta(days=DAYS_BEFORE))]['4. close']
    closing_day_before = stock_response.json()['Time Series (Daily)'][str(datetime.now().date() - timedelta(days=DAYS_BEFORE+1))]['4. close']
except KeyError:
    print('Stock market was closed during this period, try again.')
else:
    closing_bilance = round(((float(closing_yesterday) - float(closing_day_before)) / float(closing_day_before) * 100),2)
    print(f"{closing_bilance}% diffrence" )
    if abs(closing_bilance) >= 5:
        news_on_stock = requests.get('https://newsapi.org/v2/top-headlines', params=news_params).json()['articles']
        for i in news_on_stock:
            encoded_msg = str(f"""Subject:Stock allert! {COMPANY_NAME}\n\n{COMPANY_NAME} stock prices went {'up' if closing_bilance > 0 else 'down'} by {closing_bilance}% \
            \nCheck the latest details below: \n{i['title']}\n{i['description']} \
                            \nfind more at:{i['url']}""").encode('utf-8', 'ignore')
            with smtplib.SMTP("smtp.gmail.com", port=587) as main_connection:
                main_connection.starttls()
                main_connection.login(user=main_email, password=mail_password)
                main_connection.sendmail(from_addr=main_email,
                to_addrs=secondary_email,
                msg= encoded_msg)



