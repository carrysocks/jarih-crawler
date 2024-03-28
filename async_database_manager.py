import asyncpg


class AsyncDatabaseManager:
    def __init__(self, dsn):
        self.dsn = dsn
        self.conn = None 
    
    async def connect(self):
        if self.conn is None or self.conn.is_closed():
            self.conn = await asyncpg.connect(self.dsn)

    async def close(self):
        await self.conn.close()
        
    async def save_data(self, buses):
        await self.connect()
        async with self.conn.transaction():
            await self.conn.executemany("""
                INSERT INTO bus_data (time, plate_no, plate_type, route_id, route_name, 
                remain_seat_cnt, station_id, station_name, station_seq)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """, [(bus['time'], bus['plate_no'], bus['plate_type'], bus['route_id'], 
                        bus['route_name'], bus['remain_seat_cnt'], bus['station_id'], 
                        bus['station_name'], bus['station_seq']) for bus in buses])
