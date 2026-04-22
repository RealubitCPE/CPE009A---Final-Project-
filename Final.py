# ================= MODULES =================
import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib

# ================= FILES =================
users_file = "users.json"
products_file = "products.json"
orders_file = "reservations.json"

# ================= Security  =================
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ================= DATA =================
users = {}
products = []
orders = []

current_user = {"username": None, "role": None}

# ================= SAVE =================
def save_users():
    with open(users_file, "w") as f:
        json.dump(users, f, indent=2)

def save_products():
    with open(products_file, "w") as f:
        json.dump(products, f, indent=2)

def save_orders():
    with open(orders_file, "w") as f:
        json.dump(orders, f, indent=2)

# ================= LOAD =================
def load_data():
    global users, products, orders

    if os.path.exists(users_file):
        try:
            with open(users_file) as f:
                users = json.load(f)
        except:
            users = {}
    else:
        users = {}

    if os.path.exists(products_file):
        try:
            with open(products_file) as f:
                products = json.load(f)
        except:
            products = []
    else:
        products = []

    if os.path.exists(orders_file):
        try:
            with open(orders_file) as f:
                orders = json.load(f)
        except:
            orders = []
    else:
        orders = []

    # AUTO ADMIN
    if "admin" not in users:
        users["admin"] = {
            "password": encrypt_password("1234"),
            "role": "Admin"
        }
        save_users()

# ================= AUTHENTICATION =================
def register(username, password):
    if username in users:
        return False

    users[username] = {
        "password": encrypt_password(password),
        "role": "User"
    }

    save_users()
    return True

def login(username, password):
    if username in users:
        if users[username]["password"] == encrypt_password(password):
            return users[username]["role"]
    return None

# ================= PRODUCTS =================
def add_item(animal, name, breed, info, qty, price):
    for p in products:
        if p["name"] == name:
            return False

    products.append({
        "animal": animal,
        "name": name,
        "breed": breed,
        "info": info,
        "qty": qty,
        "price": price
    })

    save_products()
    return True

def reserve_item(username, name, qty):
    for p in products:
        if p["name"] == name and p["qty"] >= qty:
            p["qty"] -= qty

            orders.append({
                "user": username,
                "product": name,
                "qty": qty
            })

            save_products()
            save_orders()
            return True

    return False

def remove_item(name):
    for p in products:
        if p["name"] == name:
            products.remove(p)
            save_products()
            return True
    return False

# ================= GUI Setup =================
root = tk.Tk()
root.title("🐾 PET SHOP SYSTEM")
root.geometry("550x700")
root.configure(bg="#FFF6F9")

login_frame = tk.Frame(root, bg="#FFF6F9")
login_frame.pack()

tk.Label(login_frame, text="PET SHOP SYSTEM",
         font=("Arial", 16, "bold"),
         bg="#FFF6F9", fg="#C94C82").pack(pady=10)

tk.Label(login_frame, text="Username", bg="#FFF6F9").pack()
username_input = tk.Entry(login_frame)
username_input.pack()

tk.Label(login_frame, text="Password", bg="#FFF6F9").pack()
password_input = tk.Entry(login_frame, show="*")
password_input.pack()

main_frame = tk.Frame(root, bg="#FFF6F9")

listbox = tk.Listbox(main_frame, width=70)
listbox.pack(pady=10)

def refresh_list():
    listbox.delete(0, tk.END)
    for p in products:
        listbox.insert(
            tk.END,
            f"{p['animal']} - {p['name']} ({p['breed']}) | ₱{p['price']} | Qty: {p['qty']}"
        )

def register_user():
    if register(username_input.get(), password_input.get()):
        messagebox.showinfo("Success", "Account created")
    else:
        messagebox.showerror("Error", "User exists")

def login_user():
    role = login(username_input.get(), password_input.get())

    if role:
        current_user["username"] = username_input.get()
        current_user["role"] = role

        login_frame.pack_forget()
        main_frame.pack()

        if role == "Admin":
            admin_frame.pack()
        else:
            user_frame.pack()

        refresh_list()
    else:
        messagebox.showerror("Error", "Invalid login")

def add_item_ui():
    try:
        add_item(
            animal_input.get(),
            name_input.get(),
            breed_input.get(),
            info_input.get(),
            int(qty_input.get()),
            float(price_input.get())
        )
        refresh_list()
    except:
        messagebox.showerror("Error", "Invalid input")

def reserve_ui():
    try:
        qty = int(reserve_input.get())
    except:
        messagebox.showerror("Error", "Invalid quantity")
        return

    name = name_input.get()

    if reserve_item(current_user["username"], name, qty):
        refresh_list()
        messagebox.showinfo("Receipt", f"{name} x{qty}")
    else:
        messagebox.showerror("Error", "Not enough stock")

def delete_ui():
    sel = listbox.curselection()
    if not sel:
        messagebox.showerror("Error", "Select product")
        return

    item = listbox.get(sel[0])
    name = item.split(" - ")[1].split(" (")[0]

    if remove_item(name):
        refresh_list()
        messagebox.showinfo("Success", "Deleted")

def logout():
    current_user["username"] = None
    current_user["role"] = None

    main_frame.pack_forget()
    admin_frame.pack_forget()
    user_frame.pack_forget()

    login_frame.pack()

tk.Button(login_frame, text="Login", command=login_user).pack()
tk.Button(login_frame, text="Sign Up", command=register_user).pack()

admin_frame = tk.Frame(main_frame, bg="#FFF6F9")

animal_input = tk.Entry(admin_frame)
name_input = tk.Entry(admin_frame)
breed_input = tk.Entry(admin_frame)
info_input = tk.Entry(admin_frame)
qty_input = tk.Entry(admin_frame)
price_input = tk.Entry(admin_frame)

for label, entry in [
    ("Animal", animal_input),
    ("Name", name_input),
    ("Breed", breed_input),
    ("Info", info_input),
    ("Qty", qty_input),
    ("Price", price_input)
]:
    tk.Label(admin_frame, text=label, bg="#FFF6F9").pack()
    entry.pack()

tk.Button(admin_frame, text="Add", command=add_item_ui).pack()
tk.Button(admin_frame, text="Delete", command=delete_ui).pack()
tk.Button(admin_frame, text="Logout", command=logout).pack()

user_frame = tk.Frame(main_frame, bg="#FFF6F9")

reserve_input = tk.Entry(user_frame)
reserve_input.pack()

tk.Button(user_frame, text="Reserve", command=reserve_ui).pack()
tk.Button(user_frame, text="Logout", command=logout).pack()

# ================= MAIN =================
load_data()
root.mainloop()
