import yfinance as yf
import schedule
import logging

from datetime import datetime
import time

from postgresql import *

db = DataBase()

data_price = datetime.now()
only_date = data_price.date()

db.create_table_query()

# logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.basicConfig(filename="mylog.log", level=logging.INFO)


def main():
    price = []
    tickers = ['PM']
    for ticker in tickers:
        ticker_yahoo = yf.Ticker(ticker)
        data = ticker_yahoo.history()
        data_close = data['Close'].iloc[-1]
        data_open = data['Open'].iloc[-1]
        data_low = data['Low'].iloc[-1]
        data_high = data['High'].iloc[-1]
        if data_open > 0 and data_close > 0 and data_low > 0 and data_high > 0:
            logging.info('Все переменные положительные')
            price.extend([data_open, data_high, data_low, data_close])
        else:
            logging.info('Произошла ошибка \nзамечено отрицательное значение в датах')

    db.select_query()
    all_date_in_db = (db.cursor.fetchall())
    for max_date_base in all_date_in_db[-1]:
        if max_date_base < only_date:
            db.insert_query(tickers[0], price[0], price[1], price[2], price[3], only_date)
            logging.info('Найдены новые данные и записаны в бд')
        else:
            logging.info('Не найдено новых данных')
            # schedule.every(5).seconds.do(main)
            schedule.every().hour.do(main)


# schedule.every(25).seconds.do(main)
schedule.every().day.at('9:40').do(main)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)

