CREATE DATABASE movie_rental;

USE movie_rental;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);


CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);


CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    description TEXT,
    price DECIMAL(10,2)
);
select * from movies;
--  (user_id gets access to locked movies)
CREATE TABLE access (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);



select * from admins;
INSERT INTO movies (name, description, price) VALUES
('wrath_of_man', 'A mind-bending thriller by jason statham.', 4.99),
('avatar', 'Space exploration and time dilation.', 5.99),
('into the wild', ' jungle book continuation.', 3.99),
('breaking_bad', 'Classic carteldrama.', 4.49),
('deadpool', 'Classic action with wolvarine.', 8.49),
('dark knight', 'Batman battles the Joker in Gotham.', 4.79);

select * from access;
select * from users;



