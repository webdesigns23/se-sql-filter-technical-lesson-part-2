# Technical Lesson Part 2: Filtering Data with SQL

## Instructions

Now, we'll walk through executing a handful of common and handy SQL queries that use WHERE with conditional operators. We'll start with an example of what this type of query looks like, then type a query specifically related to the cats table.
<br /><br />
For this section as the queries get more advanced we'll be using a simpler database called pets_database.db containing a table called cats.
<br /><br />
The cats table is populated with the following data:

| id | name      | age  | breed              | owner_id |
|----|-----------|------|--------------------|----------|
| 1  | Maru      | 3.0  | Scottish Fold      | 1.0      |
| 2  | Hana      | 1.0  | Tabby              | 1.0      |
| 3  | Lil' Bub  | 5.0  | American Shorthair | NaN      |
| 4  | Moe       | 10.0 | Tabby              | NaN      |
| 5  | Patches   | 2.0  | Calico             | NaN      |
| 6  | None      | NaN  | Tabby              | NaN      |

***Cats Table Dataset***

Below we make a new database connection and read all of the data from this table:

```python
conn = sqlite3.connect('pets_database.db')
cursor = conn.cursor()
cats_data = pd.read_sql("SELECT * FROM cats;", conn)
print(cats_data)
```

Output:

| #  | id | name      | age  | breed              | owner_id |
|----|----|-----------|------|--------------------|----------|
| 0  | 1  | Maru      | 3.0  | Scottish Fold      | 1.0      |
| 1  | 2  | Hana      | 1.0  | Tabby              | 1.0      |
| 2  | 3  | Lil' Bub  | 5.0  | American Shorthair | NaN      |
| 3  | 4  | Moe       | 10.0 | Tabby              | NaN      |
| 4  | 5  | Patches   | 2.0  | Calico             | NaN      |
| 5  | 6  | None      | NaN  | Tabby              | NaN      |

***Data Output using read_sql***

### Step 1: `WHERE` with `>=`

For the `=`, `!=`, `<`, `<=`, `>`, and `>=` operators, the query looks like:

```sql
SELECT column/s
 FROM table_name
 WHERE <column_name> <operator> <value>;
```

Note: The example above is not valid SQL, it is a template for how the queries are constructed.

We type the SQL query between the quotes to select all cats who are at least 5 years old:

```python
older_cats = pd.read_sql("""
SELECT *
 FROM cats
WHERE age >= 5;
""", conn)

print(older_cats)
```

This should return:

| id | name      | age  | breed              | owner_id |
|----|-----------|------|--------------------|----------|
| 3  | Lil' Bub  | 5.0  | American Shorthair | None     |
| 4  | Moe       | 10.0 | Tabby              | None     |

***SQL query output: cats at least 5 y.o.***

### Step 2: `WHERE` with `BETWEEN`

If we wanted to select all rows with values in a range, we could do this by combining the `<=` and AND operators. However, since this is such a common task in SQL, there is a shorter and more efficient command specifically for this purpose, called `BETWEEN`.

A typical query with `BETWEEN` looks like:

```sql
SELECT column_name(s)
  FROM table_name
  WHERE column_name BETWEEN value1 AND value2;
```

Note that `BETWEEN` is an inclusive range, so the returned values can match the boundary values (not like `range()` in Python).

Let's say we need to select the names of all of the cats whose age is between 1 and 3. We'll type the SQL query between the quotes below to select all cats who are in this age range:

```python
young_adult_cats = pd.read_sql("""
SELECT *
  FROM cats
  WHERE age BETWEEN 1 AND 3;
""", conn)

print(young_adult_cats)
```

This should return:

| id | name     | age  | breed         | owner_id |
|----|----------|------|---------------|----------|
| 1  | Maru     | 3.0  | Scottish Fold | 1.0      |
| 2  | Hana     | 1.0  | Tabby         | 1.0      |
| 3  | Patches  | 2.0  | Calico        | NaN      |

***SQL query: cats 1-3 y.o.***

### Step 3: `WHERE` Column Is Not `NULL`

`NULL` in SQL represents missing data. It is similar to `None` in Python or `NaN` in NumPy or pandas. However, we use the `IS` operator to check if something is `NULL`, not the `=` operator (or `IS NOT` instead of `!=`).
<br /><br />
To check if a value is `NULL` (or not), the query looks like:

```sql
SELECT column(s)
  FROM table_name
  WHERE column_name IS (NOT) NULL;
```

You might have noticed when we selected all rows of cats, some owner IDs were `NaN`, then in the above query they are None instead. This is a subtle difference where Python/pandas is converting SQL `NULL` values to `NaN` when there are numbers in other rows, and converting to None when all of the returned values are `NULL`. This is a subtle difference that you don't need to memorize; it is just highlighted to demonstrate that the operators we use in SQL are similar to Python operators, but not quite the same.
<br /><br />

If we want to select all cats that don't currently belong to an owner, we want to select all cats where the `owner_id` is `NULL`.
<br /><br />

We'll type the SQL query between the quotes below to select all cats that don't currently belong to an owner:

```python
ownerless_cats = pd.read_sql("""
SELECT *
  FROM cats
WHERE owner_id IS NULL;
""", conn)

print(ownerless_cats)
```

This should return:

| id | name      | age  | breed              | owner_id |
|----|-----------|------|--------------------|----------|
| 3  | Lil' Bub  | 5.0  | American Shorthair | None     |
| 4  | Moe       | 10.0 | Tabby              | None     |
| 5  | Patches   | 2.0  | Calico             | None     |
| 6  | None      | NaN  | Tabby              | None     |

***SQL query: cats without owner***

### Step 4: `WHERE` with `LIKE`

The `LIKE` operator is very helpful for writing SQL queries with messy data. It uses wildcards to specify which parts of the string query need to be an exact match and which parts can be variable.
<br /><br />

When using `LIKE`, a query looks like:

```sql
SELECT column(s)
  FROM table_name
  WHERE column_name LIKE 'string_with_wildcards';
```

The most common wildcard you'll see is `%`. This is similar to the * wildcard in Bash or regex: it means zero or more characters with any value can be in that position.
<br /><br />

So for example, if we want all cats with names that start with "M", we could use a query containing `M%`. This means that we're looking for matches that start with one character "M" (or "m", since this is a case-insensitive query in SQLite) and then zero or more characters that can have any value.
<br /><br />

We'll type the SQL query between the quotes below to select all cats with names that start with "M" (or "m"):

```python
cats_starting_with_m = pd.read_sql("""
SELECT *
  FROM cats
 WHERE name LIKE 'M%';
""", conn)

print(cats_starting_with_m)
```

This should return:

| id | name | age  | breed         | owner_id |
|----|------|------|---------------|----------|
| 1  | Maru | 3.0  | Scottish Fold | 1.0      |
| 4  | Moe  | 10.0 | Tabby         | NaN      |

***SQL query: cat names starting with "M"***

Note that we also could have used the `substr` SQL built-in function here to perform the same task:

```python
pd.read_sql("""
SELECT *
  FROM cats
 WHERE substr(name, 1, 1) = "M";
""", conn)
```

Unlike in Python where:
> There should be one-- and preferably only one --obvious way to do it. (Zen of Python)

There will often be multiple valid approaches to writing the same SQL query. Sometimes one will be more efficient than the other, and sometimes the only difference will be a matter of preference.
<br /><br />

The other wildcard used for comparing strings is `_`, which means exactly one character, with any value.
<br /><br />

For example, if we wanted to select all cats with four-letter names where the second letter was "a", we could use `_a__`.
<br /><br />

We'll type the SQL query between the quotes below to select all cats with names where the second letter is "a" and the name is four letters long:

```python
pd.read_sql("""
SELECT *
  FROM cats
 WHERE name LIKE '_a__';
""", conn)
```

This should return:

| id | name | age | breed         | owner_id |
|----|------|-----|---------------|----------|
| 1  | Maru | 3   | Scottish Fold | 1        |
| 2  | Hana | 1   | Tabby         | 1        |

***SQL query: cats with 2nd letter "a" in name***

Again, we could have done this using length and substr, although it would be much less concise:

```python
pd.read_sql("""
SELECT *
  FROM cats
 WHERE length(name) = 4 AND substr(name, 2, 1) = "a";
""", conn)
```

These examples are a bit silly, but you can imagine how this technique would help to write queries between multiple datasets where the names don't quite match exactly. You can combine `%` and `_` in your string to narrow and expand your query results as needed.

### Step 5: Filter and Aggregate

Now, let's talk about the SQL aggregate function `COUNT`.
<br /><br />

SQL aggregate functions are SQL statements that can get the average of a column's values, retrieve the minimum and maximum values from a column, sum values in a column, or count a number of records that meet certain conditions. You can learn more about these SQL aggregators here and here.
<br /><br />

For now, we'll just focus on `COUNT`, which counts the number of records that meet a certain condition. Here's a standard SQL query using `COUNT`:

```sql
SELECT COUNT(column_name)
  FROM table_name
  WHERE conditional_statement;
```

Let's try it out and count the number of cats who have an `owner_id` of 1. We'll type the SQL query between the quotes below:

```python
pd.read_sql("""
SELECT COUNT(owner_id)
  FROM cats
 WHERE owner_id = 1;
""", conn)
```

This should return:

| # | COUNT(owner_id) |
|---|------------------|
| 0 | 2                |

***SQL Query: cats with owner_id of 1***


Finally, close our database connection at the bottom of our code:
```
conn.close()
```
