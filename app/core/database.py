from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings
import asyncpg

# SQLAlchemy setup for Supabase PostgreSQL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Try to use session pooler (port 5432) instead of transaction pooler
# This might work better with prepared statements
ALTERNATIVE_DATABASE_URL = settings.DATABASE_URL.replace(":6543/", ":5432/")

# Custom connection function for pgbouncer compatibility
async def create_async_connection():
    """Create asyncpg connection with pgbouncer compatibility"""
    # Try session pooler first, then transaction pooler
    urls_to_try = [
        ALTERNATIVE_DATABASE_URL,  # Session pooler (5432)
        settings.DATABASE_URL      # Transaction pooler (6543)
    ]
    
    for url in urls_to_try:
        try:
            conn = await asyncpg.connect(
                url,
                statement_cache_size=0,
                command_timeout=30
            )
            return conn
        except Exception as e:
            print(f"Failed to connect with {url[:50]}...: {e}")
            continue
    
    raise Exception("Could not connect to any database URL")

# Async engine for SQLAlchemy - try session pooler first
try:
    # Try session pooler first (port 5432)
    engine = create_async_engine(
        ALTERNATIVE_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=False,
        future=True,
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=False,
        pool_recycle=60,
        connect_args={
            "statement_cache_size": 0,
            "command_timeout": 30,
            "server_settings": {
                "application_name": "eWash_Backend",
            }
        }
    )
    print("Using session pooler (port 5432)")
except Exception as e:
    print(f"Session pooler failed, trying transaction pooler: {e}")
    # Fallback to transaction pooler (port 6543)
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=False,
        future=True,
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=False,
        pool_recycle=60,
        connect_args={
            "statement_cache_size": 0,
            "command_timeout": 30,
            "server_settings": {
                "application_name": "eWash_Backend",
            }
        }
    )
    print("Using transaction pooler (port 6543)")

# Session factory with autocommit disabled and autoflush enabled
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=True,
    autocommit=False
)

# Base class for models
Base = declarative_base()

# Supabase client (optional, only if needed)
supabase = None
try:
    from supabase import create_client, Client
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
except Exception as e:
    print(f"Warning: Could not initialize Supabase client: {e}")
    print("Continuing with PostgreSQL only...")

# Dependency to get database session with proper error handling
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

# Dependency to get Supabase client
def get_supabase():
    if supabase is None:
        raise Exception("Supabase client not available")
    return supabase

# Database initialization with better error handling
async def init_db():
    """Initialize database tables"""
    try:
        async with engine.begin() as conn:
            # Import all models here to ensure they are registered
            from app.models import user, organization, client, employee, service, order, vehicle
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        # Don't raise the exception to allow the app to start
        print("⚠️ Continuing without database initialization...")

# Database connection test with transaction handling
async def test_db_connection():
    """Test database connection with proper transaction handling"""
    try:
        # Use direct asyncpg connection for testing to avoid SQLAlchemy prepared statements
        conn = await create_async_connection()
        result = await conn.fetchval("SELECT 1")
        await conn.close()
        
        if result == 1:
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection test failed: unexpected result")
            return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False 