from faker import Faker
import psycopg2
from datetime import datetime, timedelta
import random
import hashlib
from typing import List, Dict


class StreamingDatabasePopulator:
    def __init__(self, connection_params: Dict):
        self.fake = Faker()
        self.conn = psycopg2.connect(**connection_params)
        self.cursor = self.conn.cursor()

        # Store IDs for relationships
        self.user_ids = []
        self.person_ids = []
        self.company_ids = []
        self.location_ids = []
        self.media_ids = []
        self.series_ids = []
        self.subscription_ids = []

        # Set to keep track of used emails
        self.used_emails = set()

    def clear_all_tables(self):
        """Clear all tables in the correct order to handle foreign key constraints"""
        print("Clearing existing data from tables...")
        tables = [
            'watch_later_lists', 'ratings', 'comments', 'episodes',
            'series_storage', 'movies', 'series', 'media', 'payments',
            'subscriptions', 'storage_locations', 'production_companies',
            'persons', 'users'
        ]
        for table in tables:
            print(f"Clearing table: {table}")
            self.cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
        self.conn.commit()
        print("All tables cleared successfully")

    def get_unique_email(self):
        """Generate a unique email address"""
        while True:
            email = self.fake.email()
            if email not in self.used_emails:
                self.used_emails.add(email)
                return email

    def populate_users(self, num_users: int):
        """Populate users table"""
        print(f"Populating {num_users} users...")
        for i in range(num_users):
            user_id = i + 1
            username = self.fake.user_name()
            email = self.get_unique_email()
            password = hashlib.sha256(self.fake.password().encode()).hexdigest()
            registration_date = self.fake.date_between(start_date='-3y')
            pfp_path = f'/avatars/user_{user_id}.jpg'
            address = self.fake.address()

            self.cursor.execute("""
                INSERT INTO users (user_id, username, email, password, registration_date, pfp_path, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, username, email, password, registration_date, pfp_path, address))

            self.user_ids.append(user_id)
            if i % 100 == 0:
                self.conn.commit()
        self.conn.commit()
        print("Users population completed")

    def populate_persons(self, num_persons: int):
        """Populate persons table (directors)"""
        print(f"Populating {num_persons} persons...")
        for i in range(num_persons):
            person_id = i + 1
            name = self.fake.name()
            birth_date = self.fake.date_between(start_date='-80y', end_date='-20y')

            self.cursor.execute("""
                INSERT INTO persons (person_id, name, birth_date)
                VALUES (%s, %s, %s)
            """, (person_id, name, birth_date))

            self.person_ids.append(person_id)
            if i % 100 == 0:
                self.conn.commit()
        self.conn.commit()
        print("Persons population completed")

    def populate_production_companies(self, num_companies: int):
        """Populate production_companies table"""
        print(f"Populating {num_companies} production companies...")
        for i in range(num_companies):
            company_id = i + 1
            name = f"{self.fake.company()} Productions"
            establishment_year = self.fake.random_int(min=1950, max=2024)
            contact_info = f"Email: {self.fake.company_email()}\nPhone: {self.fake.phone_number()}"

            self.cursor.execute("""
                INSERT INTO production_companies (company_id, name, establishment_year, contact_info)
                VALUES (%s, %s, %s, %s)
            """, (company_id, name, establishment_year, contact_info))

            self.company_ids.append(company_id)
        self.conn.commit()
        print("Production companies population completed")

    def populate_storage_locations(self, num_locations: int):
        """Populate storage_locations table"""
        print(f"Populating {num_locations} storage locations...")
        for i in range(num_locations):
            location_id = i + 1
            server_name = f"server-{self.fake.word()}-{random.randint(1, 99)}"
            file_path = f"/media/content/{self.fake.uuid4()}"

            self.cursor.execute("""
                INSERT INTO storage_locations (location_id, server_name, file_path)
                VALUES (%s, %s, %s)
            """, (location_id, server_name, file_path))

            self.location_ids.append(location_id)
        self.conn.commit()
        print("Storage locations population completed")

    def populate_subscriptions(self, num_subscriptions: int):
        """Populate subscriptions table"""
        print(f"Populating {num_subscriptions} subscriptions...")
        tier_names = ['Basic', 'Standard', 'Premium', 'Family']

        for i in range(num_subscriptions):
            subscription_id = i + 1
            user_id = random.choice(self.user_ids)
            tier_name = random.choice(tier_names)
            start_date = self.fake.date_between(start_date='-2y')
            end_date = start_date + timedelta(days=random.choice([30, 90, 180, 365]))

            self.cursor.execute("""
                INSERT INTO subscriptions (subscription_id, user_id, tier_name, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (subscription_id, user_id, tier_name, start_date, end_date))

            self.subscription_ids.append(subscription_id)
            if i % 100 == 0:
                self.conn.commit()
        self.conn.commit()
        print("Subscriptions population completed")

    def populate_payments(self, num_payments: int):
        """Populate payments table"""
        print(f"Populating {num_payments} payments...")
        statuses = ['Completed', 'Pending', 'Failed', 'Refunded']

        for i in range(num_payments):
            payment_id = i + 1
            subscription_id = random.choice(self.subscription_ids)
            amount = random.choice([9.99, 14.99, 19.99, 29.99])
            payment_date = self.fake.date_between(start_date='-1y')
            transaction_status = random.choice(statuses)

            self.cursor.execute("""
                INSERT INTO payments (payment_id, subscription_id, amount, payment_date, transaction_status)
                VALUES (%s, %s, %s, %s, %s)
            """, (payment_id, subscription_id, amount, payment_date, transaction_status))

            if i % 100 == 0:
                self.conn.commit()
        self.conn.commit()
        print("Payments population completed")

    def populate_media(self, num_media: int):
        """Populate media table"""
        print(f"Populating {num_media} media entries...")
        genres = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Romance', 'Documentary']

        for i in range(num_media):
            media_id = i + 1
            title = self.fake.catch_phrase()
            genre = random.choice(genres)
            production_year = random.randint(1990, 2024)
            average_rating = round(random.uniform(1.0, 10.0), 1)
            director_id = random.choice(self.person_ids)
            production_company_id = random.choice(self.company_ids)
            location_id = random.choice(self.location_ids)

            self.cursor.execute("""
                INSERT INTO media (media_id, title, genre, production_year, average_rating,
                                 director_id, production_company_id, location_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (media_id, title, genre, production_year, average_rating,
                  director_id, production_company_id, location_id))

            self.media_ids.append(media_id)
        self.conn.commit()
        print("Media population completed")

    def populate_movies_and_series(self):
        """Split media between movies and series"""
        print("Populating movies and series...")
        for media_id in self.media_ids:
            if random.random() < 0.7:  # 70% movies, 30% series
                duration = random.randint(80, 180)
                self.cursor.execute("""
                    INSERT INTO movies (media_id, duration)
                    VALUES (%s, %s)
                """, (media_id, duration))
            else:
                total_seasons = random.randint(1, 8)
                self.cursor.execute("""
                    INSERT INTO series (media_id, total_seasons)
                    VALUES (%s, %s)
                """, (media_id, total_seasons))
                self.series_ids.append(media_id)
        self.conn.commit()
        print("Movies and series population completed")

    def populate_series_storage(self):
        """Populate series_storage table"""
        print("Populating series storage...")
        for series_id in self.series_ids:
            storage_server = f"series-server-{self.fake.word()}"
            storage_path = f"/series/{series_id}/{self.fake.uuid4()}"

            self.cursor.execute("""
                INSERT INTO series_storage (series_id, storage_server, storage_path)
                VALUES (%s, %s, %s)
            """, (series_id, storage_server, storage_path))
        self.conn.commit()
        print("Series storage population completed")

    def populate_episodes(self):
        """Populate episodes table"""
        print("Populating episodes...")
        episode_id = 1
        for series_id in self.series_ids:
            self.cursor.execute("SELECT total_seasons FROM series WHERE media_id = %s", (series_id,))
            total_seasons = self.cursor.fetchone()[0]

            for season in range(1, total_seasons + 1):
                num_episodes = random.randint(8, 13)
                for ep_num in range(1, num_episodes + 1):
                    title = self.fake.catch_phrase()
                    duration = random.randint(20, 60)

                    self.cursor.execute("""
                        INSERT INTO episodes (episode_id, series_id, season_number, episode_number, title, duration)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (episode_id, series_id, season, ep_num, title, duration))

                    episode_id += 1
        self.conn.commit()
        print("Episodes population completed")

    def populate_comments(self, num_comments: int):
        """Populate comments table"""
        print(f"Populating {num_comments} comments...")
        for i in range(num_comments):
            comment_id = i + 1
            user_id = random.choice(self.user_ids)
            media_id = random.choice(self.media_ids)
            comment_text = self.fake.text(max_nb_chars=200)
            comment_date = self.fake.date_between(start_date='-1y')

            self.cursor.execute("""
                INSERT INTO comments (comment_id, user_id, media_id, comment_text, comment_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (comment_id, user_id, media_id, comment_text, comment_date))

            if i % 100 == 0:
                self.conn.commit()
        self.conn.commit()
        print("Comments population completed")

    def populate_ratings(self, num_ratings: int):
        """Populate ratings table"""
        print(f"Populating {num_ratings} ratings...")
        for i in range(num_ratings):
            rating_id = i + 1
            user_id = random.choice(self.user_ids)
            media_id = random.choice(self.media_ids)
            rating_value = round(random.uniform(1.0, 10.0), 1)

            self.cursor.execute("""
                INSERT INTO ratings (rating_id, user_id, media_id, rating_value)
                VALUES (%s, %s, %s, %s)
            """, (rating_id, user_id, media_id, rating_value))

            if i % 100 == 0:
                self.conn.commit()
        self.conn.commit()
        print("Ratings population completed")

    def populate_watch_later_lists(self, num_entries: int):
        """Populate watch_later_lists table"""
        print(f"Populating {num_entries} watch later entries...")
        for i in range(num_entries):
            list_id = i + 1
            user_id = random.choice(self.user_ids)
            media_id = random.choice(self.media_ids)

            self.cursor.execute("""
                INSERT INTO watch_later_lists (list_id, user_id, media_id)
                VALUES (%s, %s, %s)
            """, (list_id, user_id, media_id))

            if i % 100 == 0:
                self.conn.commit()
        self.conn.commit()
        print("Watch later lists population completed")

    def populate_all(self, num_records: Dict[str, int]):
        """Populate all tables with specified number of records"""
        try:
            print("Starting data population process...")
            self.clear_all_tables()

            self.populate_users(num_records['users'])
            self.populate_persons(num_records['persons'])
            self.populate_production_companies(num_records['companies'])
            self.populate_storage_locations(num_records['locations'])
            self.populate_subscriptions(num_records['subscriptions'])
            self.populate_payments(num_records['payments'])
            self.populate_media(num_records['media'])
            self.populate_movies_and_series()
            self.populate_series_storage()
            self.populate_episodes()
            self.populate_comments(num_records['comments'])
            self.populate_ratings(num_records['ratings'])
            self.populate_watch_later_lists(num_records['watch_later'])

            print("Data population completed successfully!")

        except Exception as e:
            self.conn.rollback()
            print(f"Error during population: {e}")
            raise e

    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    # Database connection parameters
    connection_params = {
        "dbname": "DB Project",  # Replace with your database name
        "user": "postgres",  # Replace with your username
        "password": "09356261060",  # Replace with your password
        "host": "localhost",
        "port": "5433"
    }

    # Number of records to generate for each table
    num_records = {
        'users': 1000,
        'persons': 200,
        'companies': 50,
        'locations': 100,
        'subscriptions': 1200,
        'payments': 5000,
        'media': 500,
        'comments': 3000,
        'ratings': 4000,
        'watch_later': 2000
    }

    print("Starting database population script...")
    print("Using the following configuration:")
    print(f"Number of users: {num_records['users']}")
    print(f"Number of persons: {num_records['persons']}")
    print(f"Number of media items: {num_records['media']}")

    try:
        # Create and run the populator
        populator = StreamingDatabasePopulator(connection_params)
        populator.populate_all(num_records)
    except psycopg2.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        try:
            populator.close()
        except:
            print("Error while closing database connection")
        print("Script execution completed.")