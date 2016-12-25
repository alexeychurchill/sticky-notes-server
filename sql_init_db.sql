CREATE DATABASE sticky_notes_db;

USE sticky_notes_db;

CREATE TABLE user (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	login VARCHAR(25) NOT NULL,
	password VARCHAR(50) NOT NULL,
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

CREATE TABLE friend (
	id INTEGER AUTO_INCREMENT NOT NULL,
	user_a_id INTEGER NOT NULL PRIMARY KEY,
	user_b_id INTEGER NOT NULL PRIMARY KEY,
	FOREIGN KEY (user_a_id) REFERENCES user(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	FOREIGN KEY (user_b_id) REFERENCES user(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	PRIMARY KEY (id, user_a_id, user_b_id)
);

CREATE TABLE friend_request (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	status INTEGER NOT NULL DEFAULT 0,
	requester_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	FOREIGN KEY (requester_id) REFERENCES user(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES user(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE note_entry (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(50) NOT NULL,
	subject VARCHAR(20) NULL,
	creation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	change_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	owner_id INTEGER NOT NULL,
	FOREIGN KEY (owner_id) REFERENCES user(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE note_text (
	note_id INTEGER NOT NULL,
	text TEXT NOT NULL,
	FOREIGN KEY (note_id) REFERENCES note_entry(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	PRIMARY KEY (note_id)
);

CREATE TABLE shared_note (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	note_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	edit_permission BOOLEAN NOT NULL,
	FOREIGN KEY (note_id) REFERENCES note_entry(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES user(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE comment (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	text VARCHAR(250) NOT NULL,
	note_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (note_id) REFERENCES note_entry(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES user(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE VIEW note(id, title, subject, text, creation_date, change_date, owner_id)
	AS SELECT
		note_entry.id,
		note_entry.title,
		note_entry.subject,
		note_text.text,
		note_entry.creation_date,
		note_entry.change_date,
		note_entry.owner_id
	FROM 
		note_entry,
		note_text
	WHERE note_entry.id=note_text.note_id;

