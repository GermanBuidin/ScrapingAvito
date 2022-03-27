import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from log import logger


class Database:

    CREATE = '''CREATE TABLE IF NOT EXISTS OLD_CARS 
            (ID INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            URL VARCHAR(255) UNIQUE NOT NULL,
            TITLE TEXT NOT NULL,
            USD_PRICE INT NOT NULL,
            MILEAGE VARCHAR(50) NOT NULL,
            USERNAME VARCHAR(50) NOT NULL,
            PHONE_NUMBER INT NOT NULL,
            IMG_URL VARCHAR(255) NOT NULL,
            IMG_TOTAL_COUNT INT2 NOT NULL,
            CAR_NUMBER VARCHAR(16),
            CAR_VIN_CODE VARCHAR(20),
            DATETIME_FOUND TIMESTAMP DEFAULT NOW() );'''

    INSERT = """INSERT INTO OLD_CARS (URL, TITLE, USD_PRICE, MILEAGE, USERNAME, PHONE_NUMBER,
             IMG_TOTAL_COUNT, CAR_NUMBER, CAR_VIN_CODE, IMG_URL ) 
             VALUES (%(url)s, %(title)s, %(usd_price)s, %(mileage)s, %(username)s, %(phone_number)s,
             %(img_total_count)s, %(car_number)s, %(car_vin_code)s, %(img_url)s)
             ON CONFLICT (URL) 
             DO NOTHING"""

    def __init__(self):
        self.connection = psycopg2.connect(database="postgres",
                                           user="postgres",
                                           password="Marianna+",
                                           host="127.0.0.1",
                                           port="5432")
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()
        logger.info("Database opened successfully")

    def create_table(self):
        self.cursor.execute(self.CREATE)

    def insert_car_info(self, car_info: list):
        try:
            psycopg2.extras.execute_batch(self.cursor, self.INSERT, car_info)
            logger.info("Record inserted successfully")
        except Exception as err:
            logger.exception(err)