CREATE TABLE movie_db.movies (
    movieId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    -- yearr INT NOT NULL,
    PRIMARY KEY (movieId)
);
CREATE TABLE movie_db.links (
    movieId INT NOT NULL AUTO_INCREMENT,
    imdbId INT NOT NULL,
    tmdbId INT NOT NULL,
    PRIMARY KEY (movieId)
);



-- LOAD DATA INFILE '../secure_file_priv/links.csv'
-- INTO TABLE links
-- FIELDS TERMINATED BY ','
-- IGNORE 1 ROWS;

-- LOAD DATA INFILE '../secure_file_priv/links.csv' 
-- INTO TABLE movies_db.links 
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

CREATE TABLE movie_db.ratings (
    userId INT NOT NULL,
    movieId INT NOT NULL,
    rating FLOAT NOT NULL,
    timestampp INT NOT NULL,
    PRIMARY KEY (userID, movieId)
);
-- LOAD DATA INFILE 'ml-latest-small/ratings.csv' 
-- INTO TABLE ratings 
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

CREATE TEMPORARY TABLE movie_db.tags (
    userId INT NOT NULL ,
    movieId INT NOT NULL,
    tag VARCHAR(255) NOT NULL,
    timestampp INT NOT NULL,
    tagIndex INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (tagIndex)
);
-- LOAD DATA INFILE 'ml-latest-small/tags.csv' 
-- INTO TABLE tags
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;


SHOW VARIABLES LIKE "secure_file_priv";

LOAD DATA INFILE '../../movies.csv' 
INTO TABLE movie_db.movies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '../../links.csv' 
INTO TABLE movie_db.links
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '../../ratings.csv'
INTO TABLE movie_db.ratings
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '../../tags.csv'
INTO TABLE movie_db.tags
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


CREATE TABLE movie_db.tagData (
  userId INT NOT NULL,
  movieId INT NOT NULL,
  tagIndex INT NOT NULL ,
  timestampp INT NOT NULL,
  PRIMARY KEY (userId,movieId,tagIndex)

);

CREATE TABLE movie_db.tagCollection (
  tagIndex INT NOT NULL AUTO_INCREMENT,
  tag VARCHAR(255) NOT NULL,
  PRIMARY KEY (tagIndex)
);

INSERT INTO movie_db.tagData (userId, movieId,timestampp,tagIndex)
SELECT userId, movieId,timestampp,tagIndex
FROM movie_db.tags;

INSERT INTO movie_db.tagCollection (tag,tagIndex)
SELECT tag,tagIndex
FROM movie_db.tags;