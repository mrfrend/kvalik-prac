from typing import Any
from PyQt6.QtCore import QDate
import pymysql
from pymysql.cursors import DictCursor

class Database:
    def __init__(self) -> None:
        self.conn = pymysql.connect(host="localhost", user="root", password="", database="hotel", cursorclass=DictCursor)
    
    def cursor(self) -> DictCursor:
        return self.conn.cursor()
    
    def commit(self):
        self.conn.commit()

    def get_all(self, table_name: str):
        with self.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name}")
            return cur.fetchall()
    
    def get_by_id(self, table_name: str, row_id: int):
        with self.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name} WHERE id = %s", (row_id,))
            return cur.fetchone()
    
    def update_client(self, client_id: int, first_name: str, last_name: str, middle_name: str, passport_series: int, passport_number: int, phone_number: str | None, preferences: str | None):
        with self.cursor() as cur:
            query = "UPDATE guests SET first_name = %s, last_name = %s, middle_name = %s, passport_series = %s, passport_number = %s, phone = %s, preferences = %s WHERE id = %s"
            cur.execute(query, (first_name, last_name, middle_name, passport_series, passport_number, phone_number, preferences, client_id))
            self.commit()
    
    def delete(self, table_name, row_id: int):
         with self.cursor() as cur:
            query = f"DELETE FROM {table_name} WHERE id = %s"
            cur.execute(query, (row_id,))
            self.commit()
    
    def insert_client(self, last_name: str, first_name: str, middle_name: str | None, passport_series: int, passport_number: int, phone_number: str | None, preferences: str | None):
        with self.cursor() as cur:
            query = "INSERT INTO guests(last_name, first_name, middle_name, passport_series, passport_number, phone, preferences) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (last_name, first_name, middle_name, passport_series, passport_number, phone_number, preferences))
            self.commit()

    
    # def insert(self, table_name: str, **cols: dict[str, Any]):
    #     placeholder = ', '.join(["%s"] * len(cols.keys()))
    #     col_names = ", ".join(cols.keys())
    #     query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholder})"
    #     with self.cursor() as cur:
    #         cur.execute(f"SELECT * FROM {table_name}")
    #         return cur.fetchall()
    
    def insert_booking(self, client_id: int, room_id: int, start_date: str, end_date: str):
        with self.cursor() as cur:
            cur.execute("INSERT INTO bookings(guest_id, room_id, start_date, end_date, booking_status_id) VALUES (%s, %s, %s, %s, 2)", (client_id, room_id, start_date, end_date))
            self.commit()
    
    def update_booking(self, booking_id: int, client_id: int, room_id: int, start_date: str, end_date: str):
         with self.cursor() as cur:
            query = """
                UPDATE bookings
                SET guest_id = %s,
                room_id = %s,
                start_date = %s,
                end_date = %s
                WHERE id = %s
            """
            cur.execute(query, (client_id, room_id, start_date, end_date, booking_id))
            self.commit()


    def auth(self, email: str, password: str):
        with self.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            result = cur.fetchone()
            return result
    
    def get_reservations_info(self):
        with self.cursor() as cur:
            query = """
                SELECT bookings.id, CONCAT_WS(" ", last_name, first_name, middle_name) as fio, room_number, room_types.name as room_type,
                start_date, end_date, booking_statuses.status_name, total_price
                FROM bookings
                JOIN guests ON guest_id = guests.id
                JOIN rooms ON room_id = rooms.id
                JOIN booking_statuses ON booking_statuses.id = booking_status_id
                JOIN room_types ON room_type_id = room_types.id
            """
            cur.execute(query)
            result = cur.fetchall()
            return result
    
    def get_reservations_info_filtered(self, start: QDate, end: QDate):
        start_string = start.toString("yyyy-MM-dd")
        end_string = end.toString("yyyy-MM-dd")
        with self.cursor() as cur:
            query = """
                SELECT bookings.id, CONCAT_WS(" ", last_name, first_name, middle_name) as fio, room_number, room_types.name as room_type,
                start_date, end_date, booking_statuses.status_name, total_price
                FROM bookings
                JOIN guests ON guest_id = guests.id
                JOIN rooms ON room_id = rooms.id
                JOIN booking_statuses ON booking_statuses.id = booking_status_id
                JOIN room_types ON room_type_id = room_types.id
                WHERE start_date >= %s AND start_date <= %s
            """
            cur.execute(query, (start_string, end_string))
            result = cur.fetchall()
            return result

        
        


db = Database()