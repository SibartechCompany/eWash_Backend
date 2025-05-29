import asyncio
import asyncpg
import socket
from urllib.parse import urlparse
from app.core.config import settings

async def test_network_connectivity():
    """Test basic network connectivity to Supabase"""
    try:
        # Parse the URL to get host and port
        parsed = urlparse(settings.DATABASE_URL)
        host = parsed.hostname
        port = parsed.port or 5432
        
        print(f"Testing network connectivity to {host}:{port}...")
        
        # Test TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Network connectivity to {host}:{port} successful")
            return True
        else:
            print(f"❌ Network connectivity to {host}:{port} failed (error code: {result})")
            return False
            
    except Exception as e:
        print(f"❌ Network connectivity test failed: {e}")
        return False

async def test_direct_asyncpg():
    """Test direct asyncpg connection with detailed error handling"""
    try:
        print(f"Testing direct asyncpg connection...")
        print(f"Database URL: {settings.DATABASE_URL}")
        
        # Try to connect with a shorter timeout
        conn = await asyncio.wait_for(
            asyncpg.connect(settings.DATABASE_URL),
            timeout=15.0
        )
        
        result = await conn.fetchval("SELECT 1")
        print(f"✅ Direct asyncpg connection successful (result: {result})")
        await conn.close()
        return True
        
    except asyncio.TimeoutError:
        print("❌ Direct asyncpg connection timed out")
        return False
    except Exception as e:
        print(f"❌ Direct asyncpg connection failed: {type(e).__name__}: {e}")
        return False

async def test_alternative_urls():
    """Test alternative database URLs"""
    urls = [
        # Direct connection
        "postgresql://postgres:mancos2024*@db.ajqkrulblcfjvbfobiph.supabase.co:5432/postgres",
        # Session pooler
        "postgresql://postgres.ajqkrulblcfjvbfobiph:mancos2024*@aws-0-us-east-2.pooler.supabase.com:5432/postgres",
        # Transaction pooler
        "postgresql://postgres.ajqkrulblcfjvbfobiph:mancos2024*@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
    ]
    
    for i, url in enumerate(urls, 1):
        print(f"\nTesting URL {i}: {url[:50]}...")
        try:
            conn = await asyncio.wait_for(
                asyncpg.connect(url),
                timeout=10.0
            )
            result = await conn.fetchval("SELECT 1")
            print(f"✅ URL {i} successful (result: {result})")
            await conn.close()
            return url
        except Exception as e:
            print(f"❌ URL {i} failed: {type(e).__name__}: {e}")
    
    return None

async def main():
    print("=== Diagnóstico de Conexión a Base de Datos ===")
    print(f"URL configurada: {settings.DATABASE_URL}")
    print()
    
    # Test 1: Network connectivity
    network_ok = await test_network_connectivity()
    print()
    
    # Test 2: Direct asyncpg connection
    if network_ok:
        direct_ok = await test_direct_asyncpg()
        print()
        
        # Test 3: Try alternative URLs if direct fails
        if not direct_ok:
            print("Probando URLs alternativas...")
            working_url = await test_alternative_urls()
            if working_url:
                print(f"\n✅ URL funcional encontrada: {working_url}")
                print("Actualiza tu archivo .env con esta URL")
            else:
                print("\n❌ Ninguna URL funciona")
    
    print("\n=== Fin del diagnóstico ===")

if __name__ == "__main__":
    asyncio.run(main()) 