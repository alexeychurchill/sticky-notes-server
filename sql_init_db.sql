CREATE DATABASE sticky_notes_db;

USE sticky_notes_db;

CREATE TABLE user (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	login VARCHAR(25) NOT NULL,
	password VARCHAR(30) NOT NULL,
	name VARCHAR(50),
	last_name VARCHAR(50)
);

CREATE TABLE access_token (
	user_id INTEGER NOT NULL,
	access_token VARCHAR(75) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	PRIMARY KEY (user_id, access_token)
);