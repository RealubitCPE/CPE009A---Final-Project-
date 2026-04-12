#Uses a json file to save progress
import json
#Uses hash passwords for better security
import hashlib
#uses roles for admin and user accounts
from abc import ABC, abstractmethod 

#Creates SHA256 based hashes on different characters and uses hexdigest to make it readable
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#This is the main format for account security
#username can be accessed by user and admins only 
#passwords cannot be directly accessed since it is automatically hashed
class account(ABC):
    def __init__(self, username, password):
        self._username = username
        self.__password = hash_password(password)
#Used for password security, similar password, contains similar hashes
    def check_password(self, password):
        return self.__password == hash_password(password)

    def get_username(self):
        return self._username
    
    def get_password(self):
        return self.__password
#creates different roles for admin and user
    @abstractmethod
    def role(self):
        pass

#These are the main roles set by the developer 
class Admin(account):
    def role(self):
        return "Admin"

class User(account):
    def role(self):
        return "User"

#stores the accounts in a list
class System:
    def __init__(self):
        self.__accounts = []

#signing up process
#checks if a similar username already exists     
    def signup(self, username, password, role):
        for acc in self.__accounts:
            if acc.get_username() == username:
                return "Username already exists."
#checks if the account created is an admin or a user account   
        if role.lower() == "admin":
            account = Admin(username, password)
        else:
            account = User(username, password)
#verifies if the account is created       
        self.__accounts.append(account)
        return f"{role} account created successfully."
    
#Loops through the entire saved account list to find match of your account
    def login(self, username, password):
        for acc in self.__accounts:
            if acc.get_username() == username and acc.check_password(password):
                return acc
        return None
    
    def save_accounts(self):
        data = []
#Accounts are stored in a list using a dictionary where each specific username and passwords should match each
        for acc in self.__accounts:
            data.append({
                "username": acc.get_username(),
                "password": acc.get_password(),
                "role": acc.role()
            })
#Opens a Json file to store all account informations       
        with open("accounts.json", "w") as f:
            json.dump(data,f)
#stores the data into a json file
    def load_accounts(self):
        try:
            with open("accounts.json", "r") as f:
                data =json.load(f)
#turns the data into objects
            for item in data:
                if item ["role"] == "Admin":
                    acc = Admin(item["username"],"temp")
                else:
                    acc = User(item["username"],"temp")
#returns hashed password into original text
                acc._Account__password = item["password"]
#Stores the accounts in the system
                self.__accounts.append(acc)
        
        except FileNotFoundError, json.JSONDecodeError:
            pass
#Account deletion function    
    def delete_account(self,username):
        try:
            with open("accounts.json", "r") as f:
                data = json.load(f)
        
            new_data = []
            for acc in data:
                if acc["username"] != username:
                    new_data.append(acc)

            with open("accounts.json", "w") as f:
               json.dump(data,f)

            return "Account Deleted."
        
        except FileNotFoundError:
            return "No account found."
#This is the main function where all methods above takes action          
def main():
#System function above will run and the account signup and login takes place.
    system = System()
    system.load_accounts()
#When it loads, a selection will appear     
    while True:
        print("\n=== MENU ===")
        print("1. sign up")
        print("2. login")
        print("3. Exit")

        choice = input("Choose: ")
#Once the user chooses, a choice-based response will occure, different choices will have different outcomes
#Note: This can work with Switch case but since I know how to use if-elif statements better, I used it instead.
        if choice == "1":
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            role = input("Role (admin/user): ")

            print(system.signup(username, password, role))
            system.save_accounts()

        elif choice == "2":
            username = input("Enter Username: ")
            password = input("Enter Password: ")

            acc = system.login(username, password)

            if acc:
                print(f"Welcome {role} {acc.get_username()}!")

            else:
                print("Invalid Login.")

        elif choice == "3":
            system.save_accounts()
            print("Thank you for shopping.")
            break

        else:
            print("Invalid Choice.")
#Since we are running the file in VSCode, a special variable called "__name__" is changed into "__main__" so we have to take that into account
#If that condition is not taken into account, a runtime error will occur.
if __name__ == "__main__":
#This runs the whole system
    main()
    class PetItem:
    def __init__(self, name, breed, info, qty, srp, img):
        self.name = name
        self.breed = breed
        self.info = info
        self.qty = int(qty)
        self.srp = float(srp)
        self.img = img

class ThePetShop:
    def __init__(self):
        self.users = []
        self.catalog = []
        self.load_all()

    def load_all(self):

        if os.path.exists("the_pet_shop_users.json"):
            with open("the_pet_shop_users.json", "r", encoding="utf-8") as f:
                for u in json.load(f):
                    maximum = Manager(u['id'], u['level']) if u['lvl'] =="Admin" else Guest(u['id'], u['level'])
                    self.users.append(maximum)

        if os.path.exists("the_pet_shop_inv.json"):
            with open("the_pet_shop_inv.json", "r", encoding="utf-8") as f:
                for idx in json.load(f):
                    self.catalog.append(PetItem(idx['length'], idx['b'], idx['f'], idx['q'], idx['s'], idx['p']))

    def sync_files(self):

        u_data = [{"id": value.handle, "level": value.key, "lvl": value.get_access()} for value in self.users]
        with open("the_pet_shop_users.json", "w", encoding="utf-8") as f:
            json.dump(u_data, f, indent=2)

        inv_data = [{"length": p.name, "b": p.breed, "f": p.info, "q": p.qty, "s": p.srp, "p": p.img} for p in self.catalog]
        with open("the_pet_shop_inv.json", "w", encoding="utf-8") as f:
            json.dump(inv_data, f, indent=2)
