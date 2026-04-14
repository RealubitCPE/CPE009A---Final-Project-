# ================= PET SHOP =================
import json
import os

class PetItem:
    def __init__(self, name, breed, info, qty, srp, img):
        self.name = name
        self.breed = breed
        self.info = info
        self.qty = int(qty)
        self.srp = float(srp)
        self.img = img


class Manager:
    def __init__(self, handle, key):
        self.handle = handle
        self.key = key

    def check_auth(self, password):
        return self.key == password

    def get_access(self):
        return "Admin"


class Guest:
    def __init__(self, handle, key):
        self.handle = handle
        self.key = key

    def check_auth(self, password):
        return self.key == password

    def get_access(self):
        return "User"


class ThePetShop:
    def __init__(self):
        self.users = []
        self.catalog = []
        self.load_all()

    def load_all(self):

        if os.path.exists("the_pet_shop_users.json"):
            with open("the_pet_shop_users.json", "r", encoding="utf-8") as f:
                for u in json.load(f):
                    maximum = Manager(u['id'], u['level']) if u['lvl'] == "Admin" else Guest(u['id'], u['level'])
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

    def add_product(self, name, breed, info, qty, srp, img):
        new_item = PetItem(name, breed, info, qty, srp, img)
        self.catalog.append(new_item)
        self.sync_files() # Save changes immediately
        print(f"Product {name} added successfully.")

    def update_product_stock(self, name, new_qty):
        for item in self.catalog:
            if item.name.lower() == name.lower():
                item.qty = int(new_qty)
                self.sync_files()
                print(f"Stock for {name} updated to {new_qty}.")
                return True
        print("Product not found.")
        return False

    def show_catalog(self):
        
        if not self.catalog:
            print('No products available.')
            return

        for item in self.catalog
            print("Name:{item.name}, Breed:{item.breed}, Info:{item.info}, qty:{item.qty}, srp: {item.srp}, image: {item.img}')
       
