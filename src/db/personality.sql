-- Integrate personality tables into the database
ALTER TABLE movie_db.users
ADD openness FLOAT,
ADD agreeableness FLOAT,
ADD emotional_stability FLOAT,
ADD conscientiousness FLOAT,
ADD extraversion FLOAT,
ADD personality_userId VARCHAR(255),
ADD source VARCHAR(255);

UPDATE movie_db.users
SET source = 'MovieLens';

INSERT INTO movie_db.users (personality_userId, openness, agreeableness, emotional_stability, conscientiousness, extraversion, source)
SELECT *, 'Personality'
FROM movie_db.user_personalities;

INSERT INTO movie_db.ratings
SELECT u.userId, m.movieId, rating, UNIX_TIMESTAMP(`timestamp`) as `timestamp`
FROM movie_db.ratings_personality r
INNER JOIN movie_db.movies m  -- to honor the foreign key
ON r.movieId = m.movieId
LEFT JOIN movie_db.users u
ON r.userId = u.personality_userId;

ALTER TABLE movie_db.users
DROP personality_userId;

DROP TABLE movie_db.ratings_personality;
DROP TABLE movie_db.user_personalities;

CREATE TABLE movie_db.personality_movie_analysis AS
SELECT u.*, ROUND(AVG(r.rating), 2) as avg_rating, g.type
FROM movie_db.users u
JOIN movie_db.ratings r
ON u.userId = r.userId
JOIN movie_db.moviegenres mg
ON r.movieId = mg.movieId
JOIN movie_db.genres g
ON mg.genreId = g.genreId
WHERE u.source = 'Personality'
GROUP BY u.userId, u.openness, u.agreeableness, u.emotional_stability, u.conscientiousness, u.extraversion, g.type
ORDER BY `u`.`userId` ASC;