import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# =========================
# WINDOW
# =========================
root = tk.Tk()
root.title("Evonne Angel's Burger POS")
root.geometry("1100x650")
root.configure(bg="#F3F4F6")


# =========================
# COLORS
# =========================
BG = "#F3F4F6"
CARD = "#FFFFFF"
PRIMARY = "#F59E0B"
GREEN = "#10B981"
RED = "#EF4444"
TEXT = "#111111"
LIGHT = "#6B7280"


# =========================
# PRODUCTS
# =========================
products = [
    {"name": "Regular Burger", "price": 65, "category": "Burger"},
    {"name": "Cheesy Burger", "price": 80, "category": "Burger"},

    {"name": "French Fries", "price": 60, "category": "Snacks"},
    {"name": "Onion Rings", "price": 70, "category": "Snacks"},

    {"name": "MilkTea", "price": 90, "category": "Drinks"},
    {"name": "Softdrinks", "price": 50, "category": "Drinks"},

    {"name": "Ketchup", "price": 10, "category": "Sauces"},
    {"name": "Mayonnaise", "price": 15, "category": "Sauces"},
]

cart = []


# =========================
# CART FUNCTIONS
# =========================
def update_cart():
    cart_table.delete(*cart_table.get_children())

    total = 0

    for item in cart:
        subtotal = item["qty"] * item["price"]

        cart_table.insert("", tk.END, values=(
            item["name"],
            item.get("flavor", "-"),
            item.get("size", "-"),
            item["qty"],
            f"₱{item['price']}"
        ))

        total += subtotal

    total_label.config(text=f"TOTAL: ₱{total}")
    return total


def add_to_cart(product):

    for item in cart:
        if item["name"] == product["name"]:
            item["qty"] += 1
            update_cart()
            return

    cart.append({
        "name": product["name"],
        "price": product["price"],
        "qty": 1,
        "flavor": product.get("flavor", "-"),
        "size": product.get("size", "-")
    })

    update_cart()


def remove_item():
    selected = cart_table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select item")
        return

    name = cart_table.item(selected)["values"][0]

    for item in cart:
        if item["name"] == name:
            cart.remove(item)
            break

    update_cart()


def clear_cart():
    cart.clear()
    update_cart()


# =========================
# PAYMENT SYSTEM
# =========================
cash_var = tk.StringVar()


def checkout():

    if not cart:
        messagebox.showwarning("Empty", "Cart is empty")
        return

    total = update_cart()

    try:
        cash = float(cash_var.get())
    except:
        messagebox.showerror("Error", "Enter valid cash amount")
        return

    if cash < total:
        messagebox.showerror("Insufficient", "Not enough cash")
        return

    change = cash - total

    receipt = f"""
======= EVONNE ANGEL'S BURGER =======

Date: {datetime.now()}

--------------------------------------
"""

    for item in cart:
        subtotal = item["qty"] * item["price"]
        receipt += f"{item['name']} x{item['qty']} = ₱{subtotal}\n"

    receipt += f"""
--------------------------------------
TOTAL: ₱{total}
CASH: ₱{cash}
CHANGE: ₱{change}

THANK YOU!
"""

    messagebox.showinfo("Receipt", receipt)

    cart.clear()
    cash_var.set("")
    update_cart()


# =========================
# OPTIONS WINDOW
# =========================
def open_options(product):

    win = tk.Toplevel(root)
    win.title(product["name"])
    win.geometry("300x350")

    selected_flavor = tk.StringVar()
    selected_size = tk.StringVar(value="Small")

    tk.Label(win, text=product["name"], font=("Segoe UI", 14, "bold")).pack(pady=10)

    options = []

    if product["name"] == "MilkTea":
        options = ["Cookies & Cream", "Mango", "Strawberry"]

    elif product["name"] == "Softdrinks":
        options = ["Coke", "Pepsi", "Royal"]

    elif product["name"] == "French Fries":
        options = ["Barbeque", "Sour Cream", "Cheese", "Salt"]

    for opt in options:
        tk.Radiobutton(win, text=opt, variable=selected_flavor, value=opt).pack(anchor="w")

    tk.Label(win, text="Size").pack(pady=10)

    for s in ["Small", "Medium", "Large"]:
        tk.Radiobutton(win, text=s, variable=selected_size, value=s).pack(anchor="w")

    def confirm():

        name = product["name"]

        if selected_flavor.get():
            name += f" | {selected_flavor.get()}"

        name += f" | {selected_size.get()}"

        add_to_cart({
            "name": name,
            "price": product["price"],
            "flavor": selected_flavor.get(),
            "size": selected_size.get()
        })

        win.destroy()

    tk.Button(win, text="Add", bg=GREEN, fg="white", command=confirm).pack(pady=15)


# =========================
# UI
# =========================
tk.Label(root, text="Evonne Angel's Burger POS",
         bg=BG, fg=TEXT, font=("Segoe UI", 22, "bold")).pack(pady=10)


main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True)


center_frame = tk.Frame(main_frame, bg=BG)
center_frame.pack(side="left", fill="both", expand=True, padx=10)


order_frame = tk.Frame(main_frame, bg=CARD, width=420)
order_frame.pack(side="right", fill="y")


# =========================
# CART UI
# =========================
tk.Label(order_frame, text="Customer Orders",
         bg=CARD, fg=TEXT, font=("Segoe UI", 18, "bold")).pack(pady=10)


columns = ("Product", "Flavor", "Size", "Qty", "Price")

cart_table = ttk.Treeview(order_frame, columns=columns, show="headings", height=15)

for col in columns:
    cart_table.heading(col, text=col)
    cart_table.column(col, width=80)

cart_table.pack(padx=10)


total_label = tk.Label(order_frame, text="TOTAL: ₱0",
                       bg=CARD, fg=PRIMARY, font=("Segoe UI", 20, "bold"))
total_label.pack(pady=10)


# CASH INPUT
tk.Label(order_frame, text="Cash:", bg=CARD).pack()
tk.Entry(order_frame, textvariable=cash_var).pack()


btn_frame = tk.Frame(order_frame, bg=CARD)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Remove", bg=RED, fg="white", command=remove_item).grid(row=0, column=0)
tk.Button(btn_frame, text="Clear", bg=LIGHT, fg="white", command=clear_cart).grid(row=0, column=1)

tk.Button(order_frame, text="Checkout", bg=GREEN, fg="white",
          font=("Segoe UI", 14, "bold"), command=checkout).pack(pady=10)


# =========================
# CATEGORIES
# =========================
category_frame = tk.Frame(center_frame, bg=BG)
category_frame.pack(pady=10)

categories = ["Home", "Burger", "Snacks", "Drinks", "Sauces"]


def show_home():
    for w in center_frame.winfo_children():
        if w != category_frame:
            w.destroy()

    home = tk.Frame(center_frame, bg=BG)
    home.pack(expand=True, pady=120)

    tk.Label(home, text="START ORDER",
             font=("Segoe UI", 34, "bold"),
             bg=BG, fg=PRIMARY).pack()

    tk.Label(home, text="Thank you for ordering",
             font=("Segoe UI", 14),
             bg=BG, fg=LIGHT).pack()


def show_category(cat):
    if cat == "Home":
        show_home()
    else:
        display_products(cat)


for i, cat in enumerate(categories):
    tk.Button(category_frame, text=cat,
              bg=PRIMARY, fg="white",
              font=("Segoe UI", 14, "bold"),
              width=12, height=2,
              command=lambda c=cat: show_category(c)).grid(row=0, column=i, padx=5)


# =========================
# PRODUCTS
# =========================
def display_products(category):

    for w in center_frame.winfo_children():
        if w != category_frame:
            w.destroy()

    grid = tk.Frame(center_frame, bg=BG)
    grid.pack()

    row = col = 0

    for product in products:

        if product["category"] != category:
            continue

        card = tk.Frame(grid, bg=CARD, width=200, height=160)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)
        card.pack_propagate(False)

        tk.Label(card, text="🍔", bg=CARD, font=("Segoe UI", 25)).pack()
        tk.Label(card, text=product["name"], bg=CARD, font=("Segoe UI", 11, "bold")).pack()
        tk.Label(card, text=f"₱{product['price']}", bg=CARD).pack()

        tk.Button(
            card,
            text="Add",
            bg=PRIMARY,
            fg="white",
            command=lambda p=product:
                open_options(p) if p["name"] in ["MilkTea", "Softdrinks", "French Fries"]
                else add_to_cart(p)
        ).pack(pady=5)

        col += 1
        if col == 3:
            col = 0
            row += 1


# START
show_home()
root.mainloop()