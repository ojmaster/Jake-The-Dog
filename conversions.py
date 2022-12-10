import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('config/prefixes.sqlite')

# Create a cursor
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS prefixes
                (guild INTEGER, prefix text)''')

# Convert the prefixes.json file into a dictionary and insert it into the database
"""with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
    for guild in prefixes:
        c.execute("INSERT INTO prefixes VALUES (?, ?)", (guild, prefixes[guild]))"""

# def change_prefix(guild, prefix):
#     c.execute("UPDATE prefixes SET prefix = ? WHERE guild = ?", (prefix, guild))
#     conn.commit()

# change_prefix(651230389171650560, ";")

conn.commit()
conn.close()