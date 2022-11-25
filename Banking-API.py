import sqlite3
from random import randint

from flask import Flask, request, jsonify  # added to top of file

from flask_cors import CORS  # added to top of file

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

    return inserted_user


# Function for generate random account numbers

def random_Account(n):
    range_start = 10 ** (n - 1)

    range_end = (10 ** n) - 1

    return randint(range_start, range_end)


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


if __name__ == "__main__":
    # app.debug = True
    # app.run(debug=True)
    app.run()  # run app
