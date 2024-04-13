import requests


apikey = os.getenv("NEWSAPIKEY")
articles = []
def getTechNews():
    url = 'https://newsapi.org/v2/top-headlines?country=us&category=business&from=2024-03-13&sortBy=popularity&apiKey=' + apikey
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