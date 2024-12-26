CREATE TABLE users (
  user_id INT PRIMARY KEY,
  username VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  registration_date DATE,
  pfp_path VARCHAR(255),
  address TEXT
);

CREATE TABLE persons (
  person_id INT PRIMARY KEY,
  name VARCHAR(255),
  birth_date DATE
);

CREATE TABLE production_companies (
  company_id INT PRIMARY KEY,
  name VARCHAR(255),
  establishment_year INT,
  contact_info TEXT
);

CREATE TABLE storage_locations (
  location_id INT PRIMARY KEY,
  server_name VARCHAR(255),
  file_path VARCHAR(255)
);

CREATE TABLE subscriptions (
  subscription_id INT PRIMARY KEY,
  user_id INT,
  tier_name VARCHAR(255),
  start_date DATE,
  end_date DATE,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE payments (
  payment_id INT PRIMARY KEY,
  subscription_id INT,
  amount DECIMAL(10, 2),
  payment_date DATE,
  transaction_status VARCHAR(255),
  FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);

CREATE TABLE media (
  media_id INT PRIMARY KEY,
  title VARCHAR(255),
  genre VARCHAR(255),
  production_year INT,
  average_rating FLOAT,
  director_id INT,
  production_company_id INT,
  location_id INT,
  FOREIGN KEY (director_id) REFERENCES persons(person_id),
  FOREIGN KEY (production_company_id) REFERENCES production_companies(company_id),
  FOREIGN KEY (location_id) REFERENCES storage_locations(location_id)
);

CREATE TABLE movies (
  media_id INT PRIMARY KEY,
  duration INT,
  FOREIGN KEY (media_id) REFERENCES media(media_id)
);

CREATE TABLE series (
  media_id INT PRIMARY KEY,
  total_seasons INT,
  FOREIGN KEY (media_id) REFERENCES media(media_id)
);

CREATE TABLE series_storage (
    series_id INT PRIMARY KEY,
    storage_server VARCHAR(255),
    storage_path VARCHAR(255),
    FOREIGN KEY (series_id) REFERENCES series(media_id)
);

CREATE TABLE episodes (
    episode_id INT PRIMARY KEY,
    series_id INT,
    season_number INT,
    episode_number INT,
    title VARCHAR(255),
    duration INT,
    FOREIGN KEY (series_id) REFERENCES series(media_id)
);

CREATE TABLE comments (
  comment_id INT PRIMARY KEY,
  user_id INT,
  media_id INT,
  comment_text TEXT,
  comment_date DATE,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (media_id) REFERENCES media(media_id)
);

CREATE TABLE ratings (
  rating_id INT PRIMARY KEY,
  user_id INT,
  media_id INT,
  rating_value FLOAT,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (media_id) REFERENCES media(media_id)
);

CREATE TABLE watch_later_lists (
  list_id INT PRIMARY KEY,
  user_id INT,
  media_id INT,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (media_id) REFERENCES media(media_id)
);