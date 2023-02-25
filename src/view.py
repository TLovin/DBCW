from flask import Flask, render_template
import os
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'movie_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movies')
def movies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies")
    value = cur.fetchall()
    cur.close()
    return render_template('movies.html', data=value, name='Movies')

@app.route('/genres')
def genres():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM genres")
    value = cur.fetchall()
    cur.close()
    return render_template('genres.html', data=value, name='Genres')

@app.route('/links')
def links():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM links")
    value = cur.fetchall()
    cur.close()
    return render_template('links.html', data=value, name='Links')

@app.route('/ratings')
def ratings():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ratings")
    value = cur.fetchall()
    cur.close()
    return render_template('ratings.html', data=value, name='Ratings')

@app.route('/tags')
def tags():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tags")
    value = cur.fetchall()
    cur.close()
    return render_template('tags.html', data=value, name='Tags')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)