from urllib.parse import urlparse, urlunparse

from pydantic import AnyUrl
from sqlalchemy import create_engine, text


def convert_to_sync_dsn(uri: AnyUrl) -> str:
    """
    Convert an async PostgreSQL URI to a sync PostgreSQL DSN (Data Source Name).
    """
    parsed_uri = urlparse(str(uri))
    
    # Check if the URI is async, then replace with sync scheme
    if parsed_uri.scheme in ["postgresql+asyncpg"]:
        # Create a new URI with the synchronous scheme "postgresql"
        sync_scheme = "postgresql"
        new_uri = parsed_uri._replace(scheme=sync_scheme)
        
        # Rebuild the URI into a string
        sync_dsn = urlunparse(new_uri)
        return sync_dsn
    
    # If already synchronous, return the original URI
    return uri

def create_database(uri: str, db_name: str):    
    # Connect to the default PostgreSQL database
    default_engine = create_engine(uri, isolation_level="AUTOCOMMIT")
    
    # Drop the database if it exists
    with default_engine.connect() as conn:
        query=text(f"DROP DATABASE IF EXISTS {db_name};")
        conn.execute(query)
        print(f"Dropped database '{db_name}' if it existed.")
    
        conn.execute(text(f"CREATE DATABASE {db_name};"))
        print(f"Database '{db_name}' created.")

def populate_database(uri: str, db_name: str):
    default_engine = create_engine(uri, isolation_level="AUTOCOMMIT")
    
    # Create the test table and populate it with data
    with default_engine.connect() as conn:
        # Create the table
        conn.execute(
            text(
                """
                    CREATE TABLE IF NOT EXISTS test_table (
                        id SERIAL PRIMARY KEY, 
                        name TEXT
                    );
                """
            )
        )

        # Check available tables
        result = conn.execute(
            text(
                """
                    SELECT 
                        table_name 
                    FROM 
                        information_schema.tables 
                    WHERE 
                        table_schema='public';
                """
            )
        )
        tables = [row[0] for row in result]

        # Clear existing data
        conn.execute(text("DELETE FROM test_table;"))

        # Insert new data
        conn.execute(
            text("""
                INSERT INTO test_table (name) 
                VALUES ('Alice'), ('Bob'), ('Charlie'), ('David');
            """)
        )
        conn.commit()

def prepare_database(admin_uri: AnyUrl, data_uri: AnyUrl, db_name):
    admin_uri = convert_to_sync_dsn(admin_uri)
    data_uri = convert_to_sync_dsn(data_uri)

    create_database(admin_uri, db_name)
    populate_database(data_uri, db_name)
