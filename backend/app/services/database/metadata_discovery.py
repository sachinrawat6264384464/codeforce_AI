from sqlalchemy import create_engine, inspect
from typing import Dict, Any, List
from app.domain.models.database import ConnectedDatabase
from app.services.database.connection import build_connection_uri
from app.services.database.encryption import decrypt_password
from app.domain.schemas.database import DatabaseTest

def get_metadata(db: ConnectedDatabase) -> Dict[str, Any]:
    """Extract metadata from the connected database."""
    # Build a DatabaseTest object from ConnectedDatabase to reuse build_connection_uri
    db_info = DatabaseTest(
        name=db.name,
        db_type=db.db_type,
        host=db.host,
        port=db.port,
        db_name=db.db_name,
        username=db.username,
        password=decrypt_password(db.encrypted_password) if db.encrypted_password else None,
        ssl_enabled=db.ssl_enabled,
        cloud_url=db.cloud_url
    )
    
    uri = build_connection_uri(db_info)
    engine = create_engine(uri)
    
    inspector = inspect(engine)
    
    metadata = {
        "schemas": [],
        "tables": {},
        "views": {},
        "relationships": 0,
        "owners": 1, # Default placeholder for now
        "lineage": 0 # Default placeholder for now
    }
    
    schemas = inspector.get_schema_names()
    metadata["schemas"] = schemas
    
    for schema in schemas:
        # Ignore system schemas for postgres/mysql to speed up and clean results
        if schema in ['information_schema', 'pg_catalog', 'pg_toast', 'sys', 'performance_schema', 'mysql']:
            continue
            
        tables = inspector.get_table_names(schema=schema)
        views = inspector.get_view_names(schema=schema)
        
        for table in tables:
            columns = inspector.get_columns(table, schema=schema)
            fks = inspector.get_foreign_keys(table, schema=schema)
            pks = inspector.get_pk_constraint(table, schema=schema)
            indexes = inspector.get_indexes(table, schema=schema)
            
            table_meta = {
                "columns": [{"name": c["name"], "type": str(c["type"])} for c in columns],
                "primary_keys": pks.get("constrained_columns", []) if pks else [],
                "foreign_keys": [{"constrained_columns": fk["constrained_columns"], "referred_table": fk["referred_table"]} for fk in fks],
                "indexes": [{"name": idx["name"], "columns": idx["column_names"]} for idx in indexes]
            }
            
            metadata["relationships"] += len(fks)
            metadata["tables"][f"{schema}.{table}"] = table_meta
            
        for view in views:
            columns = inspector.get_columns(view, schema=schema)
            metadata["views"][f"{schema}.{view}"] = {
                "columns": [{"name": c["name"], "type": str(c["type"])} for c in columns]
            }
            
    return metadata
