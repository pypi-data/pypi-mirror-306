import psycopg2
from torch.utils.data import IterableDataset


class PostgresDataset(IterableDataset):
    def __init__(
        self,
        db: str,
        user: str,
        password: str,
        host: str,
        port: int,
        query: str,
        fetch_size: int = 10000,
    ):
        self.conn_params = {
            "dbname": db,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        self.query = query
        self.fetch_size = fetch_size

    def __iter__(self):
        connection = psycopg2.connect(**self.conn_params)
        cursor = connection.cursor(name="server_side_cursor")
        cursor.execute(self.query)

        while True:
            rows = cursor.fetchmany(self.fetch_size)
            if not rows:
                break

            for row in rows:
                yield row

        cursor.close()
        connection.close()
