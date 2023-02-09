CREATE TABLE movies (
    movieId INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    yearr INT NOT NULL,
    PRIMARY KEY (movieId)
);

CREATE TABLE links (
    movieId INT NOT NULL AUTO_INCREMENT,
    imdbId INT NOT NULL,
    tmdbId INT NOT NULL,
    PRIMARY KEY (movieId)
);

CREATE TABLE ratings (
    userId INT NOT NULL,
    movieId INT NOT NULL,
    rating FLOAT NOT NULL,
    timestampp INT NOT NULL,
    PRIMARY KEY (userID, movieId)
);

CREATE TABLE tags (
    userId INT NOT NULL,
    movieId INT NOT NULL,
    tag VARCHAR(255) NOT NULL,
    timestampp INT NOT NULL,
    PRIMARY KEY (userID, movieId)
);