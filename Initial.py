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