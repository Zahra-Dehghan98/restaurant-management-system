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
        table_num = input("enter table number:")
        if table_num.lower() == "cancel":
            print("order cancelled.")
            return
        try:
            table_num = int(table_num)
            break
        except ValueError:
            print("table number must be a number. Try again.")

    order_status = 'received'
    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("select id, status from tables where table_number = %s  and status = 'available'",
                 (table_num,))
    exist = cur.fetchone()
    if not exist:
        print(f"table {table_num} not found or occupied")
        cur.close()
        conn.close()
        return
    
    cur.execute (
         "INSERT INTO orders (table_id , status) VALUES (%s,%s) returning id",
         (exist[0], order_status)
         )
        
    order_id = cur.fetchone()[0]
    print(f"order #{order_id} registered for table #{table_num}")
    cur.execute (
            "update tables set status = 'occupied' where table_number = %s",
            (table_num,))
    

    total_items = 0    
    while True:
        show_menu()
        item_input = input("\ninput item id")
        if item_input == "0":
            if total_items == 0:
                print("Order must have at least one item!")
                continue 
            break
        total_items += 1
        try:
            item_id = int(item_input)
        except ValueError:
            print("Please enter a valid number.")
            continue
        cur.execute("SELECT name, price FROM menu_items WHERE id = %s", (item_id,))
        item = cur.fetchone()
        
        if not item:
            print(f"Item {item_id} not found in menu!")
            continue
        while True:
            quantity_input = input("Enter quantity:")
            try:
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("Quantity must be greater than 0!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        cur.execute("insert into order_details (order_id, item_id, quantity) values (%s, %s, %s)", (order_id, item_id, quantity))
        print(f"Added {quantity}x {item[0]}")
    conn.commit()
    cur.close()
    conn.close()
    print(f" Order {order_id} completed with {total_items} items!")

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
            "update tables set status = 'available' where id = (select table_id from orders where id =%s)", (or_id,) )
    
    if cur.rowcount == 0:
        print("id not found")
    else:
        print("status updated")
    conn.commit()
    cur.close()
    conn.close()
#==============================================================================
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
    while True:
        order_id = input("Enter Order ID: ")
        if order_id.lower() == "cancel":
            print("Cancelled.")
            return
        try:
            order_id = int(order_id)
            break
        except ValueError:
            print("Please enter a valid number.")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """select order_details.*, menu_items.name, menu_items.price
          from order_details
          join menu_items on order_details.item_id = menu_items.id 
          where order_details.order_id = %s""", (order_id,))
    print(f"\n---Order {order_id} details---")
    print("===================================")
    print("  ID  |  order_id  |  item_id  |  name  |  quantity  |  price  ")
    print("-------------------------------------------------------------------------")
    total = 0
    found = False
    for i in cur:
        print(f"{i[0]} |  {i[1]} |  {i[2]}  |  {i[3]}  |  {i[4]}  |  {i[5]}  |")
        total += i[4] * i[5]
        found = True
    
    print("===================================")
    if found:
        print(f"TOTAL: {total}")
    else:
        print(f"No items found for Order #{order_id}")
    cur.close()
    conn.close()

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

#CLI

def manage_tables_menu():
    while True:
        print("\n--- Table Management ---")
        print("1. Add a new table")
        print("2. Remove a table")
        print("3. Back to main menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_table()
        elif choice == "2":
            remove_table()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

def main_menu():
    while True:
        print("===================================")
        print("\n---Restaurant Management System---")
        print("===================================")
        print("1. Show Menu")
        print("2. Show Table Status")
        print("3. Add New Order")
        print("4. Update Order Status")
        print("5. View Order Details & Total Price")
        print("6. Show Daily Sales Report")
        print("7. Manage Tables")
        print("8. Exit")
        print("--------------------------------------------")
        choice = input("select an option (1-8):")
        if choice == "1":
            show_menu()
        elif choice == "2":
            show_tables_status()
        elif choice == "3":
            add_order()
        elif choice == "4":
            update_order_status()
        elif choice == "5":
            show_order_details()
        elif choice == "6":
            get_daily_sales_report()
        elif choice == "7":
            manage_tables_menu()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

# Run main menu when file is executed directly
if __name__ == "__main__":
    main_menu()