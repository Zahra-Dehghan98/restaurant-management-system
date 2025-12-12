# import sql
import psycopg2
from psycopg2 import sql

# connect to database
def get_connection():
    return psycopg2.connect (
        dbname="restaurant_db",
        user="postgres",
        password="0914zahra",
        host="localhost",
        port="5432"
)


#=========================================
#manage_menu_items

#add items to menu
def add_menu_items():
    name = input("enter food name:")
    while True:
        try:
            price = float(input("enter food price:"))
            if price <= 0:
                print("Price must be greater than zero")
                continue
            break
        except ValueError:
            print("Price must be a number")

    print(f"{name} added with price {price}")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute (
         "INSERT INTO menu_items (name, price) VALUES (%s, %s)",(name, price)
         )
    conn.commit()
    cur.close()
    conn.close()

#edit items in menu
def edit_menu_item_price():
        while True:
            edit_item = input("enter food id:")
            if edit_item.lower == "cancel":
                print("edit item cancelled.")
                return
            try:
                 edit_item= int(edit_item)
                 break
            except:
                 print("ID must be a number. Try again.")
#get new price
        while True:
            try:
                new_price = float(input("enter new price:"))
                if new_price <= 0:
                    print("Price must be greater than zero")
                    continue
                break
            except:
                print("Price must be a number")

        conn = get_connection()
        cur = conn.curser
        cur.execute (
             "update menu_items set price = %s where id = %s"
             (new_price, edit_item)
        )
        if cur.rowvount == 0:
            print("id not found")
        else:
            print("price updated")
        conn.commit()
        conn.close()
        cur.close()

def show_menu():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("select * from menu_items")
    print("\n---Food Menu---")
    print("  ID  |  Name  |  Price  ")
    print("--------------------------")

    for food in cur:
        print(f"{food[0]}, {food[1]}, {food[2]}$")
    cur.close()
    conn.close()
#=========================================
