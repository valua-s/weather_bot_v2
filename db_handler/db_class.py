"""Базовый файл для описания работы с базой данных."""
import asyncpg


class PostgresHandler:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    async def connect(self):
        self.connection = await asyncpg.connect(**self.db_config)

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def execute_query(self, query, *params):
        await self.connection.execute(query, *params)

    async def fetch_all(self, query, *params):
        return await self.connection.fetch(query, *params)

    async def fetch_one(self, query, *params):
        return await self.connection.fetchrow(query, *params)
