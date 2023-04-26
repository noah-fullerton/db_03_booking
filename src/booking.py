"""
CS3810: Principles of Database Systems
Instructor: Thyago Mota
Student(s): Muhammad Qamar
Description: A room reservation system
"""

import psycopg2
from psycopg2 import extensions, errors
import configparser as cp
from datetime import datetime

def menu(): 
    print('1. List')
    print('2. Reserve')
    print('3. Delete')
    print('4. Quit')

def db_connect():
    config = cp.RawConfigParser()
    config.read('ConfigFile.properties')
    params = dict(config.items('db'))
    conn = psycopg2.connect(**params)
    conn.autocommit = False 
    with conn.cursor() as cur: 
        cur.execute('''
            PREPARE QueryReservationExists AS 
                SELECT * FROM Reservations 
                WHERE abbr = $1 AND room = $2 AND date = $3 AND period = $4;
        ''')
        cur.execute('''
            PREPARE QueryReservationExistsByCode AS 
                SELECT * FROM Reservations 
                WHERE code = $1;
        ''')
        cur.execute('''
            PREPARE NewReservation AS 
                INSERT INTO Reservations (abbr, room, date, period) VALUES
                ($1, $2, $3, $4);
        ''')
        cur.execute('''
            PREPARE UpdateReservationUser AS 
                UPDATE Reservations SET "user" = $1
                WHERE abbr = $2 AND room = $3 AND date = $4 AND period = $5; 
        ''')
        cur.execute('''
            PREPARE DeleteReservation AS 
                DELETE FROM Reservations WHERE code = $1;
        ''')
    return conn

# TODO: display all reservations in the system using the information from ReservationsView
def list_op(conn):
    pass
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM ReservationsView;")
        rows = cur.fetchall()
        if not rows:
            print("No reservations found")
        else:
            print("Reservations:")
            for row in rows:
                print("Code: ", row[0])
                print("Date: ", row[1])
                print("Period: ", row[2])
                print("Start: ", row[3])
                print("End: ", row[4])
                print("Room: ", row[5])
                print("Name: ", row[6])
                print("--------------------")


# TODO: reserve a room on a specific date and period, also saving the user who's the reservation is for
def reserve_op(conn): 
    pass
    with conn.cursor() as cur: 
        abbr = input('Building abbreviation: ').strip().upper()
        room = int(input('Room number: ').strip())
        date = input('Date (YYYY-MM-DD): ').strip()
        period = input('Period (A-H): ').strip().upper()
        cur.execute('EXECUTE QueryReservationExists (%s, %s, %s, %s);', (abbr, room, date, period))
        if cur.fetchone():
            print('The room is already reserved for that period.')
            return
        user = input('User: ').strip()
        cur.execute('EXECUTE NewReservation (%s, %s, %s, %s);', (abbr, room, date, period))
        cur.execute('EXECUTE UpdateReservationUser (%s, %s, %s, %s, %s);', (user, abbr, room, date, period))
        conn.commit()
        print('Reservation created.')

# TODO: delete a reservation given its code
def delete_op(conn):
    pass
    with conn.cursor() as cur: 
        code = int(input('Reservation code: ').strip())
        cur.execute('EXECUTE QueryReservationExistsByCode (%s);', (code,))
        if not cur.fetchone():
            print('Reservation not found.')
            return
        cur.execute('DELETE FROM Reservations WHERE code = %s;', (code,))
        conn.commit()
        print('Reservation deleted.')

if __name__ == "__main__":
    with db_connect() as conn: 
        op = 0
        while op != 4: 
            menu()
            op = int(input('? '))
            if op == 1: 
                list_op(conn)
            elif op == 2:
                reserve_op(conn)
            elif op == 3:
                delete_op(conn)