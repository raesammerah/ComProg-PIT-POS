import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os


# =========================
# FILE PATH (SAME FOLDER)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORDERS_FILE = os.path.join(BASE_DIR, "orders.txt")
OVERALL_FILE = os.path.join(BASE_DIR, "overall_orders.txt")


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
PRIMARY = "#4F46E5"
GREEN = "#10B981"
RED = "#EF4444"
TEXT = "#1F2937"
LIGHT = "#6B7280"
GOLD = "#FBBF24"


# =========================
# DATA
# =========================
products = [
    
    {"name": "Dieter's SP Burger", "price": 120, "category": "Special"},
    {"name": "Rea's SP Burger ", "price": 120, "category": "Special"},
    {"name": "Evonne's SP Burger", "price": 120, "category": "Special"},
    {"name": "Ken's SP Burger", "price": 120, "category": "Special"},
    {"name": "BobJames SP Burger", "price": 120, "category": "Special"},
    {"name": "Regular Burger", "price": 50, "category": "Burger"},
    {"name": "Cheesy Burger", "price": 80, "category": "Burger"},
    {"name": "Chicken Burger", "price": 85, "category": "Burger"},
    {"name": "Double Patty Burger", "price": 115, "category": "Burger"},
    {"name": "Bacon Burger", "price": 110, "category": "Burger"},
    {"name": "Ham Burger", "price": 95, "category": "Burger"},
    {"name": "Veggie Burger", "price": 75, "category": "Burger"},
    {"name": "French Fries", "price": 60, "category": "Snacks"},
    {"name": "Onion Rings", "price": 70, "category": "Snacks"},
    {"name": "Chicken Nuggets", "price": 80, "category": "Snacks"},
    {"name": "Cheese Sticks", "price": 85, "category": "Snacks"},
    {"name": "Hotdog Bites", "price": 65, "category": "Snacks"},
    {"name": "Hash Brown", "price": 55, "category": "Snacks"},
    {"name": "MilkTea", "price": 90, "category": "Drinks"},
    {"name": "Softdrinks", "price": 50, "category": "Drinks"},
    {"name": "Iced Coffee", "price": 95, "category": "Drinks"},
    {"name": "Orange Juice", "price": 60, "category": "Drinks"},
    {"name": "Lemonade", "price": 55, "category": "Drinks"},
    {"name": "Water Bottle", "price": 20, "category": "Drinks"},
    {"name": "Hot Coffee", "price": 40, "category": "Drinks"},
    {"name": "Ketchup", "price": 10, "category": "Sauces"},
    {"name": "Mayonnaise", "price": 15, "category": "Sauces"},
    {"name": "Cheese Dip", "price": 20, "category": "Sauces"},
    {"name": "Barbecue Sauce", "price": 15, "category": "Sauces"},
    {"name": "Garlic Mayo", "price": 18, "category": "Sauces"},
    {"name": "Spicy Sauce", "price": 12, "category": "Sauces"},
]

cart = []
orders_history = []
sales_by_date = {}
cash_var = tk.StringVar()


# =========================
# BUTTON HIGHLIGHT
# =========================
selected_button = None

def highlight_button(btn):
    global selected_button
    if selected_button:
        selected_button.config(bg=PRIMARY)
    btn.config(bg=GOLD)
    selected_button = btn


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
            f"₱{subtotal}"
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
# CHECKOUT + SAVE
# =========================
def checkout():
    if not cart:
        messagebox.showwarning("Empty", "Cart is empty")
        return

    total = update_cart()

    try:
        cash = float(cash_var.get())
    except:
        messagebox.showerror("Error", "Enter valid cash")
        return

    if cash < total:
        messagebox.showerror("Insufficient", "Not enough cash")
        return

    change = cash - total
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_key = datetime.now().strftime("%Y-%m-%d")

    orders_history.append({
        "time": time_now,
        "items": cart.copy(),
        "total": total,
        "cash": cash,
        "change": change
    })

    sales_by_date.setdefault(date_key, 0)
    sales_by_date[date_key] += total

    with open(ORDERS_FILE, "a") as f:
        f.write(f"\nTIME: {time_now}\n")
        for item in cart:
            f.write(f"{item['name']} x{item['qty']} = ₱{item['price']*item['qty']}\n")
        f.write(f"TOTAL: ₱{total}\n")
        f.write("-"*40 + "\n")

    with open(OVERALL_FILE, "a") as f:
        f.write(f"\nTIME: {time_now}\n")
        for item in cart:
            f.write(f"{item['name']} x{item['qty']} = ₱{item['price']*item['qty']}\n")
        f.write(f"TOTAL: ₱{total}\n")
        f.write(f"CASH: ₱{cash}\n")
        f.write(f"CHANGE: ₱{change}\n")
        f.write("="*50 + "\n")

    messagebox.showinfo("Receipt", f"TOTAL: ₱{total}\nCHANGE: ₱{change}") 
    

    cart.clear()
    cash_var.set("")
    update_cart()

# =========================
# RECEIPT
# =========================
def checkout():

    if not cart:
        messagebox.showwarning("Empty", "Cart is empty")
        return

    total = 0

    for item in cart:
        total += item["qty"] * item["price"]

    try:
        cash = float(cash_var.get())
    except:
        messagebox.showerror("Error", "Enter valid cash")
        return

    if cash < total:
        messagebox.showerror("Insufficient", "Not enough cash")
        return

    change = cash - total
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # =========================
    # RECEIPT WINDOW
    # =========================
    receipt_win = tk.Toplevel(root)
    receipt_win.title("Receipt")
    receipt_win.geometry("400x500")
    receipt_win.configure(bg="white")

    title = tk.Label(
        receipt_win,
        text="EVONNE ANGEL'S BURGER POS",
        font=("Segoe UI", 16, "bold"),
        bg="white"
    )
    title.pack(pady=10)

    date_label = tk.Label(
        receipt_win,
        text=time_now,
        bg="white",
        fg="gray"
    )
    date_label.pack()

    receipt_box = tk.Text(
        receipt_win,
        width=45,
        height=20,
        font=("Consolas", 10)
    )
    receipt_box.pack(pady=10)

    receipt_box.insert(tk.END, "=================================\n")

    for item in cart:

        subtotal = item["qty"] * item["price"]

        receipt_box.insert(
            tk.END,
            f"{item['name']}\n"
        )

        receipt_box.insert(
            tk.END,
            f"{item['qty']} x ₱{item['price']} = ₱{subtotal}\n\n"
        )

    receipt_box.insert(tk.END, "=================================\n")
    receipt_box.insert(tk.END, f"TOTAL  : ₱{total}\n")
    receipt_box.insert(tk.END, f"CASH   : ₱{cash}\n")
    receipt_box.insert(tk.END, f"CHANGE : ₱{change}\n")
    receipt_box.insert(tk.END, "=================================\n")
    receipt_box.insert(tk.END, "\nTHANK YOU FOR YOUR ORDER MAEM!")

    receipt_box.config(state="disabled")

    # CLEAR CART
    cart.clear()
    cash_var.set("")
    update_cart()

# =========================
# VIEW ORDERS
# =========================
def view_orders():
    win = tk.Toplevel(root)
    win.title("Orders")
    win.geometry("600x400")

    listbox = tk.Listbox(win)
    listbox.pack(fill="both", expand=True)

    def refresh():
        listbox.delete(0, tk.END)
        for i, o in enumerate(orders_history):
            listbox.insert(tk.END, f"{i+1}. {o['time']} | ₱{o['total']}")

    def delete_order():
        sel = listbox.curselection()
        if not sel:
            return

        i = sel[0]
        orders_history.pop(i)

        with open(ORDERS_FILE, "w") as f:
            for o in orders_history:
                f.write(f"\nTIME: {o['time']}\n")
                for item in o["items"]:
                    f.write(f"{item['name']} x{item['qty']} = ₱{item['price']*item['qty']}\n")
                f.write(f"TOTAL: ₱{o['total']}\n")
                f.write("-"*40 + "\n")

        refresh()

    tk.Button(win, text="Delete Order", bg=RED, fg="white",
              font=("Segoe UI", 12, "bold"), command=delete_order).pack(pady=5)

    refresh()


# =========================
# SALES DASHBOARD
# =========================
def sales_dashboard():
    win = tk.Toplevel(root)
    win.title("Sales Dashboard")
    win.geometry("500x400")

    tk.Label(win, text="DAILY SALES",
             font=("Segoe UI", 18, "bold")).pack()

    text = tk.Text(win)
    text.pack(fill="both", expand=True)

    total_all = 0

    for d, t in sales_by_date.items():
        text.insert(tk.END, f"{d} : ₱{t}\n")
        total_all += t

    text.insert(tk.END, f"\nTOTAL SALES: ₱{total_all}")


# =========================
# OPTIONS WINDOW
# =========================
def open_options(product):
    win = tk.Toplevel(root)
    win.title(product["name"])
    win.geometry("300x350")

    selected_flavor = tk.StringVar()
    selected_size = tk.StringVar(value="Small")

    tk.Label(win, text=product["name"],
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    options = []

    if product["name"] == "MilkTea":
        options = ["Cookies & Cream", "Mango", "Strawberry"]
    elif product["name"] == "Softdrinks":
        options = ["Coke", "Pepsi", "Royal"]
    elif product["name"] == "French Fries":
        options = ["Barbeque", "Sour Cream", "Cheese", "Salt"]

    for opt in options:
        tk.Radiobutton(win, text=opt,
                       variable=selected_flavor, value=opt).pack(anchor="w")

    tk.Label(win, text="Size").pack(pady=10)

    for s in ["Small", "Medium", "Large"]:
        tk.Radiobutton(win, text=s,
                       variable=selected_size, value=s).pack(anchor="w")

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

    tk.Button(win, text="Add", bg=GREEN, fg="white",
              font=("Segoe UI", 12, "bold"),
              command=confirm).pack(pady=15)


# =========================
# UI ROOT
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
         bg=CARD, fg=TEXT,
         font=("Segoe UI", 18, "bold")).pack(pady=10)

columns = ("Product", "Flavor", "Size", "Qty", "Price")
cart_table = ttk.Treeview(order_frame, columns=columns, show="headings", height=15)

for col in columns:
    cart_table.heading(col, text=col)
    cart_table.column(col, width=80)

cart_table.pack(padx=10)

total_label = tk.Label(order_frame, text="TOTAL: ₱0",
                       bg=CARD, fg=PRIMARY,
                       font=("Segoe UI", 20, "bold"))
total_label.pack(pady=10)

tk.Label(order_frame, text="Cash:", bg=CARD).pack()
tk.Entry(order_frame, textvariable=cash_var).pack()

btn_frame = tk.Frame(order_frame, bg=CARD)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Remove", bg=RED, fg="white",
          command=remove_item).grid(row=0, column=0)

tk.Button(btn_frame, text="Clear", bg=LIGHT, fg="white",
          command=clear_cart).grid(row=0, column=1)

tk.Button(order_frame, text="Checkout", bg=GREEN, fg="white",
          font=("Segoe UI", 14, "bold"),
          command=checkout).pack(pady=10)


# =========================
# CATEGORIES
# =========================
category_frame = tk.Frame(center_frame, bg=BG)
category_frame.pack(pady=10)

categories = ["Home", "Special" ,"Burger", "Snacks", "Drinks", "Sauces"]


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

    tk.Button(home, text="VIEW ORDERS",
              bg=PRIMARY, fg="white",
              font=("Segoe UI", 14, "bold"),
              width=20, height=2,
              command=view_orders).pack(pady=8)

    tk.Button(home, text="SALES DASHBOARD",
              bg=PRIMARY, fg="white",
              font=("Segoe UI", 14, "bold"),
              width=20, height=2,
              command=sales_dashboard).pack(pady=8)


def show_category(cat):
    if cat == "Home":
        show_home()
    else:
        display_products(cat)


for i, cat in enumerate(categories):
    btn = tk.Button(category_frame, text=cat,
                    bg=PRIMARY, fg="white",
                    font=("Segoe UI", 14, "bold"),
                    width=12, height=2)

    btn.config(command=lambda b=btn, c=cat: (highlight_button(b), show_category(c)))
    btn.grid(row=0, column=i, padx=5)


# =========================
# PRODUCTS DISPLAY 
# =========================
def display_products(category):
    for w in center_frame.winfo_children():
        if w != category_frame:
            w.destroy()

    grid = tk.Frame(center_frame, bg=BG)
    grid.pack()

    row = col = 0

    CARD_WIDTH = 200
    CARD_HEIGHT = 160


    icon_map = {
        "MilkTea": "🧋",
        "Softdrinks": "🥤",
        "Iced Coffee": "☕",
        "Orange Juice": "🧃",
        "Lemonade": "🍋",
        "Water Bottle": "💧",
        "Hot Coffee": "☕",

        "French Fries": "🍟",
        "Onion Rings": "🧅",
        "Chicken Nuggets": "🍗",
        "Cheese Sticks": "🧀",
        "Hotdog Bites": "🌭",
        "Hash Brown": "🥔",

        "Ketchup": "🍅",
        "Mayonnaise": "🧴",
        "Cheese Dip": "🧀",
        "Barbecue Sauce": "🥫",
        "Garlic Mayo": "🧄",
        "Spicy Sauce": "🌶️",
    }

    for product in products:
        if product["category"] != category:
            continue

        card = tk.Frame(grid, bg=CARD,
                        width=CARD_WIDTH, height=CARD_HEIGHT)
        card.grid(row=row, column=col, padx=10, pady=10)

        card.grid_propagate(False)
        card.pack_propagate(False)

        icon = icon_map.get(product["name"], "🍔")

        tk.Label(card, text=icon, bg=CARD,
                 font=("Segoe UI", 25)).pack(pady=(5, 0))

        tk.Label(card, text=product["name"],
                 bg=CARD, font=("Segoe UI", 11, "bold"),
                 wraplength=160, justify="center").pack()

        tk.Label(card, text=f"₱{product['price']}",
                 bg=CARD).pack()

        tk.Button(card, text="Add",
                  bg=PRIMARY, fg="white",
                  command=lambda p=product:
                      open_options(p) if p["name"] in ["MilkTea", "Softdrinks", "French Fries"]
                      else add_to_cart(p)).pack(pady=5)

        col += 1
        if col == 3:
            col = 0
            row += 1


# =========================
# START
# =========================
show_home()
root.mainloop()