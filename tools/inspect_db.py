import sqlite3
from pprint import pprint

def inspect_database():
    conn = sqlite3.connect('ethical_framework.db')
    cursor = conn.cursor()
    
    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n=== Database Tables ===")
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("\nColumns:")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
        
        # Get sample data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        rows = cursor.fetchall()
        print("\nSample Data:")
        for row in rows:
            pprint(row)
            print()
    
    conn.close()

if __name__ == "__main__":
    inspect_database() 