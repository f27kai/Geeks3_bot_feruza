import sqlite3

import aiosqlite
from database import sql_queries


class AsyncDataBase:

    def __init__(self, db_path="db.sqlite3"):
        self.db_path = db_path

    async def create_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_queries.CREATE_USER_TABLE)
            await db.execute(sql_queries.CREATE_PROFILE_TABLE)
            await db.execute(sql_queries.CREATE_LIKE_DISLIKE_TABLE)
            await db.execute(sql_queries.CREATE_REVERENCE_TABLE)
            await db.execute(sql_queries.CREATE_DONATE_TRANSACTIONS_TABLE)
            await db.execute(sql_queries.CREATE_SEND_MONEY_TRANSACTIONS_TABLE)

            try:
                await db.execute(sql_queries.ALTER_USER_TABLE_V1)
                await db.execute(sql_queries.ALTER_USER_TABLE_V2)
            except sqlite3.OperationalError:
                pass

            await db.commit()
            print("База данных успешно создана")

    async def execute_query(self, query, params=None, fetch="None"):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, params or ())

            if fetch == "None":
                await db.commit()
                return

            elif fetch == "All":
                rows = await cursor.fetchall()
                return [dict(rows) for rows in rows] if rows else []

            elif fetch == "One":
                row = await cursor.fetchone()
                return dict(row) if row else None



