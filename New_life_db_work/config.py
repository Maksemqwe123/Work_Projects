import psycopg2

host = 'localhost'
user = 'postgres'
password = '1234'
db_name = 'work'

connection = psycopg2.connect(
    user=user,
    password=password,
    host=host,
    database=db_name
)
