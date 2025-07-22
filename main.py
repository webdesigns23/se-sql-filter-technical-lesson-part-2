import sqlite3
import pandas as pd

conn = sqlite3.connect('pets_database.db')
cursor = conn.cursor()
cats_data = pd.read_sql("SELECT * FROM cats;", conn)
print(cats_data)

#Step 1
cats_five_and_up = pd.read_sql("""
SELECT *
 FROM cats
WHERE age >= 5;
""", conn)

print(cats_five_and_up)

#Step 2
cats_between_one_three = pd.read_sql("""
SELECT *
  FROM cats
 WHERE age BETWEEN 1 AND 3;
""", conn)

print(cats_between_one_three)

#Step 3
cats_stray = pd.read_sql("""
SELECT *
  FROM cats
WHERE owner_id IS NULL;
""", conn)

print(cats_stray)

#Step 4
cats_m = pd.read_sql("""
SELECT *
  FROM cats
 WHERE substr(name, 1, 1) = "M";
""", conn)

print(cats_m)

#Wildcard _
#Select all cats with four-letter names where the second letter was "a", we could use _a__:
second_letter_a = pd.read_sql("""
SELECT *
  FROM cats
 WHERE name LIKE '_a__';
""", conn)

print(second_letter_a)

#Again, we could have done this using length and substr, although it would be much less concise:
second_letter_a_two = pd.read_sql("""
SELECT *
  FROM cats
 WHERE length(name) = 4 AND substr(name, 2, 1) = "a";
""", conn)

print(second_letter_a_two)

#Let's try it out and count the number of cats who have an owner_id of 1
filter_aggreg = pd.read_sql("""
SELECT COUNT(owner_id)
  FROM cats
 WHERE owner_id = 1;
""", conn)

print(filter_aggreg)

conn.close()