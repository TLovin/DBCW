-- Create tables
CREATE TABLE movie_db.moviegenres (
  movieId INT NOT NULL,
  genreId INT NOT NULL
);

CREATE TABLE movie_db.genres (
  genreId INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(255) NOT NULL,
  PRIMARY KEY (genreId)
);

CREATE TABLE movie_db.users (
  userId INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (userId)
);

ALTER TABLE movie_db.movies
ADD `year` INT;

UPDATE movies
SET `year` =
  CASE 
    WHEN REPLACE(SUBSTRING_INDEX(title, '(', -1), ')', '') REGEXP '^[0-9][0-9][0-9][0-9]$' THEN REPLACE(SUBSTRING_INDEX(title, '(', -1), ')', '')
      ELSE NULL
  END,
title = SUBSTRING_INDEX(title, '(', 1);

-- Populate tables
-- Users
INSERT INTO movie_db.users (userId)
SELECT userId
FROM movie_db.ratings
UNION 
SELECT userId
FROM movie_db.tags;

-- Genres
INSERT INTO movie_db.genres (`type`)
SELECT DISTINCT
  TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(m.genre, '|', numbers.n), '|', -1), '\r\n', ''), '\n', ''), '\r', '')) AS genre
FROM
  (select 1 n UNION ALL
  select 2 UNION ALL 
  select 3 UNION ALL
  select 4 UNION ALL 
  select 5) numbers 
  INNER JOIN movie_db.movies m
  ON CHAR_LENGTH(m.genre) - CHAR_LENGTH(REPLACE(m.genre, '|', '')) >= numbers.n - 1
ORDER BY 1;

-- Moviegenres
INSERT INTO movie_db.moviegenres
WITH temp_movies AS (
  SELECT
    movies.movieId as movieId,
    TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(movies.genre, '|', numbers.n), '|', -1), '\r\n', ''), '\n', ''), '\r', '')) genre
  FROM
    (select 1 n UNION ALL
    select 2 UNION ALL 
    select 3 UNION ALL
    select 4 UNION ALL 
    select 5) numbers 
    INNER JOIN movies
    ON CHAR_LENGTH(movies.genre) - CHAR_LENGTH(REPLACE(movies.genre, '|', '')) >= numbers.n - 1
)
SELECT t.movieId, g.genreID
FROM temp_movies t
JOIN movie_db.genres g
ON t.genre = g.`type`
ORDER BY 1, 2;

ALTER TABLE movie_db.movies
DROP genre;