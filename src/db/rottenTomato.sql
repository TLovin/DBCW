CREATE TEMPORARY TABLE movie_db.rottenTomatoRating(
    rotten_tomatoes_link VARCHAR(255) NOT NULL,
    movieTitle VARCHAR(255) NOT NULL,
    movieInfo VARCHAR(255)  NOT NULL,
    review TEXT NOT NULL,
    posterImage VARCHAR(255) NOT NULL,
    pgRating VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    director VARCHAR(255) NOT NULL,
    writer VARCHAR(255) NOT NULL,
    cast1 VARCHAR(255) NOT NULL,
    in_theaters_year VARCHAR(255) NOT NULL,
    on_streaming_date VARCHAR(255) NOT NULL,
    runtime_in_minutes VARCHAR(255) NOT NULL,
    studio_name VARCHAR(255) NOT NULL,
    tomatometer_status VARCHAR(255) NOT NULL,
    tomatometer_rating VARCHAR(255) NOT NULL,

    PRIMARY KEY (rotten_tomatoes_link)
);

LOAD DATA INFILE '../../ml-latest-small/rotten.csv'
INTO TABLE movie_db.rottenTomatoRating
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n' ;


ALTER TABLE movie_db.rottenTomatoRating
DROP review,
DROP on_streaming_date,
DROP tomatometer_status ,
DROP runtime_in_minutes,
DROP  studio_name,
DROP  genre;

UPDATE movie_db.rottenTomatoRating
SET in_theaters_year= SUBSTRING_INDEX(in_theaters_year, '-', 1);


CREATE TABLE movie_db.rotten
SELECT DISTINCT  movie_db.movies.title,movie_db.rottenTomatoRating.movieInfo,movie_db.rottenTomatoRating.posterImage,movie_db.rottenTomatoRating.director,movie_db.rottenTomatoRating.writer,movie_db.rottenTomatoRating.cast1,movie_db.rottenTomatoRating.tomatometer_rating


FROM movie_db.movies LEFT JOIN movie_db.rottenTomatoRating
ON movie_db.movies.title= movie_db.rottenTomatoRating.movieTitle AND movie_db.movies.year = movie_db.rottenTomatoRating.in_theaters_year;#LIKE CONCAT(movie_db.rottenTomatoRating.movieTitle,"%") #AND movie_db.movies.year LIKE CONCAT(movie_db.rottenTomatoRating.in_theaters_date,"%")

-- ## query to get details of the movie 
-- #SELECT * FROM rotten WHERE title = 'movieName';