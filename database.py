import sqlite3

connection = sqlite3.connect('bank.db')

print("connect to the database server")

connection.execute('CREATE TABLE Users(Account_ID INT(10) PRIMARY KEY,User_Name TEXT, Money_Amount TEXT, Password TEXT, Email TEXT);')

print("Table Created")

connection.close()