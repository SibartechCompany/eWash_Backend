import asyncio
from app.core.database import AsyncSessionLocal
from sqlalchemy import text

async def check_orders_table():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'orders' ORDER BY ordinal_position"))
        columns = result.fetchall()
        print('Columnas en la tabla orders:')
        for col in columns:
            print(f'  - {col[0]}')

if __name__ == "__main__":
    asyncio.run(check_orders_table()) 