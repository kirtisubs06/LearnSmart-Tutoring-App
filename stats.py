import os
import tempfile
from google.cloud.sql.connector import Connector


class Stats:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
            temp_file_path = temp_file.name

        # Use the temporary file path as the value for GOOGLE_APPLICATION_CREDENTIALS
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

        instance_connection_name = os.environ[
            "MYSQL_CONNECTION_STRING"
        ]  # e.g. 'project:region:instance'
        db_user = os.environ["SQL_USERNAME"]  # e.g. 'my-db-user'
        db_pass = os.environ["SQL_PASSWORD"]  # e.g. 'my-db-password'
        db_name = os.environ["SQL_DATABASE"]  # e.g. 'my-database'

        return Connector().connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
