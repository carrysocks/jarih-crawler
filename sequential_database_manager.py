import psycopg2

class DatabaseManager:
    def __init__(self, dsn):
        self.dsn = dsn

    def save_data(self, buses):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cursor:
                
                sql = """
                    INSERT INTO bus_data (
                        time, plate_no, plate_type, route_id, route_name, 
                        remain_seat_cnt, station_id, station_name, station_seq
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                
                for bus in buses:
                    cursor.execute("""
                        INSERT INTO bus_data (
                            time, plate_no, plate_type, route_id, route_name, 
                            remain_seat_cnt, station_id, station_name, station_seq
                        ) VALUES (%(time)s, %(plate_no)s, %(plate_type)s, %(route_id)s, 
                                  %(route_name)s, %(remain_seat_cnt)s, %(station_id)s, 
                                  %(station_name)s, %(station_seq)s)
                    """, bus)