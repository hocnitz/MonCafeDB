import sqlite3
import os
import atexit
import sys


dbcon = sqlite3.connect('moncafe.db')
cursor = dbcon.cursor()


def print_table_as_a_table(table):
    if table == "Activities":
        cursor.execute('SELECT * FROM ' + table + " ORDER BY date")
    else:
        cursor.execute('SELECT * FROM ' + table+ " ORDER BY id")
    list = cursor.fetchall()
    for item in list:
        print(item)


def create_Employee_report():
    print("Employee report")

    # cursor.execute(""" SELECT Employees.name, Employees.salary, Coffee_stands.location,SUM TOTAL FROM SELECT Activities.activator_id, Activities.quantity*Products.price as TOTAL FROM Activities,Products WHERE Products.id=Activities.product_id WHERE
    #                     FROM Employees JOIN Coffee_stands ON Employees.coffee_stand = Coffee_stands.id
    #                  """)

    # cursor.execute("""SELECT total_sum FROM (SELECT  Emp_id, SUM(activity_sale_sum) as total_sum FROM (SELECT Emp_id , quantity*price as activity_sale_sum FROM (SELECT Activities.activator_id as Emp_id, Activities.quantity as quantity, Products.price as price
    #                     FROM Activities LEFT JOIN Products ON Activities.product_id = Products.id)) group by Emp_id )
    #                  """)
    cursor.execute("""SELECT Employees.name as name, Employees.salary, Coffee_stands.location, total_sum 
                    FROM Employees LEFT JOIN Coffee_stands ON Employees.coffee_stand = Coffee_stands.id 
                    LEFT JOIN (SELECT  Emp_id, SUM(activity_sale_sum) as total_sum FROM (SELECT Emp_id , quantity*price as activity_sale_sum FROM (SELECT Activities.activator_id as Emp_id, Activities.quantity as quantity, Products.price as price
                        FROM Activities LEFT JOIN Products ON Activities.product_id = Products.id)) group by Emp_id ) ON Employees.id = Emp_id order by name
                     """)

    list = cursor.fetchall()
    for item in list:
        print(str(item[0]) + " " + str(item[1]) + " " + str(item[2]) + (" {}").format("0" if item[3] is None else str(item[3]*-1)))



def create_Activity_report():
    print("Activities")

    cursor.execute("""SELECT Activities.date as act_date, Products.description, Activities.quantity, Employees.name, Suppliers.name FROM 
                    Activities LEFT JOIN Products ON Activities.Product_id = Products.id
                    LEFT JOIN Employees ON Activities.activator_id = Employees.id
                    LEFT JOIN Suppliers ON Activities.activator_id = Suppliers.id order by act_date""")

    list = cursor.fetchall()
    for item in list:
        print(item)


def print_db():
    print("Activities")
    print_table_as_a_table("Activities")
    print("Coffee stands")
    print_table_as_a_table("Coffee_stands")
    print("Employees")
    print_table_as_a_table("Employees")
    print("Products")
    print_table_as_a_table("Products")
    print("Suppliers")
    print_table_as_a_table("Suppliers")
    print("")
    create_Employee_report()
    print("")
    create_Activity_report()


def main():
    print_db()


if __name__ == "__main__":
    main()


# Define a function to be called when the interpreter terminates
def close_db():
    dbcon.commit()
    dbcon.close()
    # os.remove('moncafe.db')   #Just for debug


# register close_db to be called when the interpreter terminates
atexit.register(close_db)
