
import mysql.connector

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="studentinfo"
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Create Table
table_creation_query = """
CREATE TABLE IF NOT EXISTS Student_Info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    contact VARCHAR(15) UNIQUE NOT NULL,
    dob VARCHAR(25) NOT NULL,
    address TEXT NOT NULL
)
"""

cursor.execute(table_creation_query)
print("Table created successfully")

# Close the cursor and connection
cursor.close()
connection.close()
