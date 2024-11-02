from .password import Password
from .db import Database
import datetime
from pprint import pprint
import os


Database = Database()


def main():
    current_user = None
    re_run = True
    print("Welcome to Password Manager(pm).")
    print("What things make a password strong.")
    print("    1. A password must contain one Capital Word.")
    print("    2. A password must contain 2-3 special characters.")
    print("    3. A password must contain 2-3 numbers.")
    print("run the command pm help to know how pm(password manager) works.")

    while re_run:
        print(datetime.datetime.now().strftime("%w-%d-%Y: %H-%M-%S"), end=" ")
        command_input = input(">>> ")

        if command_input.split(" ")[0] != "pm":
            print(
                "Error in syntax for password manager command line! Add pm before every command."
            )
            continue

        command = command_input.split(" ")[1]
        try:
            command_type = command_input.split(" ")[2]
        except IndexError:
            command_type = None

        try:
            additional = command_input.split(" ")[3]
        except IndexError:
            additional = None

        if command == "help":
            print("write pm before every command to proceed")
            print("Enter generate in enter password section to generate password.")
            print(
                "Run command --- set user ----------- to set the user in the password manager."
            )
            print(
                "Run command --- get user {user_name}----------- to login the user in the password manager."
            )
            print(
                "Run command --- save password----------- to save the password in the password manager."
            )
            print(
                "Run command --- view password----------- to show the password in the password manager saved by you."
            )
            print(
                "Run command --- del password {password_id}----------- to delete the password in the password manager."
            )
            print(
                "Run command --- edit password {password_id}----------- to edit the password in the password manager."
            )
            print(
                "Run command --- clear----------- to clear the screen in the password manager."
            )
            print("Run command --- exit----------- to exit the password manager.")

        elif command == "set" and (command_type == " " or command_type == "user"):
            user = input("Enter your name.(It must be unique): ")
            user_password = input("Enter your password: ")

            Password_User = Password(user_password)
            if user_password == "generate":
                Password_User.generate()
                accept_generated_password = input(
                    f"The generated password is {Password_Saver.password}. Do you wnat to accept it. (yes/no): "
                )
                if accept_generated_password.lower() == "no":
                    accepted_password = input("Enter your own password: ")
                    Password_Saver.password = accepted_password

            strength_status = Password_User.status_declaration()

            if strength_status == "weak" or strength_status == "moderate":
                re_enter = input(
                    f"Your password is {strength_status}. Do you want to re enter the password. (yes/no): "
                ).lower()
                if re_enter == "yes":
                    user_password = input("Re Enter your password: ")

            result_user_class = Database.upload_user_details(
                user_name=user, user_password=user_password
            )
            try:
                current_user = result_user_class[1][1]
            except:
                current_user = None

            print(result_user_class[0]["message"])

        elif command == "get" and command_type == "user":
            if additional == None:
                print("Please give your username.")
                continue

            existed_user_password = input("Enter the saved password: ")
            result_get_user = Database.get_user(
                name=additional, password=existed_user_password
            )
            print(result_get_user[0]["message"])

            try:
                current_user = result_get_user[1]
            except:
                current_user = None

        elif command == "save" and command_type == "password":
            if not current_user:
                print("You have to Log In or Register first to continue!")
                continue

            password_dest_name = input(
                "Enter the name of which password you want to save: "
            )
            password_input = input("Enter the password to save: ")

            Password_Saver = Password(password=password_input)
            if password_input == "generate":
                Password_Saver.generate()
                accept_generated_password = input(
                    f"The generated password is {Password_Saver.password}. Do you wnat to accept it. (yes/no): "
                )
                if accept_generated_password.lower() == "no":
                    accepted_password = input("Enter your own password: ")
                    Password_Saver.password = accepted_password

            Password_Saver.caesar_cipher(shift=3)
            strength_status = Password_Saver.status_declaration()

            result_upload_password = Database.upload_password(
                password_dest_name=password_dest_name,
                password=Password_Saver.password,
                strength_status=strength_status,
                user_id=current_user["_id"],
            )

            print(result_upload_password[0]["message"])

        elif command == "view" and command_type == "password":
            if not current_user:
                print("You have to Log In or Register first to continue!")
                continue

            result_get_passwords = Database.get_passwords(userId=current_user["_id"])
            try:
                Password_Table_Formatter = Password(" ")
                decipher_password_array = Password_Table_Formatter.caesar_decipher(
                    passwords=result_get_passwords[1], shift=3
                )
                Password_Table_Formatter.print_password_table_format(
                    decipher_password_array
                )
            except:
                pass

            print(result_get_passwords[0]["message"])

        elif command == "del" and command_type == "password":
            if not current_user:
                print("You have to Log In or Register first to continue!")
                continue

            if additional == None:
                print("Please provide the id of the password to delete!")
                continue

            result_del_password = Database.delete_password(password_id=additional)
            if result_del_password:
                additional = None

        elif command == "edit" and command_type == "password":
            if not current_user:
                print("You have to Log In or Register first to continue!")
                continue
            
            if additional == None:
                print("Please provide the id of the password to edit!")
                continue

            new_password_input = input("Enter the new Password: ")
            confirm_password = input("Confirm the above entered password: ")

            New_Password = Password(new_password_input)
            New_Password.caesar_cipher(shift=3)
            strength_status = New_Password.status_declaration()

            if new_password_input != confirm_password:
                print("Your password does not match!")
                continue

            result_edit_password = Database.edit_password(
                password_id=additional,
                new_password=New_Password.password,
                strength_status=strength_status,
            )
            if result_edit_password:
                additional = None

        elif command == "clear":
            os.system("cls")

        elif command == "exit":
            re_run = False

        else:
            print("Error while executing your command!")


if __name__ == "__main__":
    main()
