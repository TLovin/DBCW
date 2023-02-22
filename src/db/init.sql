CREATE TABLE movie_db.movies (
    movieId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    -- yearr INT NOT NULL,
    PRIMARY KEY (movieId)
);

CREATE TABLE movie_db.links (
    movieId INT NOT NULL,
    imdbId INT NOT NULL,
    tmdbId INT NOT NULL,
    PRIMARY KEY (movieId)
);

CREATE TABLE movie_db.ratings (
    userId INT NOT NULL,
    movieId INT NOT NULL,
    rating FLOAT NOT NULL,
    `timestamp` INT NOT NULL,
    PRIMARY KEY (userID, movieId)
);

CREATE TABLE movie_db.tags (
    userId INT NOT NULL,
    movieId INT NOT NULL,
    tag VARCHAR(255) NOT NULL,
    `timestamp` INT NOT NULL,
    -- tagIndex INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (userId,movieId,tag,`timestamp`)
);


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