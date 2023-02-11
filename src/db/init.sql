CREATE TABLE movie_db.movies (
    movieId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    yearr INT NOT NULL,
    PRIMARY KEY (movieId)
);
LOAD DATA INFILE 'ml-latest-small/movies.csv' 
INTO TABLE movies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE movie_db.links (
    movieId INT NOT NULL AUTO_INCREMENT,
    imdbId INT NOT NULL,
    tmdbId INT NOT NULL,
    PRIMARY KEY (movieId)
);
LOAD DATA INFILE 'ml-latest-small/links.csv' 
INTO TABLE links 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE movie_db.ratings (
    userId INT NOT NULL,
    movieId INT NOT NULL,
    rating FLOAT NOT NULL,
    timestampp INT NOT NULL,
    PRIMARY KEY (userID, movieId)
);
LOAD DATA INFILE 'ml-latest-small/ratings.csv' 
INTO TABLE ratings 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE movie_db.tags (
    userId INT NOT NULL,
    movieId INT NOT NULL,
    tag VARCHAR(255) NOT NULL,
    timestampp INT NOT NULL,
    PRIMARY KEY (userID, movieId)
);
LOAD DATA INFILE 'ml-latest-small/tags.csv' 
INTO TABLE tags
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;