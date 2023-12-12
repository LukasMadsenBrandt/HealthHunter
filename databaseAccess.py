# import a database module
import sqlite3

from dtos import Item, User

# Only run when called from main
if __name__ == "__main__":
    print("")

    # Connect to the database, with password and username
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create tables if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (topName text, name text, price_per_unit real, link text, timeframe text)''')

    conn = None

    # function which takes in connection to database and insert an Item
    def insertItem(item: Item):
        # create a cursor object
        c = conn.cursor()
        # insert the item into the database
        c.execute(
            "INSERT INTO items VALUES (?,?,?,?,?)",
            (item.topName, item.name, item.price_per_unit, item.link, item.timeframe)
        )

        # commit the changes
        conn.commit()


    # function which takes in connection to database and returns all items
    def getAllItems():
        # create a cursor object
        c = conn.cursor()
        # select all items from the database
        c.execute("SELECT * FROM items")

        # return all items
        return c.fetchall()


    def getAllUsers():
        # create a cursor object
        c = conn.cursor()
        # select all items from the database
        c.execute("SELECT * FROM users")

        # return all items
        return c.fetchall()
