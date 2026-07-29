from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from app.domain.schemas.database import DatabaseTest
import urllib.parse

def build_connection_uri(db_info: DatabaseTest) -> str:
    """Build SQLAlchemy connection URI from DatabaseTest schema."""
    if db_info.cloud_url:
        return db_info.cloud_url

    driver_map = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
        "sqlserver": "mssql+pyodbc",
        "oracle": "oracle+cx_oracle",
        "sqlite": "sqlite",
        "snowflake": "snowflake",
        "bigquery": "bigquery"
    }
    
    driver = driver_map.get(db_info.db_type, "postgresql")
    
    if db_info.db_type == "sqlite":
        # SQLite usually uses just the db_name as file path
        return f"sqlite:///{db_info.db_name or ':memory:'}"
        
    auth = ""
    if db_info.username:
        password = urllib.parse.quote_plus(db_info.password) if db_info.password else ""
        auth = f"{db_info.username}:{password}@"
        
    host_port = f"{db_info.host}"
    if db_info.port:
        host_port += f":{db_info.port}"
        
    db = f"/{db_info.db_name}" if db_info.db_name else ""
    
    uri = f"{driver}://{auth}{host_port}{db}"
    
    if db_info.ssl_enabled:
        # Simplistic SSL append; exact params vary by dialect
        uri += "?sslmode=require" if "?" not in uri else "&sslmode=require"
        
    return uri

def test_connection(db_info: DatabaseTest) -> tuple[bool, str]:
    """Test connection to the database. Returns (success, message)."""
    try:
        uri = build_connection_uri(db_info)
        engine = create_engine(uri, pool_pre_ping=True, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            # Execute a simple query
            pass
        return True, "Connection successful"
    except SQLAlchemyError as e:
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"
