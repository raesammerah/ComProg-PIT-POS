import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# WINDOW
root = tk.Tk()
root.title("Evonne Angel's Burger POS")
root.geometry("1100x650")
root.configure(bg="#F3F4F6")


# COLORS
BG = "#F3F4F6"
CARD = "#FFFFFF"
PRIMARY = "#4F46E5"
GREEN = "#10B981"
RED = "#EF4444"
TEXT = "#1F2937"
LIGHT = "#6B7280"


# PRODUCTS
products = [
    {"name": "Regular Burger", "price": 50},
    {"name": "Cheesy Burger", "price": 80},
    {"name": "Burger & Fries", "price": 120},
    {"name": "Burger & MilkTea", "price": 150},
    {"name": "French Fries", "price": 60},
    {"name": "MilkTea", "price": 90},
]

cart = []


# FUNCTIONS
def update_cart():
    """
    Update cart table and total
    """

    cart_table.delete(*cart_table.get_children())

    total = 0

    for item in cart:

        subtotal = item["qty"] * item["price"]

        cart_table.insert(
            "",
            tk.END,
            values=(
                item["name"],
                item["qty"],
                f"₱{item['price']}",
                f"₱{subtotal}"
            )
        )

        total += subtotal

    total_label.config(text=f"TOTAL: ₱{total}")


def add_to_cart(product):
    """
    Add product into cart
    """

    for item in cart:

        if item["name"] == product["name"]:
            item["qty"] += 1
            update_cart()
            return

    cart.append({
        "name": product["name"],
        "price": product["price"],
        "qty": 1
    })

    update_cart()


def remove_item():
    """
    Remove selected item
    """

    selected = cart_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an item."
        )
        return

    item = cart_table.item(selected)

    product_name = item["values"][0]

    for product in cart:

        if product["name"] == product_name:
            cart.remove(product)
            break

    update_cart()


def clear_cart():
    """
    Clear all items
    """

    cart.clear()
    update_cart()


def checkout():
    """
    Checkout process
    """

    if not cart:
        messagebox.showwarning(
            "Empty Cart",
            "No items in cart."
        )
        return
total = 0

receipt = ""
receipt += "================================\n"
receipt += "       EVONNE ANGEL'S BURGER\n"
receipt += f"{datetime.now()}\n"
receipt += "--------------------------------\n"

for item in cart:

        subtotal = item["qty"] * item["price"]
        total += subtotal

        receipt += (
            f"{item['name']} x{item['qty']}"
            f" = ₱{subtotal}\n"
        )

receipt += "--------------------------------\n"
receipt += f"TOTAL AMOUNT: ₱{total}\n"
receipt += "================================\n"
receipt += "      THANK YOU!\n"

messagebox.showinfo("Receipt", receipt)

cart.clear()
update_cart()

# HEADER
header = tk.Label(
    root,
    text="Evonne Angel's Burger Point of Sale",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 24, "bold")
)
header.pack(pady=20)

# MAIN FRAME
main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True)

# PRODUCTS FRAME
products_frame = tk.Frame(main_frame, bg=BG)
products_frame.pack(side="left", fill="both", expand=True, padx=20)


# ORDER FRAME
order_frame = tk.Frame(
    main_frame,
    bg=CARD,
    width=420
)
order_frame.pack(
    side="right",
    fill="y",
    padx=20,
    pady=10
)

# ORDER TITLE
order_title = tk.Label(
    order_frame,
    text="Customer Orders",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 20, "bold")
)
order_title.pack(pady=20)


# TABLE
columns = ("Product", "Qty", "Price", "Subtotal")

cart_table = ttk.Treeview(
    order_frame,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    cart_table.heading(col, text=col)
    cart_table.column(col, width=90)

cart_table.pack(padx=10)


# TOTAL LABEL
total_label = tk.Label(
    order_frame,
    text="TOTAL: ₱0",
    bg=CARD,
    fg=PRIMARY,
    font=("Segoe UI", 22, "bold")
)
total_label.pack(pady=20)

# BUTTONS

button_frame = tk.Frame(order_frame, bg=CARD)
button_frame.pack(pady=10)

remove_btn = tk.Button(
    button_frame,
    text="Remove",
    bg=RED,
    fg="white",
    relief="flat",
    font=("Segoe UI", 11, "bold"),
    padx=15,
    pady=10,
    cursor="hand2",
    command=remove_item
)
remove_btn.grid(row=0, column=0, padx=5)

clear_btn = tk.Button(
    button_frame,
    text="Clear Cart",
    bg="#6B7280",
    fg="white",
    relief="flat",
    font=("Segoe UI", 11, "bold"),
    padx=15,
    pady=10,
    cursor="hand2",
    command=clear_cart
)
clear_btn.grid(row=0, column=1, padx=5)

checkout_btn = tk.Button(
    order_frame,
    text="Checkout",
    bg=GREEN,
    fg="white",
    relief="flat",
    font=("Segoe UI", 14, "bold"),
    padx=30,
    pady=12,
    cursor="hand2",
    command=checkout
)
checkout_btn.pack(pady=20)

# PRODUCT CARDS
row = 0
col = 0

for product in products:

    card = tk.Frame(
        products_frame,
        bg=CARD,
        width=220,
        height=180,
        highlightbackground="#E5E7EB",
        highlightthickness=1
    )

    card.grid(
        row=row,
        column=col,
        padx=15,
        pady=15
    )

    card.grid_propagate(False)

    icon = tk.Label(
        card,
        text="🍔",
        bg=CARD,
        font=("Segoe UI Emoji", 35)
    )
    icon.pack(pady=(15, 5))

    name = tk.Label(
        card,
        text=product["name"],
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 14, "bold")
    )
    name.pack()

    price = tk.Label(
        card,
        text=f"₱{product['price']}",
        bg=CARD,
        fg=LIGHT,
        font=("Segoe UI", 12)
    )
    price.pack(pady=5)

    add_btn = tk.Button(
        card,
        text="Add to Cart",
        bg=PRIMARY,
        fg="white",
        relief="flat",
        font=("Segoe UI", 11, "bold"),
        padx=15,
        pady=8,
        cursor="hand2",
        command=lambda p=product: add_to_cart(p)
    )

    add_btn.pack(pady=15)

    col += 1

    if col == 3:
        col = 0
        row += 1

root.mainloop()