import sqlite3

from random import randint

from flask import Flask, request, jsonify

from flask_cors import CORS

import main


# function for database creation

def connect_to_db():
    conn = sqlite3.connect('bank.db')

    return conn


# that function return user details when you pass user id

def get_user_by_id(user_id):
    user = {}

    try:
        conn = connect_to_db()

        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        cur.execute("SELECT * FROM Users WHERE Account_ID = ?", (user_id,))

        row = cur.fetchone()

        # convert row object to dictionary

        user["Account_Number"] = row["Account_ID"]

        user["Name"] = row["User_Name"]

        user["Account_Balance"] = row["Money_Amount"]

        user["Email_Address"] = row["Email"]

    except:
        user = {}

    return user


def authentication(account_id, pin_code):
    conn = sqlite3.connect('bank.db')

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("SELECT * FROM Users WHERE Account_ID = ? AND Password = ?", (account_id, pin_code))

    row = cur.fetchone()

    if row != None:

        return 1

    else:

        return 0


# the money deposit part

def money_deposit(user):
    updated_user = {}
    try:
        conn = connect_to_db()

        cur = conn.cursor()

        balance = money_process(user["account_number"], user["amount"])

        cur.execute("UPDATE Users SET Money_Amount = ? WHERE Account_ID = ?", (balance, user["account_number"]))

        conn.commit()

        updated_user = get_user_by_id(user["account_number"])

    except:

        conn.rollback()

        updated_user = {}

        return 0

    finally:
        conn.close()

    return updated_user


# that function can process money

def money_process(account_id, amount):

    conn = sqlite3.connect('bank.db')

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("SELECT * FROM Users WHERE Account_ID = ?", (account_id,))

    row = cur.fetchone()

    money = int(row["Money_Amount"]) + int(amount)

    return str(money)


# that function can create user accounts when pass username, password and email

def create_account(user):
    inserted_user = {}

    Account_Number = random_Account(10)

    Account_Balance = 0

    try:
        conn = connect_to_db()

        cur = conn.cursor()

        cur.execute("INSERT INTO Users (Account_ID, User_Name, Money_Amount, Password, Email) VALUES (?, ?, ?, ?, ?)",
                    (Account_Number, user['name'], Account_Balance, user['password'], user['email']))

        conn.commit()

        inserted_user = get_user_by_id(cur.lastrowid)

    except:
        conn().rollback()

    finally:
        conn.close()

    return Account_Number


# Function for generate random account numbers

def random_Account(n):
    range_start = 10 ** (n - 1)

    range_end = (10 ** n) - 1

    return randint(range_start, range_end)


def money_withdrawProcess(account_id, amount):

    conn = sqlite3.connect('bank.db')

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("SELECT * FROM Users WHERE Account_ID = ?", (account_id,))

    row = cur.fetchone()

    money = int(row["Money_Amount"])

    if money > int(amount) + 1000:

        balance = money - int(amount) + 1000

    else:

        balance = 0

    return balance


def money_withdraw(user):
    updated_user = {}

    user_id = user["user_id"]

    password = user["password"]

    amount = user["money"]

    authentication_account = authentication(user_id, password)

    try:
        if(authentication_account == 1):

            get_balance = money_withdrawProcess(user_id, amount)

            if(get_balance == 0):

                return "Insufficient Account Balance For Withdraw Money"

            else:
                try:
                    conn = connect_to_db()

                    cur = conn.cursor()

                    cur.execute("UPDATE Users SET Money_Amount = ? WHERE Account_ID = ?", (get_balance, user_id))

                    conn.commit()

                    updated_user = get_user_by_id(user["user_id"])

                except:
                    conn.rollback()

                    updated_user = {}

                    return "Application Logical Error"

                finally:
                    conn.close()

                return updated_user
        else:

            return "User Can't Be Authenticated, Try Again"
    except:

        return "Logical Error"




app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(main.get_users())


@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))


@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(create_account(user))


@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(money_deposit(user))


@app.route('/api/users/withdraw', methods=['PUT'])
def api_update_withdraw():
    user = request.get_json()
    return jsonify(money_withdraw(user))


if __name__ == "__main__":
    # app.debug = True
    # app.run(debug=True)
    app.run()  # run app
