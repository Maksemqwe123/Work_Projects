# -*- coding: utf-8 -*-

import undetected_chromedriver

from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By

from creation_files_and_folders import files_path_binance, binance_tickers, csv
import time

Open = []
Max = []
Min = []
Close = []


class SeleniumBinance:
    def __init__(self):
        self.binance_tickers = binance_tickers
        self.Open = Open
        self.Max = Max
        self.Min = Min
        self.Close = Close

        self._get_html()

    def _get_html(self):
        for ticker in binance_tickers:
            driver = undetected_chromedriver.Chrome()
            driver.get(f"https://www.binance.com/ru/trade/{ticker}?_from=markets&theme=dark&type=isolated")
            html_source = driver.page_source

            self._get_info(driver, html_source)

    def _get_info(self, driver, html_source):
        pages_info = BeautifulSoup(html_source, 'html.parser')
        close_advertisement = driver.find_element(By.CLASS_NAME, "css-4rbxuz")
        close_advertisement.click()
        time.sleep(3)

        price_open = pages_info.find("div", class_='chart-title-indicator-container').find("span", key="o")
        Open.append(price_open.text)

        price_max = pages_info.find("div", class_='chart-title-indicator-container').find("span", key="h")
        Max.append(price_max.text)

        price_min = pages_info.find("div", class_='chart-title-indicator-container').find("span", key="l")
        Min.append(price_min.text)

        price_close = pages_info.find("div", class_='chart-title-indicator-container').find("span", key="c")
        Close.append(price_close.text)

        all_tickers_and_files_path = (list(zip(Open, Max, Min, Close, files_path_binance)))

        self._file_add_data(all_tickers_and_files_path)

        driver.close()
        driver.quit()

    def _file_add_data(self, all_tickers_and_files_path):
        for ticker_and_path in all_tickers_and_files_path:  # A loop for writing data to files and passing the write path to a file
            with open(ticker_and_path[4], 'w') as file:
                writer = csv.writer(file)
                writer.writerow(ticker_and_path[0:4])


if __name__ == "__main__":
    SeleniumBinance()
