from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

connection = mysql.connector.connect(
    user='root', password='root', host='mysql', port="3306", database= 'movie_db')

print ("DB connected")

cursor = connection.cursor()

@app.route("/")
def index():
    return "Welcome nfdvhdfjdj"

# @app.route("/python")
# def python():
#     cursor.execute("select * from favourite_colours'")
#     value = cursor.fetchall()
#     return render_template("registration.html", data=value, name='Python')


if __name__ == "__main__":
    app.run(debug=True)