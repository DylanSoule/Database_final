import database as db
from terminaltables3 import AsciiTable as tables
import subprocess

def create_user():
    """Create a new user by collecting username, max grade, and description."""
    while True:
        subprocess.run(['clear'], shell=False)
        uname = input("What would you like your user name to be\n")
        # Ensure username is unique
        if db.validate_user(uname):
            print("That username already exists\n")
        else:
            break
    while True:
        subprocess.run(['clear'], shell=False)
        mgrade = input("What is the max grade that you have sent\n")
        # Validate against allowed grades
        if mgrade not in ['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16','V17','5.2','5.3','5.4','5.5','5.6','5.7','5.8','5.9','5.10a','5.10b','5.10c','5.10d','5.11a','5.11b','5.11c','5.11d','5.12a','5.12b','5.12c','5.12d','5.13a','5.13b','5.13c','5.13d','5.14a','5.14b','5.14c','5.14d','5.15a','5.15b','5.15c','5.15d','3','4-','4','4+','5-','5','5+','6a','6a+','6b','6b+','6c','6c+','7a','7a+','7b','7b+','7c','7c+','8a','8a+','8b','8b+','8c','8c+','9a','9a+','9b','9b+','9c']:
            print("invalid grade\n")
        else:
            break
    # Optional description stored as NULL if empty
    description = input("Input user description\n")
    try:
        db.create_user(uname,mgrade,description if description else None)
        print("\nUser creation successful\n\n\n")
    except Exception as e:
        print(e)
        # Retry user creation on failure
        create_user()
    return None

def login():
    """Prompt for a username and return a db manager for that user."""
    subprocess.run(['clear'], shell=False)
    print("Input Login Credentials\n")
    name = input("What is your user name?\n")
    uid = db.validate_user(name)
    if uid and uid != LookupError:
        # Initialize DB manager with validated user id
        return db.db_mngr(uid)
    else:
        print("That is not a valid user")
        uinp = ""
        # Loop until a valid option is chosen
        while uinp != "1" and uinp != "2" and uinp != "3":
            subprocess.run(['clear'], shell=False)
            uinp = input("Would you like to\n[1] Try Again\n[2] Create a user\n[3] Quit\n")
            if uinp == "1":
                return login()
            elif uinp == "2":
                create_user()
                return login()
            elif uinp == "3":
                exit()

def view_climb(dbase,climb_name):
    """Show a climb and allow user actions (comments, wishlist, ascents)."""
    while True:
        subprocess.run(['clear'], shell=False)
        # Fetch climb details
        info=dbase.climb_info(0,climb_name)
        print(f"{info[0]}: {info[1]} {info[2]}")
        print(f"Description: {info[3]}\n\n")
        action = input("Select One of the options below:\n[1] View Comments\n[2] Add to wishlist\n[3] Mark Ascent\n[4] View ascents\n[5] Add comment\n[6] Go back\n")

        if action =="1":
            subprocess.run(['clear'], shell=False)
            # Display comments on the climb
            comments = dbase.climb_info(1,climb_name)
            for comment in comments:
                print(f"{comment[0]}\n{comment[1]}\n")
            input("Press enter to go back")
        elif action =="2":
            # Add climb to wishlist
            dbase.climb_info(2,climb_name)
            print("\nAdded to wishlist\n")
        elif action =="3":
            subprocess.run(['clear'], shell=False)
            # Collect a numeric rating before storing ascent
            while True:
                rating=input("What is your rating of the climb?(0-5)\n")
                try:
                    rating = float(rating)
                    break
                except:
                    continue
            dbase.climb_info(3,climb_name,uinput=rating)
            print("\nMarked Ascent\n")
        elif action == "4":
            subprocess.run(['clear'], shell=False)
            # List all ascents for this climb
            ascents = dbase.climb_info(4,climb_name)
            for ascent in ascents:
                print(f"{ascent[0]} | user rating: {ascent[1]}")
            input("\nPress enter to go back")
        elif action == "5":
            subprocess.run(['clear'], shell=False)
            # Add a comment to the climb
            comment = input("\nWhat would you like to comment\n")
            dbase.climb_info(5,climb_name,uinput=comment)
            print("\nAdded Comment\n")
        elif action == "6":
            break

def create_location(dbase,parent_name):
    """Collect inputs and create a new sub-location under parent_name."""
    while True:
        subprocess.run(['clear'], shell=False)
        print("Answer question below:\n")
        name = input("Input the name of the location\n")
        if not name:
            print("Make Sure you enter information correctly\n")
            continue
        # Optional description
        description = input("Would you like to add a description?(y/n) ")
        if description.lower() != "y" and description.lower() != "n":
            print("Make Sure you enter information correctly\n")
            continue
        elif description.lower() == "y":
            description = input("Input description\n")
            if not description:
                print("Make Sure you enter information correctly\n")
                continue
        else:
            description=None
        # Collect multiple climb types as a numeric string
        climb_types=input("Input each number for the type of climbing in the location\n   ex: 145 for bouldering,ice, and alpine climbing\n[1] bouldering\n[2] sport\n[3] top rope\n[4] ice\n[5] alpine\n[6] trad\n")
        try: 
            int(climb_types)
        except:
            print("Make Sure you enter information correctly\n")
            continue
        error = 0
        lookup = ['bouldering', 'sport', 'top rope', 'ice', 'alpine', 'trad']
        climb_list =""
        # Build the SET value from numeric selections
        for i in range(len(climb_types)):
            if int(climb_types[i]) < 1 or int(climb_types[i]) > 6:
                print("Make Sure you enter information correctly\n")
                error = 1
                break
            climb_list += f",{lookup[int(climb_types[i])-1]}" if i != 0 else lookup[int(climb_types[i])-1]
        if error == 1:
            continue

        # Persist new location
        dbase.create_location(name,description,climb_list,parent_name)
        return None
    
def create_climb(dbase,parent_name):
    """Collect inputs and create a new climb under parent_name."""
    while True:
        subprocess.run(['clear'], shell=False)
        print("Answer question below:\n")
        name = input("Input the name of the climb\n")
        if not name:
            print("Make Sure you enter information correctly\n")
            continue

        # Validate grade
        grade = input("Input the grade of the climb\n")
        if grade not in ['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16','V17','5.2','5.3','5.4','5.5','5.6','5.7','5.8','5.9','5.10a','5.10b','5.10c','5.10d','5.11a','5.11b','5.11c','5.11d','5.12a','5.12b','5.12c','5.12d','5.13a','5.13b','5.13c','5.13d','5.14a','5.14b','5.14c','5.14d','5.15a','5.15b','5.15c','5.15d','3','4-','4','4+','5-','5','5+','6a','6a+','6b','6b+','6c','6c+','7a','7a+','7b','7b+','7c','7c+','8a','8a+','8b','8b+','8c','8c+','9a','9a+','9b','9b+','9c']:
            print("Make Sure you enter information correctly\n")
            continue

        # Optional description
        description = input("Would you like to add a description?(y/n) ")
        if description.lower() != "y" and description.lower() != "n":
            print("Make Sure you enter information correctly\n")
            continue
        elif description.lower() == "y":
            description = input("Input description\n")
            if not description:
                print("Make Sure you enter information correctly\n")
                continue
        else:
            description=None
        
        # Optional first ascent
        fa = input("Would you like to add a first ascent?(y/n) ")
        if fa.lower() != "y" and fa.lower() != "n":
            print("Make Sure you enter information correctly\n")
            continue
        elif fa.lower() == "y":
            fa = input("Input first_ascent\n")
            if not fa:
                print("Make Sure you enter information correctly\n")
                continue
        else:
            fa=None
        
        #rating
        rating = input("Input rating(0.0-5.0)\n")
        try:
            rating = float(rating)
        except:
            continue
        if not rating or (rating < 0.0 or rating > 5.0):
            print("Make Sure you enter information correctly\n")
            continue
            
        # Map numeric selection to climb type
        climb_type=input("What type of climb is the climb\n[1] bouldering\n[2] sport\n[3] top rope\n[4] ice\n[5] alpine\n[6] trad\n")
        try: 
            int(climb_type)
        except:
            print("Make Sure you enter information correctly\n")
            continue
        if climb_type not in ['1','2','3','4','5','6']:
            continue
        lookup = ['bouldering', 'sport', 'top rope', 'ice', 'alpine', 'trad']
        climb_type = lookup[int(climb_type)-1]
        
        # Persist new climb
        dbase.create_climb(name,description,climb_type,parent_name,grade,fa,rating)
        return None

def browsing(dbase):
    """Interactive browser for locations and climbs."""
    parent_name = "The Whole World"
    search = ""
    while True:
        subprocess.run(['clear'], shell=False)
        print("Select One of the options below\n")
        output = dbase.list_locations(parent_name, search=search)
        parent_name = output[0][0]
        print(f"{parent_name}:")
        print(f"{output[0][1]}\n")

        location_list = []
        climb_list = []
        selection_map = {}

        if output[1]:
            print("Sub-Locations:")
            for i in range(len(output[1])):
                location_list.append((i, output[1][i],))
                selection_map[i] = ("location", output[1][i][0])
                print(f"[{location_list[i][0]}] {location_list[i][1][0]}: {', '.join(map(str,location_list[i][1][1]))}")
        if output[2]:
            print("\nClimbs in location:")
            for i in range(len(output[1]), len(output[1]) + len(output[2])):
                climb_list.append((i, output[2][i-len(output[1])],))
                selection_map[i] = ("climb", output[2][i-len(output[1])][0])
                print(f"[{climb_list[i-len(output[1])][0]}] {climb_list[i-len(output[1])][1][0]}: {climb_list[i-len(output[1])][1][1]}, {climb_list[i-len(output[1])][1][2]}")

        print("\n[s] Search for a location or climb")
        print("[b] Go back")
        if search == "":
            print("[nl] Add sublocation")
            print("[nc] Add climb to location")
        print("[e] Exit Browsing\n")

        action = input("What would you like to view/do\n")

        if action=="s":
            search = input("What would you like to search for\n")
            continue
        elif action=="b":
            search = ""
            if parent_name != "Search Results":
                parent_name = dbase.get_parent_name(parent_name if parent_name != "The whole world" else "")
            else:
                parent_name = "The Whole World"
            continue
        elif action=="nl" and search == "":
            create_location(dbase, parent_name)
        elif action=="nc" and search == "":
            create_climb(dbase, parent_name)
        elif action=="e":
            break
        elif action.isdigit():
            selection = selection_map.get(int(action))
            if selection:
                if selection[0] == "location":
                    parent_name = selection[1]
                else:
                    view_climb(dbase, selection[1])


def ascents(dbase):
    """View, search, or delete ascents for the current user."""
    while True:
        subprocess.run(['clear'], shell=False)
        action = input("What would you like to do now?\n     You can add climbs to your ascents on their page(Use browse climbs)\n[1] View Ascents\n[2] Search For Climb/Area\n[3] Delete Climb\n[4] Quit Ascents\n")
        try:
            if action == "1":
                subprocess.run(['clear'], shell=False)
                # Show all ascents
                table_data = dbase.pull_ascents()
                table_data.insert(0,("Climb Name","Grade","Description","Self Rating"))
                table = tables(table_data)
                print("Your Ascents:")
                print(table.table)
                print("\n")
                input("Press enter to continue")
            elif action == "2":
                subprocess.run(['clear'], shell=False)
                # Filter ascents by location or climb name
                name = input("What is the name of the climb/area\n")
                table_data = dbase.search("ascents",name)
                table_data.insert(0,("Area Name","Climb Name","Grade","Description","Your Rating"))
                table = tables(table_data)
                print("Results:")
                print(table.table)
                print("\n")
                input("Press enter to continue")
            elif action == "3":
                subprocess.run(['clear'], shell=False)
                # Delete one or more ascents
                name = input("What is the name of the climb you want to delete\n")
                table_data = dbase.search('ascents',name)
                table_data.insert(0,("Area Name","Climb Name","Grade","Description","Your Rating"))
                table = tables(table_data)
                print(table.table)
                if input("Are you sure you want to delete this climb(s) from your ascents(y/n) ").lower()=="y":
                    for i in range(len(table_data)-1):
                        dbase.delete_asc_data(table_data[i+1][0],table_data[i+1][1])
            elif action == "4":
                break
        except Exception as e:
            print("Unknown Error",e)
            break


def wishlist(dbase):
    """View, search, or delete wishlist entries for the current user."""
    while True:
        subprocess.run(['clear'], shell=False)
        action = input("What would you like to do now?\n     You can add climbs to your wishlist on their page(Use browse climbs)\n[1] View Wishlist\n[2] Search For Climb/Area\n[3] Delete Climb\n[4] Quit Wishlist\n")
        try:
            if action == "1":
                subprocess.run(['clear'], shell=False)
                # Show all wishlist entries
                table_data = dbase.pull_wishlist()
                table_data.insert(0,("Climb Name","Grade","Description"))
                table = tables(table_data)
                print("Your Wishlist:")
                print(table.table)
                print("\n")
                input("Press enter to continue")
            elif action == "2":
                subprocess.run(['clear'], shell=False)
                # Filter wishlist by location or climb name
                name = input("What is the name of the climb/area\n")
                table_data = dbase.search("wishlists",name)
                table_data.insert(0,("Area Name","Climb Name","Grade","Description"))
                table = tables(table_data)
                print("Results:")
                print(table.table)
                print("\n")
                input("Press enter to continue")
            elif action == "3":
                subprocess.run(['clear'], shell=False)
                # Delete one or more wishlist entries
                name = input("What is the name of the climb you want to delete\n")
                table_data = dbase.search("wishlists",name)
                table_data.insert(0,("Area Name","Climb Name","Grade","Description"))
                table = tables(table_data)
                print(table.table)
                if input("Are you sure you want to delete this climb(s) from your wishlist(y/n) ").lower()=="y":
                    for i in range(len(table_data)-1):
                        dbase.delete_wl_data(table_data[i+1][0],table_data[i+1][1])
            elif action == "4":
                break
        except:
            print("Unknown Error")
            break

def main():
    """Main application loop."""
    subprocess.run(['clear'], shell=False)
    # Authenticate user and start session
    dbase = login()
    print("You're logged in\n\n")
    while True:
        subprocess.run(['clear'], shell=False)
        # Top-level navigation
        action = input("What would you like to do now?\n[1] Browse Climbs\n[2] View or Edit Ascents\n[3] View or Edit Wishlist\n[4] Quit App\n")
        if action == "1":
            browsing(dbase)
        elif action == "2":
            ascents(dbase)
        elif action == "3":
            wishlist(dbase)
        elif action == "4":
            break


if __name__=="__main__":
    main()