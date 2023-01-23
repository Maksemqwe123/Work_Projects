from config import *


class DataBase:
    def __init__(self):
        self.connection = connection
        self.cursor = connection.cursor()

    def create_table_query(self):
        with self.connection:
            return self.cursor.execute("""CREATE TABLE IF NOT EXISTS price_history (
                        TICKET_ID SERIAL PRIMARY KEY,
                        TICKET VARCHAR(64) NOT NULL,
                        PRICE_OPEN DOUBLE PRECISION,
                        PRICE_HIGH DOUBLE PRECISION,
                        PRICE_LOW DOUBLE PRECISION,
                        PRICE_CLOSE DOUBLE PRECISION,
                        PRICE_DATE date UNIQUE)""")

    def insert_query(self, ticket, price_open, price_high, price_low, price_close, price_date):
        with self.connection:
            return self.cursor.execute(
                """INSERT INTO price_history (TICKET, PRICE_OPEN, PRICE_HIGH, PRICE_LOW, PRICE_CLOSE, PRICE_DATE)
                 VALUES (%s, %s, %s, %s, %s, %s)""",
                (ticket, price_open, price_high, price_low, price_close, price_date))

    def select_query(self):
        with self.connection:
            return self.cursor.execute(
                """select distinct on (1)
                price_date
                from price_history"""
            )
