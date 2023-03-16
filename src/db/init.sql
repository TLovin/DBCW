CREATE TABLE movie_db.movies (
    movieId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
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
    PRIMARY KEY (userId, movieId),
    FOREIGN KEY (movieId) REFERENCES movie_db.movies(movieId)
);

CREATE TABLE movie_db.tags (
    userId INT NOT NULL,
    movieId INT NOT NULL,
    tag VARCHAR(255) NOT NULL,
    `timestamp` INT NOT NULL,
    PRIMARY KEY (userId, movieId, tag, `timestamp`),
    FOREIGN KEY (movieId) REFERENCES movie_db.movies(movieId)
);

CREATE TABLE movie_db.user_personalities (
    userId VARCHAR(255) NOT NULL,
    openness FLOAT NOT NULL,
    agreeableness FLOAT NOT NULL,
    emotional_stability FLOAT NOT NULL,
    conscientiousness FLOAT NOT NULL,
    extraversion FLOAT NOT NULL,
    PRIMARY KEY (userId)
);

CREATE TABLE movie_db.ratings_personality (
    userId VARCHAR(255) NOT NULL,
    movieId INT NOT NULL,
    rating INT NOT NULL,
    `timestamp` TIMESTAMP NOT NULL,
    PRIMARY KEY (userId, movieId)
);

LOAD DATA INFILE '../../ml-latest-small/movies.csv' 
INTO TABLE movie_db.movies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '../../ml-latest-small/links.csv' 
INTO TABLE movie_db.links
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '../../ml-latest-small/ratings.csv'
INTO TABLE movie_db.ratings
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '../../ml-latest-small/tags.csv'
INTO TABLE movie_db.tags
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '../../personality-isf2018/personality-data.csv' IGNORE
INTO TABLE movie_db.user_personalities 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS (userid, openness, agreeableness, emotional_stability, conscientiousness, extraversion, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy);

LOAD DATA INFILE '../../personality-isf2018/ratings.csv' IGNORE
INTO TABLE movie_db.ratings_personality
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;