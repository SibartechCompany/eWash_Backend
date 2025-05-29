import asyncio
import asyncpg
from app.core.config import settings

async def reset_and_test_connection():
    """Reset any pending transactions and test connection"""
    try:
        print("🔄 Resetting database connection...")
        
        # Try different connection URLs
        urls_to_try = [
            # Session pooler (5432)
            settings.DATABASE_URL.replace(":6543/", ":5432/"),
            # Transaction pooler (6543) 
            settings.DATABASE_URL,
            # Direct connection
            settings.DATABASE_URL.replace("aws-0-us-east-2.pooler.supabase.com:6543", "db.ajqkrulblcfjvbfobiph.supabase.co:5432")
        ]
        
        for i, url in enumerate(urls_to_try, 1):
            try:
                print(f"Trying URL {i}: {url[:50]}...")
                
                # Connect with minimal settings to avoid prepared statements
                conn = await asyncpg.connect(
                    url,
                    statement_cache_size=0,
                    command_timeout=10
                )
                
                # Execute a simple query to test
                result = await conn.fetchval("SELECT 1")
                print(f"✅ Connection {i} successful (result: {result})")
                
                # Test a simple table query
                try:
                    tables = await conn.fetch("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        LIMIT 5
                    """)
                    print(f"✅ Found {len(tables)} tables in database")
                    for table in tables:
                        print(f"  - {table['table_name']}")
                except Exception as e:
                    print(f"⚠️ Could not list tables: {e}")
                
                await conn.close()
                print(f"✅ Connection {i} reset successful")
                return True, url
                
            except Exception as e:
                print(f"❌ Connection {i} failed: {e}")
                continue
        
        return False, None
        
    except Exception as e:
        print(f"❌ Connection reset failed: {e}")
        return False, None

async def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        from app.core.database import test_db_connection
        print("🔄 Testing SQLAlchemy connection...")
        success = await test_db_connection()
        return success
    except Exception as e:
        print(f"❌ SQLAlchemy test failed: {e}")
        return False

async def main():
    print("=== Database Connection Reset ===")
    
    # Test 1: Direct connection with multiple URLs
    direct_ok, working_url = await reset_and_test_connection()
    print()
    
    if working_url:
        print(f"✅ Working URL found: {working_url}")
        print("Update your .env file with this URL if different from current")
    
    # Test 2: SQLAlchemy connection
    if direct_ok:
        sqlalchemy_ok = await test_sqlalchemy_connection()
        if sqlalchemy_ok:
            print("🎉 All connections working!")
        else:
            print("⚠️ SQLAlchemy connection needs attention")
    else:
        print("❌ All direct connections failed")

if __name__ == "__main__":
    asyncio.run(main()) 