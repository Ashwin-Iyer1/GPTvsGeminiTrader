
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import requests
import chatGPT
import Gemini
import smtplib
import os
from datetime import datetime
from stockdata import insert_total_values_into_value_table, QueryStock
phonenumber = os.getenv("phonenumber")
Alpaca_API_KEY = os.getenv("Alpaca_API_KEY")
Alpaca_SECRET_KEY = os.getenv("Alpaca_SECRET_KEY")
EMAIL = os.getenv("Email")
PASSWORD = os.getenv("EmailPass")
auth = (EMAIL, PASSWORD)
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(auth[0], auth[1])


headers = {
    "APCA-API-KEY-ID": Alpaca_API_KEY,
    "APCA-API-SECRET-KEY": Alpaca_SECRET_KEY
}

trading_client = TradingClient(Alpaca_API_KEY, Alpaca_SECRET_KEY, paper=True)

def initAcc():
    global account
    account = trading_client.get_account()
    server.sendmail(auth[0], f"{phonenumber}@vtext.com", f'Current portfolio balance: ${account.equity}')

def get_liquid():
    return account.buying_power


def margin():
    balance_change = float(account.equity) - float(account.last_equity)
    server.sendmail(auth[0], f"{phonenumber}@vtext.com", f'Today\'s portfolio balance change: ${balance_change}')
    print(f'Today\'s portfolio balance change: ${balance_change}')


def sellAsset(symbol, qty):
    market_sell_data = MarketOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.GTC
                        )
    submit(market_sell_data)

def buyAsset(symbol, qty):
    market_order_data = MarketOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY
                        )
    print("buying " + str(symbol) + " at " + str(getStockPrice(symbol)) + " " + str(qty))
    submit(market_order_data)

def getStockPrice(symbol):
    url = f'https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest'
    response = requests.get(url, headers=headers)
    return response.json()['trade']['p']


def submit(type):
    trading_client.submit_order(order_data=type)

def getallassets():
    assets = trading_client.get_all_assets()
    return assets

def TableValue():
    val = insert_total_values_into_value_table()
    print(val)
    server.sendmail(auth[0], f"{phonenumber}@vtext.com", str(val))
    

def buy_multiple_eql_amts(stocks, amt, Platform):
    listofbuys = []
    listofPrices = []
    counter = 0
    stockPrices = []
    for stock in stocks:
        stockprice = getStockPrice(stock)
        stockPrices.append(stockprice)
        listofPrices.append(float(amt) / stockprice)
    print(listofPrices)
    for stock in stocks:
        try:
            buyAsset(stock, round(listofPrices[counter], 1))
            QueryStock(stock, round(listofPrices[counter], 1), Platform)
            #print only up to 1 decimal place for amt / stockprice
            listofbuys.append(f'{listofPrices[counter]:.2f} shares of {stock} at {stockPrices[counter]}')
            counter += 1
        except Exception as e:
            if "asset not found" in str(e) or "is not active" in str(e):
                print(f"Skipping {stock} due to error: {e}")
                continue
            else:
                raise e
    server.sendmail(auth[0], f"{phonenumber}@vtext.com", Platform + " bought " + str(stocks))
    print('Using ' + Platform + " bought " + str(listofbuys))

    return listofbuys

def main():
    i = 0
    while i < 10:
        try:
            Gemini_content = Gemini.main()
            print(Gemini_content)
            numstocks = len(Gemini_content)
            buys = buy_multiple_eql_amts(Gemini_content, 3000/numstocks, 'gemini')
            if buys:
                break
        except Exception as e:
            print(f"Gemini Error occurred: {e}")
        i += 1


    i = 0
    while i < 10:
        try:
            OpenAI_content = chatGPT.main()
            print(OpenAI_content)
            numstocks = len(OpenAI_content)
            buys = buy_multiple_eql_amts(OpenAI_content, 3000/numstocks, 'openai')
            if buys:
                break
        except Exception as e:
            print(f"OpenAI Error occurred: {e}")
        i += 1



dt = datetime.now()
if dt.isoweekday() > 5:
    print("It's the weekend, no trading today")
else:
    initAcc()
    margin()
    main()
    TableValue()
    server.quit()


