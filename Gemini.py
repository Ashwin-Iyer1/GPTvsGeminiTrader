import google.generativeai as genai
import News

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_content():
    response = model.generate_content("You are a stock trading bot that analyses the news and based on the current events from the news you predict stock If you were to read the news and read the following, what stocks would you pick for the day. Only return the stock symbols and give me the top 10 you would pick. Return the stock symbols in a list with no numbers or extra characters EX: SPY, APL, NVDA. The news is as follows: " + str(News.getArticles()))
    content_text = response._result.candidates[0].content.parts[0].text
    return content_text

def parse_text(text):
    global stocks
    #remove all \n and - from the text
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace("'", '')
    text = text.replace('"', '')
    text = text.replace(",", '')
    text = text.replace('\n', ' ')
    text = text.replace('-', '')
    stocks = text.split(' ')
    return(stocks)


def main():
    return(parse_text(get_content()))

