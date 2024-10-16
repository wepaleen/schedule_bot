import asyncpg
from typing import List, Tuple
# from connection import db_connection

async def create_pool():
    return await asyncpg.create_pool(
        user='admin',
        password='234dfgdf',
        database='tg_db_postgres',
        host='45.151.30.108'
    )


# Функция для инициализации таблиц (выполнить её один раз для создания таблиц)
async def init_db(pool):
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL UNIQUE,
                username VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                file_name VARCHAR(255) NOT NULL,
                file_path VARCHAR(255) NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

async def add_user(pool, telegram_id: int, username: str):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO users (telegram_id, username)
            VALUES ($1, $2)
            ON CONFLICT (telegram_id) DO NOTHING;
        ''', telegram_id, username)

async def get_user_id(pool, telegram_id: int) -> int:
    async with pool.acquire() as connection:
        user = await connection.fetchrow('''
            SELECT id FROM users WHERE telegram_id = $1;
        ''', telegram_id)
        return user['id'] if user else None

async def save_file_to_db(pool, user_id: int, file_name: str, file_path: str):
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO files (user_id, file_name, file_path)
            VALUES ($1, $2, $3);
        ''', user_id, file_name, file_path)

async def get_user_files(pool, user_id: int) -> List[Tuple[int, str, str]]:
    async with pool.acquire() as connection:
        files = await connection.fetch('''
            SELECT id, file_name, file_path
            FROM files
            WHERE user_id = $1;
        ''', user_id)
        return [(file['id'], file['file_name'], file['file_path']) for file in files]

async def delete_file_from_db(pool, file_id: int):
    async with pool.acquire() as connection:
        await connection.execute('''
            DELETE FROM files WHERE id = $1;
        ''', file_id)