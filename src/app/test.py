import mysql.connector

# create a connection to the MySQL service
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="movie_db"
)

# create a cursor
mycursor = mydb.cursor()

# execute a MySQL query
mycursor.execute("SELECT * FROM movies")

# fetch all rows of the result set
results = mycursor.fetchall()

# iterate through the results and display them
for row in results:
  print(row)
