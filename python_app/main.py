import database as db
from terminaltables3 import AsciiTable as table


def create_user():
    while True:
        uname = input("What would you like your user name to be\n")
        if db.validate_user(uname):
            print("That username already exists\n")
        else:
            break
    while True:
        mgrade = input("What is the max grade that you have sent\n")
        if mgrade not in ['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16','V17','5.2','5.3','5.4','5.5','5.6','5.7','5.8','5.9','5.10a','5.10b','5.10c','5.10d','5.11a','5.11b','5.11c','5.11d','5.12a','5.12b','5.12c','5.12d','5.13a','5.13b','5.13c','5.13d','5.14a','5.14b','5.14c','5.14d','5.15a','5.15b','5.15c','5.15d','3','4-','4','4+','5-','5','5+','6a','6a+','6b','6b+','6c','6c+','7a','7a+','7b','7b+','7c','7c+','8a','8a+','8b','8b+','8c','8c+','9a','9a+','9b','9b+','9c']:
            print("invalid grade\n")
        else:
            break
    description = input("Input user description\n")
    try:
        db.create_user()
    except:
        create_user()
    return None


def login():
    name = input("What is your user name?\n")
    uid = db.validate_user(name)
    if uid and uid != LookupError:
        return db.db_mngr(uid)
    else:
        print("That is not a valid user")
        uinp = ""
        while uinp != "1" or uinp != "2" or uinp != "3":
            input("Would you like to\n[1] Try Again\n[2] Create a user\n[3] Quit\n")
        if uinp == "1":
            return login()
        elif uinp == "2":
            create_user()
            return login()
        else:
            exit()


def main():
    dbase = login()


if __name__=="__main__":
    main()