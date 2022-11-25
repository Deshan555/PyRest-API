import sqlite3


def connect_to_db():
    conn = sqlite3.connect('bank.db')

    return conn


def insert_user(user):
    inserted_user = {}

    try:
        connection = connect_to_db()

        cur = connection.cursor()

        SQL_Query = ("INSERT INTO Users (Account_ID, User_Name, Money_Amount) VALUES (?, ?, ?);", (user['account_id'],
                                                                                                 user['name'],
                                                                                                 user['balance']))

        cur.execute(SQL_Query)

        connection.commit()

        inserted_user = get_user_by_id(cur.lastrowid)

    except:
        connection().rollback()

    finally:
        connection.close()

    return inserted_user


def get_users():
    users = []

    try:

        connection = connect_to_db()

        connection.row_factory = sqlite3.Row

        cur = connection.cursor()

        cur.execute("SELECT * FROM Users")

        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {"Account_ID": i["Account_ID"], "Name": i["User_Name"], "Money": i["Money_Amount"]}

            users.append(user)

    except:
        users = []

    return users


def get_user_by_id(user_id):
    user = {}

    try:
        connection = connect_to_db()

        connection.row_factory = sqlite3.Row

        cur = connection.cursor()

        SQL_Query = ("SELECT * FROM Users WHERE Account_ID = {id};". int(user_id))

        print(SQL_Query)

        cur.execute(SQL_Query)

        row = cur.fetchone()

        # convert row object to dictionary
        user["user_id"] = row["Account_ID"]

        user["name"] = row["User_Name"]

        user["balance"] = row["Money_Amount"]

    except:
        user = {}

    return user



