#!/usr/bin/env python3
"""
SQLite Database Search Utility

Searches all values in a SQLite database for a given string and reports
which tables contain matches.

Usage:
    python search_db.py <db_filepath> <search_string>
"""

import sqlite3
import sys
from pathlib import Path


def search_database(db_path: str, search_string: str) -> None:
    """
    Search all tables and columns in a SQLite database for a given string.
    
    Args:
        db_path: Path to the SQLite database file
        search_string: String to search for in all values
        
    Raises:
        FileNotFoundError: If database file doesn't exist
        sqlite3.DatabaseError: If database is invalid
    """
    db_path = Path(db_path)
    
    if not db_path.exists():
        print(f"Error: Database file not found: {db_path}")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            print("No tables found in database")
            return
        
        results = {}
        search_lower = search_string.lower()
        
        for table_name in tables:
            # Get column names for this table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]
            
            if not columns:
                continue
            
            # Build WHERE clause to search all columns
            where_conditions = " OR ".join(
                f"CAST({col} AS TEXT) LIKE ?" 
                for col in columns
            )
            
            # Search this table
            query = f"SELECT * FROM {table_name} WHERE {where_conditions}"
            search_param = f"%{search_string}%"
            params = [search_param] * len(columns)
            
            try:
                cursor.execute(query, params)
                matches = cursor.fetchall()
                
                if matches:
                    results[table_name] = {
                        'count': len(matches),
                        'columns': columns,
                        'rows': matches
                    }
            except sqlite3.Error as e:
                print(f"Warning: Error searching table '{table_name}': {e}")
                continue
        
        conn.close()
        
        # Print results
        if not results:
            print(f"No matches found for '{search_string}'")
            return
        
        print(f"\n{'='*60}")
        print(f"Search Results for: '{search_string}'")
        print(f"{'='*60}\n")
        
        for table_name, data in sorted(results.items()):
            print(f"📊 Table: {table_name}")
            print(f"   Found {data['count']} matching row(s)")
            print(f"   Columns: {', '.join(data['columns'])}")
            print()
        
        print(f"{'='*60}")
        print(f"Total tables with matches: {len(results)}")
        print(f"{'='*60}")
        
    except sqlite3.DatabaseError as e:
        print(f"Error: Invalid database file - {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python search_db.py <db_filepath> <search_string>")
        print("\nExample: python search_db.py game.db 'ROMAN_CULTURE'")
        sys.exit(1)
    
    db_filepath = sys.argv[1]
    search_str = sys.argv[2]
    
    search_database(db_filepath, search_str)