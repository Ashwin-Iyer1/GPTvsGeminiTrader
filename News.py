import requests
import os
from datetime import date
apikey = os.getenv("NEWSAPIKEY")
articles = []
def getTechNews():
    Todaydate = str(date.today())
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&from={Todaydate}&sortBy=popularity&apiKey=" + apikey
    response = requests.get(url)
    data = response.json()
    i=0
    for article in data['articles']:
        if i == 30:
            break
        articles.append(article['title'])
        i += 1
    return articles

getTechNews()
def getArticles():
    return articles

