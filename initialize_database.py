import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_data (
            time TIMESTAMPTZ NOT NULL,
            plate_no TEXT,
            plate_type INTEGER,
            route_id TEXT,
            route_name TEXT,
            remain_seat_cnt INTEGER,
            station_id TEXT,
            station_name TEXT,
            station_seq INTEGER
        );
    """)

def create_hypertable(cursor):
    cursor.execute("SELECT create_hypertable('bus_data', 'time');")

def insert_test(cursor, conn):
    buses = [
        ("2024-03-22 00:14:48","경기73아1737",3,"219000013","1000",43,"219000340","양우아파트",1),
        ("2024-03-22 00:14:49","경기73아1737",3,"219000013","1000",42,"219000341","양우아파트",2),
        ("2024-03-22 00:15:48","경기73아1737",3,"219000013","1000",39,"219000342","양우아파트",3),
        ("2024-03-22 00:15:49","경기73아1737",3,"219000013","1000",38,"219000345","양우아파트",4),
        ("2024-03-22 00:16:48","경기73아1737",3,"219000013","1000",12,"219000349","양우아파트",5),
        ("2024-03-22 00:16:48","경기73아1737",3,"219000013","1000",1,"219000400","양우아파트",6),
        ("2024-03-22 00:18:48","경기73아1737",3,"219000013","1000",0,"219000401","양우아파트",12),
        ("2024-03-22 00:19:48","경기73아1737",3,"219000013","1000",25,"219000403","양우아파트",23),
    ]

    for bus in buses:
        try:
            cursor.execute(
                "INSERT INTO bus_data (time, plate_no, plate_type, route_id, route_name, remain_seat_cnt, station_id, station_name, station_seq) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (bus[0], bus[1], bus[2], bus[3], bus[4], bus[5], bus[6], bus[7], bus[8])
            )
        except (Exception, psycopg2.Error) as error:
            print(error.pgerror)
    conn.commit()
    cursor.close()

def main():
    load_dotenv()
    dsn = os.getenv("DB_URL")
    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    with conn.cursor() as cursor:
        create_tables(cursor)
        create_hypertable(cursor)
        insert_test(cursor, conn)
        
    conn.close()
    print("Hyper Table initialized successfully.")

if __name__ == "__main__":
    main()
