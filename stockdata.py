import json
import psycopg2
import requests
from decimal import Decimal
import os
Alpaca_API_KEY = os.getenv("Alpaca_API_KEY")
Alpaca_SECRET_KEY = os.getenv("Alpaca_SECRET_KEY")

headers = {
    "APCA-API-KEY-ID": Alpaca_API_KEY,
    "APCA-API-SECRET-KEY": Alpaca_SECRET_KEY
}


databaseurl = os.getenv("SCHEMATOGO_URL")
conn = psycopg2.connect(databaseurl)

def initialize_data_in_database():
    try:
        cursor = conn.cursor()
        # Create a new table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gemini (
                id SERIAL PRIMARY KEY,
                Stock VARCHAR UNIQUE,
                Amt NUMERIC(10, 2),
                TotalSpent NUMERIC(10, 2)
            );
        """)
        # Insert initial data into the table
        conn.commit()
        print("Data initialized in the database.")
    except (Exception, psycopg2.Error) as error:
        print("Error initializing data in the database:", error)
    finally:
        if conn:
            cursor.close()
            conn.close()



def QueryStock(symbol, amt, total_spent, platform):
  """
  Inserts or updates stock data in the specified platform table.

  Args:
      symbol: The stock symbol (e.g., "AAPL").
      amt: The quantity of shares owned.
      total_spent: The total amount spent on the stock.
      platform: The table name (e.g., "gemini").
  """
  try:
      cursor = conn.cursor()
      query = f"""
          INSERT INTO "{platform}" (Stock, Amt, TotalSpent)
          VALUES (%s, %s, %s)
          ON CONFLICT (Stock) DO UPDATE SET
              Amt = EXCLUDED.Amt + "{platform}".Amt,
              TotalSpent = EXCLUDED.TotalSpent
          WHERE "{platform}".Stock = EXCLUDED.Stock;
      """
      cursor.execute(query, (symbol, amt, total_spent))
      conn.commit()
      print("Stock query executed successfully.")
  except (Exception, psycopg2.Error) as error:
      print("Error querying stock:", error)
  finally:
      if cursor:
          cursor.close()


def getStockPrice(symbol):
    url = f'https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest'
    response = requests.get(url, headers=headers)
    return response.json()['trade']['p']

def print_table(platform):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {platform};")
        rows = cursor.fetchall()
        if rows:
            print("ID\tStock\tAmt")
            for row in rows:
                print("{}\t{}\t{}".format(row[0], row[1], row[2]))
        else:
            print("openai table is empty.")
    except (Exception, psycopg2.Error) as error:
        print("Error printing openai table:", error)
    finally:
        if cursor:
            cursor.close()

def remove_row_by_id(row_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Gemini WHERE id = %s;", (row_id,))
        conn.commit()
        print("Row with ID {} removed successfully.".format(row_id))
    except (Exception, psycopg2.Error) as error:
        print("Error removing row:", error)
    finally:
        if cursor:
            cursor.close()



def calculate_total_value_for_all_stocks(platform):
    total_portfolio_value = Decimal(0)
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT Stock, Amt FROM {platform};")
        rows = cursor.fetchall()
        for row in rows:
            stock_symbol, amount = row[0], row[1]
            current_price = Decimal(str(getStockPrice(stock_symbol)))
            total_value = amount * current_price
            total_portfolio_value += total_value
        return total_portfolio_value

    except (Exception, psycopg2.Error) as error:
        print("Error calculating total value for all stocks:", error)
    finally:
        if cursor:
            cursor.close()


def insert_total_values_into_value_table():
    try:
        # Calculate total value for OpenAI
        openai_value = calculate_total_value_for_all_stocks("openai")
        
        # Calculate total value for Gemini
        gemini_value = calculate_total_value_for_all_stocks("gemini")
        
        # Insert total values into the value table
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO value (id, openai, gemini)
            VALUES (CURRENT_TIMESTAMP, %s, %s);
        """, (openai_value, gemini_value))
        conn.commit()
        print("Total values inserted into value table successfully.")
        return ("OpenAI Value: " + str(openai_value) + " Gemini Value: " + str(gemini_value))
    except (Exception, psycopg2.Error) as error:
        print("Error inserting total values into value table:", error)
    finally:
        if cursor:
            cursor.close()


