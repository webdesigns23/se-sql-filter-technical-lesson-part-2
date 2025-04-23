import sqlite3
import pandas as pd

conn = sqlite3.connect('pets_database.db')
cursor = conn.cursor()
cats_data = pd.read_sql("SELECT * FROM cats;", conn)
print(cats_data)