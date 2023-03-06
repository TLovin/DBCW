from flask import Flask, render_template, request
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

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    cur = mysql.connection.cursor()
    name1 = request.form.get('vehicle1')
    name2 = request.form.get('vehicle2')
    select = request.form.get('options')
    
    value=""
    cur.execute("SELECT * FROM movies")
    value = cur.fetchall()
    # cur.close()
    if name1 and select == "movieId":
        cur.execute("SELECT * FROM movies ORDER BY movieId ASC")
        value = cur.fetchall()
        # cur.close()
    if name2 and select == "movieId":
        cur.execute("SELECT * FROM movies ORDER BY movieId DESC")
        value = cur.fetchall()
        # cur.close()
    if name1 and select == "title":
        cur.execute("SELECT * FROM movies ORDER BY title ASC")
        value = cur.fetchall()
        # cur.close()
    if name2 and select == "title":
        cur.execute("SELECT * FROM movies ORDER BY title DESC")
        value = cur.fetchall()
        # cur.close()
    if name1 and select == "year":
        cur.execute("SELECT * FROM movies ORDER BY year ASC")
        value = cur.fetchall()
        # cur.close()
    if name2 and select == "year":
        cur.execute("SELECT * FROM movies ORDER BY year DESC")
        value = cur.fetchall()
        # cur.close()
    # name=request.form['name'] 
    # email=request.form['email'] 
    # password2=request.form['password2'] 
    # birthday=request.form['birthday']
    # cur.execute("insert into table_name values (%s,%s,%s,%s)",       (name,email,password2,birthday)) 
    # con.commit() 
    
    # cur.execute("SELECT * FROM movies")
    # value = cur.fetchall()
    # cur.close()
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


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_1')
def search_1():
    return render_template('search_1.html')


@app.route('/search_results', methods=['POST'])
def search_results():
     # Get search term from the form
    search_term = request.form['search']
    cur = mysql.connection.cursor()
    # Execute the search query
    query = "SELECT * FROM rotten WHERE title = %s"
    #cur.execute(f"SELECT * FROM rotten WHERE title = '{search_term}'")
    cur.execute(query, (search_term,))
    results = cur.fetchall()
   
    movie_title, description, image,director,writer,cast,rating=results[0]
    return render_template('search_results.html', movie_title=movie_title,description=description, image=image,director=director,writer=writer,cast=cast,rating=rating)

@app.route('/search_results_1', methods=['POST'])
def search_results_1():
    # Get search term from the form
    search_term = request.form['search_1']
    search_term_option = request.form['search_options']
    cur = mysql.connection.cursor()
    if search_term_option == "titledate":
        search_term_split = search_term.split(",")
        query = "SELECT DISTINCT movies.movieId, movies.title, movies.year, genres.type, AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE movies.title=%s AND movies.year = %s GROUP BY genres.type"
        cur.execute(query, (search_term_split[0],search_term_split[1],))
    elif search_term_option == "year":
        query = "SELECT movies.movieId, movies.title, movies.year, genres.type, AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE movies.year=%s GROUP BY movies.title"
        cur.execute(query, (search_term,))
    elif search_term_option == "genre":
        query = "SELECT movies.movieId, movies.title, movies.year, genres.type, AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE genres.type=%s GROUP BY movies.title"
        cur.execute(query, (search_term,))

    results = cur.fetchall()

    return render_template('search_results_1.html', results=results)

@app.route('/search_results_2', methods=['POST'])
def search_results_2():
    genre_search_term = request.form['genresearch']
    year_search_term = request.form['yearsearch']
    search_term_option = request.form['mostleast']
    cur = mysql.connection.cursor()
    if search_term_option == "mostpopular":
        query = "SELECT COUNT(ratings.userId), movies.movieId, movies.title, movies.year, genres.type FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE genres.type=%s AND movies.year >= %s GROUP BY movies.title ORDER BY COUNT(ratings.userId) DESC;"
        cur.execute(query, (genre_search_term,year_search_term,))
    elif search_term_option == "leastpopular":
        query = "SELECT DISTINCT COUNT(ratings.userId), movies.movieId, movies.title, movies.year, genres.type FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE genres.type=%s AND movies.year >= %s GROUP BY movies.title ORDER BY COUNT(ratings.userId) ASC;"
        cur.execute(query, (genre_search_term,year_search_term,))
        
    results = cur.fetchall()

    return render_template('search_results_2.html', results=results)

@app.route('/search2')
def search2():
    return render_template('search2.html')


@app.route('/task5', methods=['POST'])
def task5():
    # Get search term from the form
    search_term = request.form['search']
    cur = mysql.connection.cursor()
    # Execute the search query
    query1 = "SELECT AVG(rating) FROM (SELECT *, @counter := @counter +1 AS counter FROM (SELECT DISTINCT userId, timestamp, rating FROM movie_db.ratings,movie_db.movies WHERE movie_db.ratings.movieId = movie_db.movies.movieId AND movie_db.movies.title = %s ORDER BY movie_db.ratings.timestamp ASC) as list, (select @counter:=0) AS initvar) AS X where counter <= (ROUND(25/100 * (SELECT COUNT( DISTINCT userId, timestamp) as movies FROM movie_db.ratings,movie_db.movies WHERE movie_db.ratings.movieId = movie_db.movies.movieId AND movie_db.movies.title = %s))) ORDER BY X.timestamp ASC"
    query2 = "SELECT AVG(rating) FROM (SELECT DISTINCT userId, timestamp, rating FROM movie_db.ratings,movie_db.movies WHERE movie_db.ratings.movieId = movie_db.movies.movieId AND movie_db.movies.title = %s) as selected"
    #cur.execute(f"SELECT * FROM rotten WHERE title = '{search_term}'")
    cur.execute(query1, (search_term,search_term))
    result1 = cur.fetchall() 
    cur.execute(query2, (search_term,))
    result2 = cur.fetchall()
    results = [result1[0], result2[0]]
    return render_template('task5.html', results=results)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)