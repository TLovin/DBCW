from flask import Flask, render_template, request
import os
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
import io
import base64
from markupsafe import escape

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


@app.route('/rotten_tomato_search')
def search():
    return render_template('rotten_tomato_search.html')

@app.route('/rotten_tomato_search_results', methods=['POST'])
def search_results():
     # Get search term from the form
    search_term = escape(request.form['search'])
    cur = mysql.connection.cursor()
    # Execute the search query
    query = "SELECT m.* ,GROUP_CONCAT(DISTINCT d.name SEPARATOR ', ') AS directors,GROUP_CONCAT(DISTINCT w.name SEPARATOR ', ') AS writers, GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS cast FROM movie_db.rotten m JOIN movie_db.movie_director md ON m.movieId = md.movie_id JOIN movie_db.directors d ON md.director_id = d.id JOIN movie_db.movie_writer mw ON m.movieId = mw.movie_id JOIN movie_db.writers w ON mw.writer_id = w.id JOIN movie_db.movie_cast mc ON m.movieId = mc.movie_id JOIN movie_db.casts c ON mc.cast_id = c.id WHERE m.title =  %s"
    cur.execute(query, (search_term,))
    results = cur.fetchall()
    movie_title, movieId, description, image,rating,director,writer,cast=results[0]
    return render_template('rotten_tomato_search_results.html', movie_title=movie_title,description=description, image=image,director=director,writer=writer,cast=cast,rating=rating)

@app.route('/search_visual_browsing')
def search_visual_browsing():
    return render_template('search_visual_browsing.html')

@app.route('/search_visual_browsing_results', methods=['POST'])
def search_visual_browsing_results():
    # Get search term from the form
    search_term = escape(request.form['search_1'])
    search_term_option = escape(request.form['search_options'])
    cur = mysql.connection.cursor()
    if search_term_option == "all":
        search_term_split = search_term.split(",")
        if len(search_term_split)==1:
            query = "SELECT movies.movieId, movies.title, movies.year, genres.type, AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE movies.title LIKE %s OR genres.type LIKE %s OR movies.year LIKE %s GROUP BY movies.movieId,movies.year, genres.type"
            search_matching_pattern=f'%{search_term_split[0]}%'
            cur.execute(query, (search_matching_pattern,search_matching_pattern,search_matching_pattern))
        else:
            if len(search_term_split)==2:
                query = "SELECT movies.movieId, movies.title, movies.year, genres.type, AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE movies.title LIKE %s OR genres.type LIKE %s OR movies.year LIKE %s AND (movies.title LIKE %s OR genres.type LIKE %s OR movies.year LIKE %s) GROUP BY movies.movieId,movies.year, genres.type"
                search_matching_pattern1=f'%{search_term_split[0]}%'
                search_matching_pattern2=f'%{search_term_split[1]}%'
                cur.execute(query, (search_matching_pattern1,search_matching_pattern1,search_matching_pattern1,search_matching_pattern2,search_matching_pattern2,search_matching_pattern2))

            elif len(search_term_split)==3:
                query = "SELECT movies.movieId, movies.title, movies.year, genres.type, AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE movies.title LIKE %s OR genres.type LIKE %s OR movies.year LIKE %s AND (movies.title LIKE %s OR genres.type LIKE %s OR movies.year LIKE %s) AND (movies.title LIKE %s OR genres.type LIKE %s OR movies.year LIKE %s) GROUP BY movies.movieId,movies.year, genres.type"
                search_matching_pattern1=f'%{search_term_split[0]}%'
                search_matching_pattern2=f'%{search_term_split[1]}%'
                search_matching_pattern3=f'%{search_term_split[1]}%'
                cur.execute(query, (search_matching_pattern1,search_matching_pattern1,search_matching_pattern1,search_matching_pattern2,search_matching_pattern2,search_matching_pattern2,search_matching_pattern3,search_matching_pattern3,search_matching_pattern3 ))

    elif search_term_option == "titledate":
        search_term_split = search_term.split(",")
        query = "SELECT DISTINCT movies.movieId, movies.title, movies.year, GROUP_CONCAT(DISTINCT genres.type SEPARATOR ', '), AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE movies.title=%s AND movies.year = %s GROUP BY genres.type"
        cur.execute(query, (search_term_split[0],search_term_split[1],))
    elif search_term_option == "year":
        query = "SELECT movies.movieId, movies.title, movies.year, GROUP_CONCAT(DISTINCT genres.type SEPARATOR ', '), AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE movies.year=%s GROUP BY movies.title"
        cur.execute(query, (search_term,))
    elif search_term_option == "genre":
        query = "SELECT movies.movieId, movies.title, movies.year, genres.type, AVG(ratings.rating) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE genres.type=%s GROUP BY movies.title"
        cur.execute(query, (search_term,))
    results = cur.fetchall()
    return render_template('search_visual_browsing_results.html', results=results)

@app.route('/mostleastpopularmovie', methods=['POST'])
def mostleastpopularmovie():
    genre_search_term = escape(request.form['genresearch'])
    year_search_term = escape(request.form['yearsearch'])
    search_term_option = escape(request.form['mostleast'])
    cur = mysql.connection.cursor()
    if search_term_option == "mostpopular":
        query = "SELECT COUNT(ratings.userId), movies.movieId, movies.title, movies.year, genres.type FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE genres.type=%s AND movies.year >= %s GROUP BY movies.title ORDER BY COUNT(ratings.userId) DESC;"
        cur.execute(query, (genre_search_term,year_search_term,))
    elif search_term_option == "leastpopular":
        query = "SELECT DISTINCT COUNT(ratings.userId), movies.movieId, movies.title, movies.year, genres.type FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE genres.type=%s AND movies.year >= %s GROUP BY movies.title ORDER BY COUNT(ratings.userId) ASC;"
        cur.execute(query, (genre_search_term,year_search_term,))
    results = cur.fetchall()
    return render_template('mostleastpopularmovie.html', results=results)

def generate_graph(x, y, search_term=None, x_label=None, y_label='Rating', scatter=False):
    plt.clf()
    if scatter:
        plt.scatter(x, y)
    else:
        plt.bar(x, y)

    # Add labels and title
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(f"Bar Chart, showing User {search_term} Rating History") if search_term else None
    
    # Save the figure to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    
    # Encode the buffer as a base64 string
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode()
    return graph

@app.route('/analysisOnViewersReaction')
def analysisOnViewersReaction():
    return render_template('analysisOnViewersReaction.html')

@app.route('/viewerReactionPage1', methods=['POST'])
def viewerReactionPage1():
    # Get search term from the form
    search_term = escape(request.form['userid'])
    search_term_1 = escape(request.form['moviename'])
    cur = mysql.connection.cursor()
    query = "SELECT ROUND(AVG(rating),3) FROM `ratings` WHERE userId=%s;"
    cur.execute(query, (search_term,))
    results = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    query1 = "SELECT AVG(rating) FROM `ratings` JOIN movies ON ratings.movieId=movies.movieId WHERE movies.title=%s AND ratings.userId=%s GROUP BY userId;"
    cur.execute(query1, (search_term_1,search_term,))
    results1 = cur.fetchall()
    
    cur = mysql.connection.cursor()
    query2 = "SELECT ROUND(AVG(r.rating),3) AS this_movie_rating FROM ratings r INNER JOIN moviegenres mg ON r.movieId = mg.movieId INNER JOIN genres g ON mg.genreId = g.genreId INNER JOIN movies m ON mg.movieId = m.movieId INNER JOIN ratings r2 ON r.userId = r2.userId AND r.movieId != r2.movieId INNER JOIN moviegenres mg2 ON r2.movieId = mg2.movieId INNER JOIN genres g2 ON mg2.genreId = g2.genreId WHERE m.title=%s AND g.genreId = g2.genreId GROUP BY m.movieId;"
    cur.execute(query2, (search_term_1,))
    results2 = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    query3 = "SELECT ROUND(AVG(r2.rating),3) AS other_movies_rating FROM ratings r INNER JOIN moviegenres mg ON r.movieId = mg.movieId INNER JOIN genres g ON mg.genreId = g.genreId INNER JOIN movies m ON mg.movieId = m.movieId INNER JOIN ratings r2 ON r.userId = r2.userId AND r.movieId != r2.movieId INNER JOIN moviegenres mg2 ON r2.movieId = mg2.movieId INNER JOIN genres g2 ON mg2.genreId = g2.genreId WHERE m.title=%s AND g.genreId = g2.genreId GROUP BY m.movieId;"
    cur.execute(query3, (search_term_1,))
    results3 = cur.fetchall()
    cur.close()
    
    results = ''.join([str(x) for t in results for x in t])
    results1 = ''.join([str(x) for t in results1 for x in t])
    results2 = ''.join([str(x) for t in results2 for x in t])
    results3 = ''.join([str(x) for t in results3 for x in t])
    
    x = ["All other films", search_term_1]
    y = [float(results), float(results1)]
    
    if float(results) < float(results1):
        message = f"As can be seen, User {search_term} has voted {search_term_1} ({float(results1)}) higher than they vote all other films ({float(results)})."
    else:
        message = f"As can be seen, User {search_term} has voted {search_term_1} ({float(results1)}) lower than they vote all other films ({float(results)})."
    graph = generate_graph(x,y, search_term)
    
    if float(results2) < float(results3):
        message1 = f"{search_term_1} ({float(results2)}) has been voted lower than other movies in the same genre as {search_term_1} ({float(results3)})."
    else:
        message1 = f"{search_term_1} ({float(results2)}) has been voted higher than other movies in the same genre as {search_term_1} ({float(results3)})."

    return render_template('viewerReactionPage1.html', graph=graph, message=message, message1=message1)

@app.route('/viewerReactionPage2', methods=['POST'])
def viewerReactionPage2():
    # Get search term from the form
    search_term = escape(request.form['userid'])
    search_term_1 =escape( request.form['moviename'])
    search_term_2 = escape(request.form['genrename'])
    cur = mysql.connection.cursor()
    query = "SELECT ROUND(AVG(ratings.rating),3) FROM movies JOIN moviegenres ON movies.movieId = moviegenres.movieId JOIN genres ON moviegenres.genreId = genres.genreId JOIN ratings on movies.movieId=ratings.movieId WHERE genres.type=%s AND userId=%s GROUP BY userID;"
    cur.execute(query, (search_term_2, search_term, ))
    results = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    query1 = "SELECT AVG(rating) FROM `ratings` JOIN movies ON ratings.movieId=movies.movieId WHERE movies.title=%s AND ratings.userId=%s GROUP BY userId;"
    cur.execute(query1, (search_term_1,search_term,))
    results1 = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    query2 = "SELECT ROUND(AVG(r.rating),3) AS this_movie_rating FROM ratings r INNER JOIN moviegenres mg ON r.movieId = mg.movieId INNER JOIN genres g ON mg.genreId = g.genreId INNER JOIN movies m ON mg.movieId = m.movieId INNER JOIN ratings r2 ON r.userId = r2.userId AND r.movieId != r2.movieId INNER JOIN moviegenres mg2 ON r2.movieId = mg2.movieId INNER JOIN genres g2 ON mg2.genreId = g2.genreId WHERE m.title=%s AND g.genreId = g2.genreId AND g.type=%s GROUP BY m.movieId;"
    cur.execute(query2, (search_term_1,search_term_2, ))
    results2 = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    query3 = "SELECT ROUND(AVG(r2.rating),3) AS other_movies_rating FROM ratings r INNER JOIN moviegenres mg ON r.movieId = mg.movieId INNER JOIN genres g ON mg.genreId = g.genreId INNER JOIN movies m ON mg.movieId = m.movieId INNER JOIN ratings r2 ON r.userId = r2.userId AND r.movieId != r2.movieId INNER JOIN moviegenres mg2 ON r2.movieId = mg2.movieId INNER JOIN genres g2 ON mg2.genreId = g2.genreId WHERE m.title=%s AND g.genreId = g2.genreId AND g.type=%s GROUP BY m.movieId;"
    cur.execute(query3, (search_term_1,search_term_2, ))
    results3 = cur.fetchall()
    cur.close()
    
    results = ''.join([str(x) for t in results for x in t])
    results1 = ''.join([str(x) for t in results1 for x in t])
    results2 = ''.join([str(x) for t in results2 for x in t])
    results3 = ''.join([str(x) for t in results3 for x in t])
    
    x = ["All other films", search_term_1]
    y = [float(results), float(results1)]
    # message=""
    if float(results) < float(results1):
        message = f"As can be seen, User {search_term} has voted {search_term_1} ({float(results1)}) higher than they vote all other films in the {search_term_2} category ({float(results)})."
    else:
        message = f"As can be seen, User {search_term} has voted {search_term_1} ({float(results1)}) lower than they vote all other films in the {search_term_2} category ({float(results)})."
    graph = generate_graph(x,y, search_term)

    if float(results2) < float(results3):
        message1 = f"{search_term_1} ({float(results2)}) has been voted lower than other movies in the {search_term_2} genre ({float(results3)})."
    else:
        message1 = f"{search_term_1} ({float(results2)}) has been voted higher than other movies in the {search_term_2} genre ({float(results3)})."

    return render_template('viewerReactionPage2.html', graph=graph, message=message, message1=message1)

@app.route('/search_pred')
def search2():
    return render_template('search_pred.html')


@app.route('/task5', methods=['POST'])
def task5():
    # Get search term from the form
    search_term = escape(request.form['search'])
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


@app.route('/tag_analysis')
def tag_analysis():
    return render_template('tag_analysis.html')


@app.route('/tag_analysis_results_by_genre', methods=['POST'])
def tag_analysis_results_by_genre():
    # Get search term from the form
    selected_genre = escape(request.form['genre_option'])
    cur = mysql.connection.cursor()
    query = '''WITH temp AS (
        SELECT lower(t.tag) as tag, g.`type` as genre
        FROM movie_db.tags t
        JOIN movie_db.moviegenres m
        ON t.movieId = m.movieId
        JOIN movie_db.genres g
        ON m.genreId = g.genreId
        ORDER BY 2, 1
        )
        SELECT tag, count(tag) as frequency
        FROM temp
        WHERE genre = %s
        GROUP BY tag
        ORDER BY 2 DESC, 1'''
    cur.execute(query, (selected_genre,))
    results = cur.fetchall()

    return render_template('tag_analysis_results_by_genre.html', results=results, selected_genre=selected_genre)


@app.route('/tag_analysis_results_by_rating', methods=['POST'])
def tag_analysis_results_by_rating():
    num_tags = escape(request.form['num_tags'])
    cur = mysql.connection.cursor()
    query = '''WITH temp AS (
        SELECT 
            lower(t.tag) AS tag, 
            count(lower(t.tag)) AS `count`, 
            r.rating
        FROM tags t
        left JOIN ratings r
        ON t.movieId = r.movieId
        GROUP BY 1, 3
        ORDER BY rating DESC, `count` DESC
        )
        SELECT tag, `count`, rating
        FROM 
            (SELECT 
            *, 
            row_number() OVER (Partition BY rating ORDER BY `count` DESC) AS rnum
            FROM temp) t
        WHERE rnum <= %s
        ORDER BY 3 DESC, 2 DESC'''
    cur.execute(query, (num_tags,))
    results = cur.fetchall()

    return render_template('tag_analysis_results_by_rating.html', results=results, num_tags=num_tags)


@app.route('/tag_analysis_results_by_user', methods=['POST'])
def tag_analysis_results_by_user():
    selected_genre = escape(request.form['selected_tag'])
    cur = mysql.connection.cursor()
    query = '''WITH temp as (
        SELECT lower(tag) as tag, count(lower(tag)) AS cnt 
        FROM movie_db.tags 
        GROUP BY lower(tag)  
        ORDER BY cnt DESC
        )
        SELECT userId, lower(tags.tag) as tag, count(*) as `count`, cnt as `total count`
        FROM tags
        JOIN temp
        ON tags.tag = temp.tag
        WHERE temp.tag = %s
        group by userId, lower(tag)
        order by 3 DESC, 2'''

    query_no_tag = '''WITH temp as (
        SELECT lower(tag) as tag, count(lower(tag)) AS cnt 
        FROM movie_db.tags 
        GROUP BY lower(tag)  
        ORDER BY cnt DESC
        )
        SELECT userId, lower(tags.tag) as tag, count(*) as `count`, cnt as `total count`
        FROM tags
        JOIN temp
        ON tags.tag = temp.tag
        group by userId, lower(tag)
        order by 3 DESC, 2'''
    if selected_genre:
        cur.execute(query, (selected_genre,))
    else:
        cur.execute(query_no_tag)
    results = cur.fetchall()

    return render_template('tag_analysis_results_by_user.html', results=results)

@app.route('/personality_analysis')
def personality_analysis():
    return render_template('personality_analysis.html')


@app.route('/personality_analysis_results_by_genre', methods=['POST'])
def personality_analysis_results_by_genre():
    # Get search term from the form
    selected_genre = escape(request.form['genre_option'])
    query_openness = '''SELECT openness, avg_rating
        FROM movie_db.personality_movie_analysis
        WHERE `type` = %s'''
    query_agreeableness = '''SELECT agreeableness, avg_rating
        FROM movie_db.personality_movie_analysis
        WHERE `type` = %s'''
    query_emotional_stability = '''SELECT emotional_stability, avg_rating
        FROM movie_db.personality_movie_analysis
        WHERE `type` = %s'''
    query_conscientiousness = '''SELECT conscientiousness, avg_rating
        FROM movie_db.personality_movie_analysis
        WHERE `type` = %s'''
    query_extraversion = '''SELECT extraversion, avg_rating
        FROM movie_db.personality_movie_analysis
        WHERE `type` = %s'''

    cur = mysql.connection.cursor()
    cur.execute(query_openness, (selected_genre,))
    results_openness = cur.fetchall()
    results_openness = list(map(list, zip(*results_openness)))
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute(query_agreeableness, (selected_genre,))
    results_agreeableness = cur.fetchall()
    results_agreeableness = list(map(list, zip(*results_agreeableness)))
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute(query_emotional_stability, (selected_genre,))
    results_emotional_stability = cur.fetchall()
    results_emotional_stability = list(map(list, zip(*results_emotional_stability)))
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute(query_conscientiousness, (selected_genre,))
    results_conscientiousness = cur.fetchall()
    results_conscientiousness = list(map(list, zip(*results_conscientiousness)))
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute(query_extraversion, (selected_genre,))
    results_extraversion = cur.fetchall()
    results_extraversion = list(map(list, zip(*results_extraversion)))
    cur.close()

    graph_openness = generate_graph(results_openness[0], results_openness[1], search_term=None, x_label='Openness', y_label='Rating', scatter=True)
    graph_agreeableness = generate_graph(results_agreeableness[0], results_agreeableness[1], search_term=None, x_label='Agreeableness', y_label='Rating', scatter=True)
    graph_emotional_stability = generate_graph(results_emotional_stability[0], results_emotional_stability[1], search_term=None, x_label='Emotional Stability', y_label='Rating', scatter=True)
    graph_conscientiousness = generate_graph(results_conscientiousness[0], results_conscientiousness[1], search_term=None, x_label='Conscientiousness', y_label='Rating', scatter=True)
    graph_extraversion = generate_graph(results_extraversion[0], results_extraversion[1], search_term=None, x_label='Extraversion', y_label='Rating', scatter=True)
    
    return render_template('personality_analysis_results_by_genre.html', graph_openness=graph_openness, graph_agreeableness=graph_agreeableness, graph_emotional_stability=graph_emotional_stability, graph_conscientiousness=graph_conscientiousness, graph_extraversion=graph_extraversion, selected_genre=selected_genre)


@app.route('/personality_analysis_results_by_trait', methods=['POST'])
def personality_analysis_results_by_trait():
    genres = ["Action", "Adventure", "Animation", "Children", "Comedy", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    # Get search term from the form
    personality_trait = escape(request.form['personality_trait'])
    query = '''SELECT {column}, avg_rating
        FROM movie_db.personality_movie_analysis
        WHERE `type` = %s'''

    graphs = []
    for g in genres:
        cur = mysql.connection.cursor()
        q = query.format(column=personality_trait)
        cur.execute(q, (g,))
        res = cur.fetchall()
        res = list(map(list, zip(*res)))
        cur.close()

        graph = generate_graph(res[0], res[1], search_term=None, x_label=g, y_label='Rating', scatter=True)
        graphs.append(graph)
    
    return render_template('personality_analysis_results_by_trait.html', graphs=graphs, personality_trait=personality_trait)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)