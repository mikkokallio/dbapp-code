DROP TABLE users CASCADE;
DROP TABLE places CASCADE;
DROP TABLE events CASCADE;
DROP TABLE signups CASCADE;
DROP TABLE comments CASCADE;
DROP TABLE notifications CASCADE;

DROP TYPE GENDER;
DROP TYPE ROLE;

CREATE TYPE GENDER AS ENUM ('male', 'female', 'other');
CREATE TYPE ROLE as ENUM ('user', 'admin', 'banned');

CREATE TABLE users (
   id SERIAL PRIMARY KEY,
   username TEXT UNIQUE,
   date_of_birth DATE,
   gender GENDER,
   description TEXT,
   role ROLE NOT NULL,
   password TEXT NOT NULL,
   created_at TIMESTAMP
);

CREATE TABLE places (
   id SERIAL PRIMARY KEY,
   name TEXT UNIQUE,
   location POINT NOT NULL,
   address TEXT NOT NULL,
   description TEXT,
   page_url TEXT,
   pic_url TEXT,
   created_at TIMESTAMP
);

CREATE TABLE events (
   id SERIAL PRIMARY KEY,
   title TEXT NOT NULL,
   place_id INT REFERENCES places (id),
   host_id INT REFERENCES users (id) ON DELETE CASCADE,
   date DATE NOT NULL,
   time TIME NOT NULL,
   max_people INT,
   hidden BOOLEAN,
   description TEXT,
   created_at TIMESTAMP
);

CREATE TABLE signups (
   id SERIAL PRIMARY KEY,
   event_id INT REFERENCES events (id) ON DELETE CASCADE,
   user_id INT REFERENCES users (id) ON DELETE CASCADE,
   created_at TIMESTAMP
);

CREATE TABLE comments (
   id SERIAL PRIMARY KEY,
   event_id INT REFERENCES events (id) ON DELETE CASCADE,
   user_id INT REFERENCES users (id) ON DELETE CASCADE,
   comment TEXT NOT NULL,
   created_at TIMESTAMP
);

CREATE TABLE notifications (
   id SERIAL PRIMARY KEY,
   user_id INT REFERENCES users (id),
   message TEXT NOT NULL,
   acknowledged BOOLEAN,
   created_at TIMESTAMP
);
