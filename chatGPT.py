from openai import OpenAI
import News
import os

GPTApikey = os.getenv("GPTAPIKEY")

client = OpenAI(
    api_key=GPTApikey
)
def get_response():
  global completion_content
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": "You are a stock trading bot that analyses the news and based on the current events from the news you predict stock. Give me the stock symbol, not name"
      },
      {
        "role": "user",
        "content": "If you were to read the news and read the following, what stocks would you pick for the day. Only return the stock symbols and give me the top 10 you would pick. Return the stock symbols in a list with no numbers or extra characters EX: SPY, APL, NVDA"
      },
      {
        "role": "user",
        "content": str(News.getArticles())
      }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  completion_content = response.choices[0].message.content
  return completion_content

def strip_text(text):
  text = text.replace('[', '')
  text = text.replace(']', '')
  text = text.replace("'", '')
  text = text.replace('"', '')
  text = text.replace(",", '')
  text = text.replace('\n', ' ')
  text = text.replace('-', '')
  text = text.upper()
  stocks = text.split(' ')
  return stocks


def main():
  get_response()
  return strip_text(completion_content)

