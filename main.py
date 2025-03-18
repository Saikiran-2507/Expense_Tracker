import sys
from user import * 
from transactions import *
from pyfiglet import Figlet


def main():
    f = Figlet(font='slant')
    print(f.renderText('Finance Tracker'))
    while True:
        print("\n1. Login       2. Sign up       3. Exit")
        try:
            choice = int(input("What do you want to do? "))
        except ValueError:
            print("Enter a valid choice\n")
        else:
            if choice not in range(1, 4):
                print("Enter a valid choice\n")
                continue
            match choice:
                case 1:
                    while True:
                        user_id = input("User_id: ")
                        password = input("Password: ")
                        if Login_Manager.login(user_id, password) == 0:
                            break
                        else:
                            continue
                case 2:
                    name = input("Name: ")
                    user_id = input("User_id: ")
                    password = input("Password(Max 8 characters): ")
                    new_user = user.User(name, user_id, password)
                    User.add_new_user(new_user)
                    Login_Manager.current_user = new_user
                case 3:
                    print("-----------------------------------------------------")
                    print("                      Thank You                      ")
                    print("-----------------------------------------------------")
                    sys.exit()
        while (True):
            print("""\n1. Add a Transaction        2. View all Transactions
3. Edit a Transaction       4. Delete a Transaction
5. Delete Account           6. Change Login Password   
7. Logout""")
            try:
                choice = int(input("What do you want to do? "))
            except ValueError:
                print("Enter a valid choice\n")
            else:
                if choice not in range(1, 8):
                    print("Enter a valid choice\n")
                    continue
                match choice:
                    case 1:
                        Date = input("Date (yyyy-mm-dd): ")
                        Type = input("Transaction Type (income or expense): ")
                        Amount = input("Amount (in INR): ")
                        Category = input("Category: ")
                        Description = input("Description: ")
                        try:
                            t = Transaction(Date, Type, Amount, Category, Description)
                        except Exception as e:
                            errors = []
                            errors.append(str(e))
                            while errors:
                                if "****Invalid Date****" in errors:
                                    while(True):
                                        print("****Invalid Date****")
                                        try:
                                            Date = input("Enter valid date (yyyy-mm-dd): ")
                                            t = Transaction(Date, Type, Amount, Category, Description)
                                            errors.remove("Invalid Date")
                                            break
                                        except Exception as d:
                                            if str(d) == "****Invalid Date****":
                                                continue
                                            else:
                                                errors.remove("****Invalid Date****")
                                                errors.append(str(d))
                                                break
                                if "****Invalid Type****" in errors:
                                    while(True):
                                        print("****Invalid Type****\nShould be either income or expense: ")
                                        try:
                                            Type = input("Enter valid type: ")
                                            t = Transaction(Date, Type, Amount, Category, Description)
                                            errors.remove("****Invalid Type****")
                                            break
                                        except Exception as t:
                                            if str(t) == "****Invalid Type****":
                                                continue
                                            else:
                                                errors.remove("****Invalid Type****")
                                                errors.append(str(t))
                                                break
                                if "****Invalid Amount****" in errors:
                                    while(True):
                                        print("****Invalid Amount****\nAmount should be a non-negative number: ")
                                        try:
                                            Amount = input("Enter valid amount: ")
                                            t = Transaction(Date, Type, Amount, Category, Description)
                                            errors.remove("****Invalid Amount****")
                                            break
                                        except Exception as a:
                                            if str(a) == "****Invalid Amount****":
                                                continue
                                            else:
                                                errors.remove("****Invalid Amount****")
                                                errors.append(str(a))
                                                break
                        Transaction_Manager.add_transaction(t, Login_Manager.current_user)
                    case 2:
                        Transaction_Manager.view_transactions(Login_Manager.current_user)
                    case 3:
                        if Transaction_Manager.view_transactions(Login_Manager.current_user) != 0:
                            while (True):
                                edit_index = int(input("Enter Transaction_id of the transaction to edit: "))
                                try:
                                    et = Transaction_Manager.get_transaction_object(edit_index)
                                    break
                                except Exception:
                                    print("***Invalid Transaction_id***")
                                    continue
                            while True:
                                print("1. Date   2. Type   3. Amount   4. Category   5. Description")
                                edit_attr = int(input("Which attribute do you want to edit: "))
                                if edit_attr not in range(1, 6):
                                    print("****Invalid Attribute****")
                                    continue
                                else:
                                    match edit_attr:
                                        case 1:
                                            while True:
                                                try:
                                                    value = et.date = input("Date (yyyy-mm-dd): ")
                                                    break
                                                except Exception as e:
                                                    print(f"{e}\nValid date format is yyyy-mm-dd")
                                                    continue
                                        case 2:
                                            while True:
                                                try:
                                                    value = et.type = input("Transaction Type (income or expense): ")
                                                    break
                                                except Exception as e:
                                                    print(f"{e}\nShould be either income or expense")
                                                    continue
                                        case 3:
                                            while True:
                                                try:
                                                    value = et.amount = input("Amount (in INR): ")
                                                    break
                                                except Exception as e:
                                                    print(f"{e}\nAmount should be a non-negative number")
                                                    continue
                                        case 4:
                                            value = et.category = input("Category: ")
                                        case 5:
                                            value = et.description = input("Description: ")
                                    break
                            d = {1 : "Date", 2 : "Type", 3 : "Amount", 4 : "Category", 5 : "Description"}
                            Transaction_Manager.edit_transaction(edit_index, d[edit_attr], value)
                    case 4:
                        if Transaction_Manager.view_transactions(Login_Manager.current_user) != 0:
                            while (True):
                                del_index = int(input("Enter Transaction_id of the transaction you want to delete: "))
                                try:
                                    Transaction_Manager.delete_transaction(del_index)
                                    break                            
                                except Exception:
                                    print("****Invalid Index****")
                                    continue
                    case 5:
                        user.User.delete_user(Login_Manager.current_user)
                        break
                    case 6:
                        val = input("Enter new password: ")
                        user.User.update_user_password(Login_Manager.current_user, val)
                    case 7:
                        Login_Manager.logout()
                        break


if __name__ == "__main__":
    main()