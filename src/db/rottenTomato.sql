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
    tomatometer_rating VARCHAR(255) NOT NULL

);

LOAD DATA INFILE '../../rotten.csv'
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
SELECT DISTINCT  movie_db.movies.title,movie_db.movies.movieId, movie_db.rottenTomatoRating.movieInfo,movie_db.rottenTomatoRating.posterImage,movie_db.rottenTomatoRating.director,movie_db.rottenTomatoRating.writer,movie_db.rottenTomatoRating.cast1,movie_db.rottenTomatoRating.tomatometer_rating
FROM movie_db.movies LEFT JOIN movie_db.rottenTomatoRating
ON movie_db.movies.title= movie_db.rottenTomatoRating.movieTitle AND movie_db.movies.year = movie_db.rottenTomatoRating.in_theaters_year;#LIKE CONCAT(movie_db.rottenTomatoRating.movieTitle,"%") #AND movie_db.movies.year LIKE CONCAT(movie_db.rottenTomatoRating.in_theaters_date,"%")

-- normalising the director column 
CREATE TABLE movie_db.directors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE movie_db.movie_director (
  movie_id INT NOT NULL,
  director_id INT NOT NULL
);
ALTER TABLE movie_db.rotten ADD INDEX idx_director (director);
ALTER TABLE movie_db.directors ADD INDEX idx_name (name);


-- director table 
INSERT INTO movie_db.directors (name)
SELECT DISTINCT
  TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(m.director, ',', numbers.n), ',', -1), '\r\n', ''), '\n', ''), '\r', '')) AS director
FROM
  (select 1 n UNION ALL
  select 2 UNION ALL 
  select 3 UNION ALL
  select 4 UNION ALL 
  select 5) numbers 
  INNER JOIN movie_db.rotten m
  ON CHAR_LENGTH(m.director) - CHAR_LENGTH(REPLACE(m.director, ',', '')) >= numbers.n - 1;
-- movie director table 
INSERT INTO movie_db.movie_director
WITH temp_movies AS (
  SELECT 
    movie_db.rotten.movieId as movieId,
    TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(rotten.director, ',', numbers.n), ',', -1), '\r\n', ''), '\n', ''), '\r', '')) director
  FROM
    (select 1 n UNION ALL
    select 2 UNION ALL 
    select 3 UNION ALL
    select 4 UNION ALL 
    select 5) numbers 
    INNER JOIN movie_db.rotten
    ON CHAR_LENGTH(rotten.director) - CHAR_LENGTH(REPLACE(rotten.director, ',', '')) >= numbers.n - 1
)
SELECT temp_movies.movieId, directors.id
FROM temp_movies
JOIN movie_db.directors ON directors.name = temp_movies.director;

ALTER TABLE movie_db.rotten
DROP director;


-- normalising the writers column 
CREATE TABLE movie_db.writers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE movie_db.movie_writer (
  movie_id INT NOT NULL,
  writer_id INT NOT NULL
);
ALTER TABLE movie_db.rotten ADD INDEX idx_writer (writer);
ALTER TABLE movie_db.writers ADD INDEX idx_name (name);


-- writer table 
INSERT INTO movie_db.writers (name)
SELECT DISTINCT
  TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(m.writer, ',', numbers.n), ',', -1), '\r\n', ''), '\n', ''), '\r', '')) AS writer
FROM
  (select 1 n UNION ALL
  select 2 UNION ALL 
  select 3 UNION ALL
  select 4 UNION ALL 
  select 5) numbers 
  INNER JOIN movie_db.rotten m
  ON CHAR_LENGTH(m.writer) - CHAR_LENGTH(REPLACE(m.writer, ',', '')) >= numbers.n - 1;
-- movie director table 
INSERT INTO movie_db.movie_writer
WITH temp_movies AS (
  SELECT 
    movie_db.rotten.movieId as movieId,
    TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(rotten.writer, ',', numbers.n), ',', -1), '\r\n', ''), '\n', ''), '\r', '')) writer
  FROM
    (select 1 n UNION ALL
    select 2 UNION ALL 
    select 3 UNION ALL
    select 4 UNION ALL 
    select 5) numbers 
    INNER JOIN movie_db.rotten
    ON CHAR_LENGTH(rotten.writer) - CHAR_LENGTH(REPLACE(rotten.writer, ',', '')) >= numbers.n - 1
)
SELECT temp_movies.movieId, writers.id
FROM temp_movies
JOIN movie_db.writers ON writers.name = temp_movies.writer;

ALTER TABLE movie_db.rotten
DROP writer;


-- normalising the cast column 
CREATE TABLE movie_db.casts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE movie_db.movie_cast (
  movie_id INT NOT NULL,
  cast_id INT NOT NULL
);
ALTER TABLE movie_db.rotten ADD INDEX idx_cast (cast1);
ALTER TABLE movie_db.casts ADD INDEX idx_name (name);


-- cast table 
INSERT INTO movie_db.casts (name)
SELECT DISTINCT
  TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(m.cast1, ',', numbers.n), ',', -1), '\r\n', ''), '\n', ''), '\r', '')) AS cast1
FROM
  (select 1 n UNION ALL
  select 2 UNION ALL 
  select 3 UNION ALL
  select 4 UNION ALL 
  select 5) numbers 
  INNER JOIN movie_db.rotten m
  ON CHAR_LENGTH(m.cast1) - CHAR_LENGTH(REPLACE(m.cast1, ',', '')) >= numbers.n - 1;
-- movie director table 
INSERT INTO movie_db.movie_cast
WITH temp_movies AS (
  SELECT 
    movie_db.rotten.movieId as movieId,
    TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(rotten.cast1, ',', numbers.n), ',', -1), '\r\n', ''), '\n', ''), '\r', '')) cast1
  FROM
    (select 1 n UNION ALL
    select 2 UNION ALL 
    select 3 UNION ALL
    select 4 UNION ALL 
    select 5) numbers 
    INNER JOIN movie_db.rotten
    ON CHAR_LENGTH(rotten.cast1) - CHAR_LENGTH(REPLACE(rotten.cast1, ',', '')) >= numbers.n - 1
)
SELECT temp_movies.movieId, casts.id
FROM temp_movies
JOIN movie_db.casts ON casts.name = temp_movies.cast1;

ALTER TABLE movie_db.rotten
DROP cast1;