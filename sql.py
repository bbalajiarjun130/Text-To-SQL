import sqlite3

## Connect to the database
connection=sqlite3.connect('student.db')

## Create a cursor object to insert record, create table, retrieve data
cursor=connection.cursor()

# ## Create a table
# table_info = """
# CREATE Table STUDENT(
#     NAME VARCHAR(25), 
#     CLASS VARCHAR(25), 
#     SECTION VARCHAR(25), 
#     MARKS INT) 
# """

# cursor.execute(table_info)

## Insert Some more records

cursor.execute('''INSERT INTO STUDENT VALUES('Krish', 'Data Science', 'A', 90)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Rohan', 'Data Science', 'B', 85)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Sita', 'Data Science', 'A', 95)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Vikash', 'DEVOPS', 'B', 50)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Sita', 'DEVOPS', 'A', 35)''')

## Display all the records

print("The inserted records are:")
data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

## Close the connection
connection.commit()
connection.close()
