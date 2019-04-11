
-- DROP DATABASE IF EXISTS music;
-- create DATABASE music CHARACTER set utf8mb4 collate utf8mb4_unicode_ci;


use music;

set FOREIGN_KEY_CHECKS = 0;


DROP  TABLE IF EXISTS artists;
CREATE TABLE  artists
(
    id VARCHAR(23) PRIMARY KEY,
    name VARCHAR(60),
    followers INTEGER,
    popularity TINYINT
);

DROP TABLE IF EXISTS albums;
CREATE TABLE albums(
    id VARCHAR(23) PRIMARY KEY,
    name VARCHAR(100) ,
    img VARCHAR(80) ,
    type VARCHAR(15),
    total_tracks INTEGER,
    artist_id VARCHAR(23),
    CONSTRAINT album_artist_fk
    FOREIGN KEY (artist_id) REFERENCES artist(id)
);


DROP TABLE IF EXISTS songs;
CREATE TABLE songs(
    id VARCHAR(23) PRIMARY KEY,
    name VARCHAR(250) ,
    popularity TINYINT,
    track_number TINYINT,
    tag_id INTEGER,
    artist_id VARCHAR(23),
    album_id VARCHAR(23),
    genre VARCHAR(20),
    CONSTRAINT song_artist_fk
    FOREIGN KEY (artist_id) REFERENCES artist(id),
    CONSTRAINT song_album_fk 
    FOREIGN KEY (album_id) REFERENCES album(id)
);


DROP table IF EXISTS tags;
CREATE TABLE tags(
    id integer PRIMARY KEY AUTO_INCREMENT,
    description VARCHAR(70)
);

DROP TABLE IF EXISTS features;
CREATE TABLE features(
    id VARCHAR(23) PRIMARY KEY,
    duration DOUBLE(6,4),
    danceability DOUBLE(6,4),
    energy DOUBLE(6,4),
    instrumentalness DOUBLE(6,4),
    liveness DOUBLE(6,4),
    loudness DOUBLE(6,4),
    valence DOUBLE(6,4),
    song_id DOUBLE(6,4),
    tempo DOUBLE(6,4),
    CONSTRAINT feature_song
    FOREIGN KEY (song_id) REFERENCES song(id)
);