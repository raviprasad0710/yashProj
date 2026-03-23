import json
import time
import pymysql
import streamlit as st
from datetime import date
import bcrypt

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='crud',
        port=3306
    )

def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL, 
            role VARCHAR(50) DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def signup_user(username, email, password, role='user'):
    # Hash happens HERE — password comes in as plain text
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_pw, role)
        )
        conn.commit()
        return True
    except pymysql.IntegrityError:
        return False
    finally:
        conn.close()

def login_user_db(username_or_email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, password, role FROM users WHERE username=%s OR email=%s",
        (username_or_email, username_or_email)
    )
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        return {'id': user[0], 'username': user[1], 'email': user[2], 'role': user[4]}
    return None

def update_users_db(user_id, newusername, newemail):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s",
                   (newusername, newemail, user_id))
    conn.commit()
    conn.close()

def get_booked():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booked_seats")
    booked = cursor.fetchall()
    cursor.close()
    conn.close()
    return booked

def get_booked_seats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT seat_id, dates FROM booked_seats")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    today = date.today()
    booked_today = []
    for seat_id, dates_json in rows:
        dates_list = json.loads(dates_json) if isinstance(dates_json, str) else (dates_json or [])
        if today in [date.fromisoformat(d) for d in dates_list]:
            booked_today.append(seat_id)
    return booked_today

def get_booked_dates(seat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dates FROM booked_seats WHERE seat_id = %s", (seat_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    booked_dates = []
    for row in rows:
        dates_list = json.loads(row[0]) if isinstance(row[0], str) else (row[0] or [])
        for d in dates_list:
            booked_dates.append(date.fromisoformat(d))
    return booked_dates

def book_seat_db(user_id, username, seat_id, selected_dates):
    if isinstance(selected_dates, list):
        json_dates = json.dumps([d.strftime('%Y-%m-%d') for d in selected_dates])
    else:
        json_dates = json.dumps(selected_dates.strftime('%Y-%m-%d'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO booked_seats (user_id, user_name, seat_id, dates) VALUES (%s,%s,%s,%s)",
                       (user_id, username, seat_id, json_dates))
        conn.commit()
        return True, None
    except pymysql.Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def remove_booked_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM booked_seats WHERE user_id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def deleted_booking_overdue():
    today = date.today()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, dates FROM booked_seats")
    rows = cursor.fetchall()
    for row_id, dates_json in rows:
        try:
            dates_list = json.loads(dates_json) if isinstance(dates_json, str) else (dates_json or [])
            future_dates = [d for d in dates_list if date.fromisoformat(d) >= today]
            if len(future_dates) == 0:
                cursor.execute("DELETE FROM booked_seats WHERE user_id = %s", (row_id,))
            elif len(future_dates) < len(dates_list):
                cursor.execute("UPDATE booked_seats SET dates = %s WHERE user_id = %s",
                               (json.dumps(future_dates), row_id))
        except Exception as e:
            print(f"Error processing row {row_id}: {e}")
            continue
    conn.commit()
    cursor.close()
    conn.close()

def create_seat_positions_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seat_positions (
            seat_id VARCHAR(20) PRIMARY KEY,
            x_coord FLOAT NOT NULL,
            y_coord FLOAT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_seat_position(seat_id, x, y):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO seat_positions (seat_id, x_coord, y_coord)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE x_coord=%s, y_coord=%s
    """, (seat_id, x, y, x, y))
    conn.commit()
    conn.close()

def get_seat_positions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT seat_id, x_coord, y_coord FROM seat_positions ORDER BY seat_id")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_seat_position(seat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM seat_positions WHERE seat_id = %s", (seat_id,))
    conn.commit()
    conn.close()