CREATE TABLE IF NOT EXISTS courses (
    course_id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL,
    authors TEXT,
    summary TEXT,
    rating FLOAT,
    learners INT,
    picture TEXT,
    link TEXT UNIQUE NOT NULL,
    category TEXT
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    sex VARCHAR(10),
    age INT,
    preference TEXT
);

CREATE TABLE IF NOT EXISTS interactions (
    interaction_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    course_id INT REFERENCES courses(course_id),
    click INT DEFAULT 1,
    click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


\COPY courses(name, authors, summary, rating, learners, picture, link, category) FROM 'Courses.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8')




INSERT INTO users (sex, age, preference)
VALUES ('М', 22, 'Математика');
