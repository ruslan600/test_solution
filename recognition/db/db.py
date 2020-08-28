import os

import psycopg2
import psycopg2.extras

from recognition.utils.error_log import error_logger


PG_URL = os.getenv('PG_URL')


class DB:
    """
    Класс для работы с бд.
    """
    def __init__(self, pg_url):
        self.pg_url = pg_url
        try:
            self.connection = psycopg2.connect(self.pg_url)
        except Exception as e:
            error_logger.exception(e)

    def add_to_db(self, date, time, id_, result, phone, duration, transcript):
        """
        Функция для добавления записи с результатами в бд.
        """
        try:
            with self.connection.cursor() as cur:
                psycopg2.extras.register_uuid()
                query = """
                INSERT INTO recognition_results (date, time, unique_id, rec_result, phone_number, duration, transcript)
                VALUES (%s, %s, %s, %s, %s, %s, %s);"""
                cur.execute(query, (date, time, id_, result, phone, duration, transcript))
                self.connection.commit()
            self.connection.close()
        except Exception as e:
            error_logger.exception(e)


db = DB(PG_URL)
