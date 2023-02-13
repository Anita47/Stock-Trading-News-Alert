import requests
from twilio.rest import Client 
STOCK_NAME="TSLA"
COMPANY_NAME="Tesla Inc"
STOCK_ENDPOINT='https://www.alphavantage.co/query'
NEWS_ENDPOINT='https://newsapi.org/v2/everything'
STOCK_API_KEY='FDPH9XKDDFE9GHTY'
NEWS_API_KEY='db582a82468946ffbd6f59cf65240023'
TWILIO_SID='ACcee0c167d1650b1eb86f00daf2e22179'
TWILIO_AUTH_TOEKN='21e6f234eac9966c2ec87b0941f3243e'

stock_params={
    "funcation":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK_NAME,
    "apikey": STOCK_API_KEY,
    }
#response=requests.get(STOCK_ENDPOINT,params=stock_params)
response=requests.get(url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=TSLA&apikey=FDPH9XKDDFE9GHTY')


data=response.json()['Time Series (Daily)']
data_list=[value for (key,value) in data.items()]


yesterday_data=data_list[0]
yesterday_closing_price=yesterday_data['4. close']



day_before_yesterday_data=data_list[1]
day_before_yesterday_closing=day_before_yesterday_data['4. close']

difference=abs(float(yesterday_closing_price)-float(day_before_yesterday_closing))
diff_percent=(difference/float(yesterday_closing_price))*100


if diff_percent>5:
    news_params={
        'apikey':NEWS_API_KEY,
        'qInTitle':COMPANY_NAME,
        }
    news_response=requests.get(NEWS_ENDPOINT,params=news_params)
    articles=news_response.json()['articles']
    three_articles=articles[:3]
    print(three_articles)

    formatted_articles=[f"Headline: {article['title']}.\nBrief:{article['description']}" for article in three_articles]

    client=Client(TWILIO_SID,TWILIO_AUTH_TOEKN)
    for article in formatted_articles:
        message=client.messages.create(
            body=article,
            from_="+12342241648",
            to="+917011085656"
            )
print(str(diff_percent)+'%')

print(yesterday_closing_price)
print(day_before_yesterday_closing)
print(difference)

