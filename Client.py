import functions


def option_function():
    print("WelCome To Smart Transfer\n 1.Create A New Account\n 2.Request Your Account Info\n 3.Deposit Money\n "
          "4.Withdraw Money\n 5.Transfer Money To Another Account")

    option = int(input("\nWhat are You Want To Do? : "))

    if (option > 0) & (option < 6):

        if option == 1:
            functions.create_Account()

    else:

        print('wrong argument')

        option_function()


option_function()
