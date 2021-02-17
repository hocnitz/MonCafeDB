import sqlite3
import os
import atexit
import sys

if os.path.isfile('moncafe.db'):
    os.remove('moncafe.db')
dbcon = sqlite3.connect('moncafe.db')
cursor = dbcon.cursor()


def insert_employee(param):
    cursor.execute("""INSERT INTO Employees VALUES (?, ?, ?, ?)""", param)


def insert_supplier(param):
    val1 = param[0]
    val2 = param[1]
    val3 = param[2]
    if val3[-1:] == "\n":
        val3 = val3[:-1]
    cursor.execute("""INSERT INTO Suppliers VALUES (?, ?, ?)""", (val1, val2, val3))


def insert_product(param):
    cursor.execute("""INSERT INTO Products VALUES (?, ?, ?, 0)""", param)


def insert_stand(param):
    cursor.execute("""INSERT INTO Coffee_stands VALUES (?, ?, ?)""", param)


def line_to_table(line):
    words = line.split(", ")
    conf = words[0]
    if conf == "E":
        insert_employee(words[1:])
    elif conf == "S":
        insert_supplier(words[1:])
    elif conf == "P":
        insert_product(words[1:])
    elif conf == "C":
        insert_stand(words[1:])


def print_table_as_a_table(table):
    cursor.execute('SELECT * FROM ' + table);
    list = cursor.fetchall()
    print("\nAll {} as a table:\n-------------------------".format(table))
    i=0
    for item in list:
        i=i+1
        print("item{}: {}".format(i, str(item)))



def main(argv):
    filepath = argv[1]
    create_table()
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line_to_table(line)
            line = fp.readline()
    fp.close()



def create_table():

    cursor.execute(""" CREATE TABLE Employees(id  INTEGER PRIMARY KEY,
                        name  TEXT NOT NULL,
                        salary REAL NOT NULL,
                        coffee_stand INTEGER REFERENCES Coffee_stand(id))  
                        """)
    cursor.execute(""" CREATE TABLE Coffee_stands(id  INTEGER PRIMARY KEY,
                                               location  TEXT NOT NULL,
                                               number_of_employees  INTEGER
                                               )
                                            """)
    cursor.execute(""" CREATE TABLE Suppliers(id INTEGER PRIMARY KEY,
                                              name TEXT NOT NULL,
                                              contact_information TEXT
                                                )
                                            """)
    cursor.execute(""" CREATE TABLE Products(id INTEGER PRIMARY KEY,
                                                description  TEXT NOT NULL,
                                                price  REAL NOT NULL,
                                                quantity  INTEGER NOT NULL
                                                )
                                            """)
    cursor.execute(""" CREATE TABLE Activities(product_id  INTEGER REFERENCES Products(id),
                                                quantity  INTEGER NOT NULL,
                                                activator_id  INTEGER NOT NULL,
                                                date  DATE NOT NULL
                                                )
                                            """)


if __name__ == "__main__":
    main(sys.argv)


#Define a function to be called when the interpreter terminates
def close_db():
    dbcon.commit()
    dbcon.close()
    # os.remove('moncafe.db')   #Just for debug

#register close_db to be called when the interpreter terminates
atexit.register(close_db)
