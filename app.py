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
def add_menu_item():
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
            if edit_item.lower() == "cancel":
                print("edit item cancelled.")
                return
            try:
                 edit_item= int(edit_item)
                 break
            except ValueError:
                 print("ID must be a number. Try again.")
#get new price
        while True:
            try:
                new_price = float(input("enter new price:"))
                if new_price <= 0:
                    print("Price must be greater than zero")
                    continue
                break
            except ValueError:
                print("Price must be a number")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute (
             "update menu_items set price = %s where id = %s",
             (new_price, edit_item)
        )
        if cur.rowcount == 0:
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
    print("===================================")
    print("  ID  |  Name  |  Price  ")
    print("--------------------------")

    for food in cur:
        print(f"{food[0]} |  {food[1]} |  {food[2]}$")
    cur.close()
    conn.close()
    print("===================================")
#=========================================

#mange tables

#show tables status
def show_tables_status():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select * from tables")
    print("\n---Table status🪑---")
    print("===================================")
    print("  ID  |  Table Number  |  status  ")
    print("-----------------------------------")

    for i in cur:
        print(f"{i[0]} |  {i[1]} |  {i[2]}")
    cur.close()
    conn.close()
    print("===================================")
#edit table status
def update_table_status():
    while True:
        edit_table = input("enter table id:")
        if edit_table.lower() == "cancel":
            print("edit table status cancelled.")
            return
        try:
            edit_table = int(edit_table)
            break
        except ValueError:
            print("ID must be a number. Try again.")
     
#get new status
    while True:
        new_status = input("enter new status:")
        if new_status not in ["available" , "occupied"]:
            print("enter a valid status (available or occupied)")
            continue
        break

    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("update tables set status = %s where id = %s",
             (new_status, edit_table))
    
    if cur.rowcount == 0:
        print("id not found")
    else:
        print("status updated")
    conn.commit()
    cur.close()
    conn.close()

#add table
def add_table():
    while True:    
        nt_number = input("enter table number:")
        try:
            nt_number = int(nt_number)
            break
        except ValueError:
            print("ID must be a number. Try again.")
    while True:
        new_status = input("enter new status:")
        if new_status not in ["available" , "occupied"]:
            print("enter a valid status (available or occupied)")
            continue
        break
    print(f"table added with number{nt_number} and status {new_status}")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("select * from tables where table_number = %s", (nt_number,))
    exist = cur.fetchone()
    if exist:
        print("This table number is already registered")
        return
    cur.execute (
         "INSERT INTO tables (table_number, status) VALUES (%s , %s)",
         (nt_number, new_status))
    conn.commit()
    cur.close()
    conn.close()

# delete table
def remove_table():
    while True:
        rm_table = input("enter table id:")
        if rm_table.lower() == "cancel":
            print("remove table cancelled.")
            return
        try:
            rm_table = int(rm_table)
            break
        except ValueError:
            print("ID must be a number. Try again.")
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("DELETE FROM tables WHERE id = %s and status = 'available'", (rm_table,))
    if cur.rowcount == 0:
        print("table not found or occupied")
    else:
        print(f"table {rm_table} removed successfully")
    conn.commit()
    cur.close()
    conn.close()
#=========================================================================

#manage orders

#add orders
def add_order():
    while True:
        table_id = input("enter table id:")
        if table_id.lower() == "cancel":
            print("order cancelled.")
            return
        try:
            table_id = int(table_id)
            break
        except ValueError:
            print("ID must be a number. Try again.")

    while True:
        order_status = input("enter order status:")
        if order_status not in ["preparing" , "ready", "received", "paid"]:
            print("enter a valid status")
            continue
        break
    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("select * from tables where id = %s  and status = 'available'",
                 (table_id,))
    exist = cur.fetchone()
    if exist:
        cur.execute (
         "INSERT INTO orders (table_id , status) VALUES (%s,%s)",
         (table_id,order_status)
         )
        order_id = cur.lastrowid or "unknown"
        print(f"order #{order_id} registered for table #{table_id}")
        cur.execute (
            "update tables set status = 'occupied' where id = %s",
            (table_id,))
    else:
        print("table not found or occupied")
    
    conn.commit()
    cur.close()
    conn.close()

def update_order_status():
    while True:
        or_id = input("enter order id:")
        if or_id.lower() == "cancel":
            print("edit order status cancelled.")
            return
        try:
            or_id = int(or_id)
            break
        except ValueError:
            print("ID must be a number. Try again.")
     
#get new status
    while True:
        new_status = input("enter new status:")
        if new_status not in ["preparing" , "ready", "received", "paid"]:
            print("enter a valid status")
            continue
        break

    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("update orders set status = %s where id = %s",
             (new_status, or_id))
    if new_status == 'paid':
        cur.execute (
            "update tables set status = 'available' from orders where orders.id = %s and tables.id= orders.table_id",
            (or_id,))
    
    if cur.rowcount == 0:
        print("id not found")
    else:
        print("status updated")
    conn.commit()
    cur.close()
    conn.close()
#============================================================
#Reporting 

#show active order
def show_active_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select * from orders where status not in ('paid')")
    print("\n---Active Orders---")
    print("===================================")
    print("  ID  |  tables_id  |  order_time  |  status  ")
    print("------------------------------------------------")

    for i in cur:
        print(f"{i[0]} |  {i[1]} |  {i[2]}  |  {i[3]}  ")
    cur.close()
    conn.close()
    print("===================================")

#show details order
def show_order_details():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "select order_details.*, menu_items.name, menu_items.price from order_details join menu_items on order_details.item_id = menu_items.id")
    print("\n---Order details---")
    print("===================================")
    print("  ID  |  order_id  |  item_id  |  name  |  quantity  |  price  ")
    print("-------------------------------------------------------------------------")

    for i in cur:
        print(f"{i[0]} |  {i[1]} |  {i[2]}  |  {i[3]}  |  {i[4]}  |  {i[5]}  |")
    cur.close()
    conn.close()
    print("===================================")

#report daily sales    
def get_daily_sales_report():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute (
        """select Date(orders.order_time) as order_date,
           count(distinct orders.id) as total_orders,
           sum(order_details.quantity * menu_items.price)
           from orders
           join order_details on orders.id = order_details.order_id 
           join menu_items on order_details.item_id = menu_items.id 
           where orders.status = 'paid' and Date(orders.order_time) = current_date 
           group by Date(orders.order_time)"""
    )
    row = cur.fetchone()
    cur.execute (
        """select  COUNT(*) 
           FROM orders 
           WHERE DATE(order_time) = CURRENT_DATE AND status != 'paid'""")
    unpaid_count = cur.fetchone()
    print("\n---Daily Sales---")
    print("===================================")
    print(f"Date: {row[0]}")
    print(f"Total Orders: {row[1]}")
    print(f"Paid Orders: {row[1]:}")
    print(f"Unpaid Orders: {unpaid_count[0]}")
    print(f"Total Sales: {row[2]:,}")
    cur.close()
    conn.close()
    print("===================================")
#==========================================================================