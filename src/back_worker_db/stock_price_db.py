from typing import List
from src.data.models import Price
import psycopg2
from src.back_worker_db.database import get_db_connection

class StockPriceDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )  

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

