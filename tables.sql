DROP TABLE users;
DROP TABLE places;
DROP TABLE meetups;
DROP TABLE signups;
DROP TABLE comments;
DROP TABLE notifications;

CREATE TYPE GENDER AS ENUM ('male', 'female', 'other');
CREATE TYPE ROLE as ENUM ('user', 'admin');

CREATE TABLE users (
   id SERIAL PRIMARY KEY,
   name TEXT NOT NULL,
   age INT NOT NULL,
   gender GENDER NOT NULL,
   role ROLE NOT NULL,
   password TEXT NOT NULL,
   created_at TIMESTAMP
);

CREATE TABLE places (
   id SERIAL PRIMARY KEY,
   name TEXT NOT NULL,
   location POINT NOT NULL,
   created_at TIMESTAMP
);

CREATE TABLE meetups (
   id SERIAL PRIMARY KEY,
   title TEXT NOT NULL,
   place_id INT REFERENCES places (id),
   host_id INT REFERENCES places (id),
   begins_at TIMESTAMP NOT NULL,
   max_people INT,
   description TEXT,
   created_at TIMESTAMP
);

CREATE TABLE signups (
   id SERIAL PRIMARY KEY,
   meetup_id INT REFERENCES meetups (id),
   user_id INT REFERENCES users (id),
   created_at TIMESTAMP
);

CREATE TABLE comments (
   id SERIAL PRIMARY KEY,
   meetup_id INT REFERENCES meetups (id),
   user_id INT REFERENCES users (id),
   comment TEXT NOT NULL,
   created_at TIMESTAMP
);

CREATE TABLE notifications (
   id serial PRIMARY KEY,
   user_id INT,
   message TEXT NOT NULL,
   created_at TIMESTAMP
);


INSERT INTO users (name, age, gender, role, password, created_at) VALUES ('Jorma', 25, 'male', 'admin', 'password123', NOW());