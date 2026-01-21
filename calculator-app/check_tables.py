import sqlite3

DB_PATH = "calculator.db"

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"Tables found: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check users table structure
    if any(t[0] == 'users' for t in tables):
        cursor.execute("PRAGMA table_info(users)")
        print("\nUsers table columns:")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
    
    # Check calculation_history table structure
    if any(t[0] == 'calculation_history' for t in tables):
        cursor.execute("PRAGMA table_info(calculation_history)")
        print("\nCalculation_history table columns:")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    print("\n✅ Database check complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
