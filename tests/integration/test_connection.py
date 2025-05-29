import asyncio
import asyncpg
from app.core.config import settings
from app.core.database import test_db_connection, AsyncSessionLocal
from sqlalchemy import text

async def test_direct_connection():
    """Test direct asyncpg connection"""
    try:
        # Parse the DATABASE_URL
        url = settings.DATABASE_URL
        print(f"Testing connection to: {url[:50]}...")
        
        # Test direct asyncpg connection
        conn = await asyncpg.connect(url)
        result = await conn.fetchval("SELECT 1")
        print(f"Direct asyncpg connection: SUCCESS (result: {result})")
        await conn.close()
        
    except Exception as e:
        print(f"Direct asyncpg connection: FAILED - {e}")

async def test_sqlalchemy_connection():
    """Test SQLAlchemy async connection"""
    try:
        success = await test_db_connection()
        if success:
            print("SQLAlchemy connection: SUCCESS")
        else:
            print("SQLAlchemy connection: FAILED")
    except Exception as e:
        print(f"SQLAlchemy connection: FAILED - {e}")

async def test_session():
    """Test session creation and query"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT current_database(), current_user"))
            row = result.fetchone()
            print(f"Session test: SUCCESS - Database: {row[0]}, User: {row[1]}")
    except Exception as e:
        print(f"Session test: FAILED - {e}")

async def main():
    print("=== Testing Database Connections ===")
    print(f"Database URL: {settings.DATABASE_URL[:50]}...")
    print()
    
    await test_direct_connection()
    await test_sqlalchemy_connection()
    await test_session()

if __name__ == "__main__":
    asyncio.run(main()) 