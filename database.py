import os
import sqlite3

file = 'card.s3db'


def connect():
    connector = sqlite3.connect(file)
    cursor = connector.cursor()
    return connector, cursor


def create_table():
    if not os.path.isfile(file):
        try:
            conn, cur = connect()

            cur.execute("""
                CREATE TABLE card (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number TEXT NOT NULL,
                    pin TEXT NOT NULL,
                    balance INTEGER DEFAULT 0
                    )
            """)

            conn.commit()
        except:
            print('deu ruim')


def insert_item(number, pin):
    conn, cur = connect()

    query = f'INSERT INTO card(number,pin) Values ({number}, {pin})'
    cur.execute(query)

    conn.commit()


def is_not_empty() -> bool:
    conn, cur = connect()

    cur.execute('select count(1) from card')

    return cur.fetchone()[0] > 0


def get_data(kind: str, value, *args):
    conn, cur = connect()

    query = f'Select {kind} from card where {kind} = "{value}"'
    for i in range(len(args)):
        query += f' and {args[i][0]} = {args[i][1]}'

    cur.execute(query)

    return cur.fetchone()


def get_balance(card):
    conn, cur = connect()

    query = f'Select balance from card where number = "{card}"'
    cur.execute(query)

    return cur.fetchone()[0]


def update_balance(card, amount):
    conn, cur = connect()

    query = f'update card set balance = balance + {amount} where number = "{card}"'

    cur.execute(query)
    conn.commit()


def close_account(card):
    conn, cur = connect()

    query = f'delete from card where number = "{card}"'

    cur.execute(query)
    conn.commit()
