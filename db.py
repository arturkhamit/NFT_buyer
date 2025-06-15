import asyncpg
from config import DB_USER, DB_PASSWORD


async def connect_db():
    return await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database="users_stars",
        host="localhost",
        port=5432
    )

async def add_user(pool, user_id: int) -> None:
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO users (user_id, stars)
            VALUES ($1, 0)
            ON CONFLICT (user_id) DO NOTHING;
        ''', user_id)

async def add_stars(pool, user_id: int, count: int) -> None:
    async with pool.acquire() as conn:
        await conn.execute('''
            UPDATE users
            SET stars = stars + $1
            WHERE user_id = $2;
        ''', count, user_id)

async def get_stars(pool, user_id: int) -> int:
    async with pool.acquire() as conn:
        result = await conn.fetchval('''
            SELECT stars FROM users WHERE user_id = $1;
        ''', user_id)
        return result
