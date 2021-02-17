import sqlite3
import os
import atexit
import sys
import printdb

dbcon = sqlite3.connect('moncafe.db')
cursor = dbcon.cursor()


def action_line(line):
    words = line.split(", ")
    product_id = words[0]
    quantity = int(words[1])
    supp_id = words[2]
    date = words[3]
    cursor.execute("""SELECT quantity FROM Products WHERE id = {}""".format(product_id))
    prev_quantity = int(cursor.fetchone()[0])
    if prev_quantity + quantity >= 0:
        cursor.execute("""UPDATE Products SET quantity = {} WHERE id ={}""".format(prev_quantity+quantity, product_id))
        cursor.execute("""INSERT INTO Activities VALUES (?, ?, ?, ?)""", words)


def main(argv):
    filepath = argv[1]
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            action_line(line)
            line = fp.readline()

    fp.close()


if __name__ == "__main__":
    main(sys.argv)


# Define a function to be called when the interpreter terminates
def close_db():
    dbcon.commit()
    printdb.print_db()
    dbcon.close()
    # os.remove('moncafe.db')   #Just for debug


# register close_db to be called when the interpreter terminates
atexit.register(close_db)
