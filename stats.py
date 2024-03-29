import os
import tempfile
from google.cloud.sql.connector import Connector

from skill import EnglishSkill, MathSkill


class Stats:
    def __init__(self):
        self.connection = None

    def connect(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
            temp_file_path = temp_file.name

        # Use the temporary file path as the value for GOOGLE_APPLICATION_CREDENTIALS
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

        instance_connection_name = os.environ[
            "MYSQL_CONNECTION_STRING"
        ]
        db_user = os.environ["SQL_USERNAME"]
        db_pass = os.environ["SQL_PASSWORD"]
        db_name = os.environ["SQL_DATABASE"]

        self.connection = Connector().connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )

    def increment_session_counter(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE session_counter
            SET count = count + 1
            """
        )
        self.connection.commit()
        cursor.close()

    def increment_stats_counters(self, skill, level):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE stats
            SET count = count + 1
            WHERE skill = %s AND level = %s
            """,
            (skill.value, level.value)
        )
        self.connection.commit()
        cursor.close()

    def get_counters(self):
        cursor = self.connection.cursor()
        skills = [skill.value for skill in EnglishSkill] + [skill.value for skill in MathSkill]
        cursor.execute("SELECT skill, level, count FROM stats WHERE skill IN %s", (skills,))
        records = cursor.fetchall()
        cursor.close()
        counter_dict = {}
        for record in records:
            skill = record[0]
            level = record[1]
            count = record[2]
            counter_dict[(skill, level)] = count
        return counter_dict

    def get_session_counter(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT count FROM session_counter")
        session_count = cursor.fetchone()[0] or 0
        cursor.close()
        return session_count

    def get_total_counters(self):
        cursor = self.connection.cursor()
        skills = [skill.value for skill in EnglishSkill] + [skill.value for skill in MathSkill]
        cursor.execute("SELECT SUM(count) FROM stats WHERE skill IN %s", (skills,))
        total = cursor.fetchone()[0] or 0
        cursor.close()
        return total

    def add_review(self, score: int, comment: str):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO reviews (score, comment)
            VALUES (%s, %s)
            """,
            (score, comment)
        )
        self.connection.commit()
        cursor.close()

    def get_review_stats(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*), AVG(score) FROM reviews")
        result = cursor.fetchone()
        cursor.close()
        num_reviews = result[0]
        avg_rating = round(result[1], 1) if result[1] is not None else 0.0
        return num_reviews, avg_rating

    def get_top_reviews(self, limit=10):
        cursor = self.connection.cursor()
        cursor.execute("SELECT score, comment FROM reviews order by id DESC LIMIT %s", (limit,))
        top_reviews = cursor.fetchall()
        cursor.close()
        return top_reviews

    def store_api_key(self, vendor_name: str, api_key: str):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO api_keys (vendor_name, api_key)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE api_key = VALUES(api_key)
            """,
            (vendor_name, api_key)
        )
        self.connection.commit()
        cursor.close()

    def get_api_key(self, vendor_name: str):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT api_key FROM api_keys
            WHERE vendor_name = %s
            """,
            (vendor_name,)
        )
        api_key = cursor.fetchone()
        cursor.close()
        return api_key[0] if api_key else None

    def close(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection to MySQL database closed.")

