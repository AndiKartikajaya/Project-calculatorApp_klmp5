#!/usr/bin/env python3
"""
Simple script to check SQLite database content
"""

import sqlite3
import os

# Database file location
DB_PATH = "calculator.db"

if not os.path.exists(DB_PATH):
    print(f"❌ Database file not found: {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 70)
print("📊 DATABASE INSPECTION - calculator.db")
print("=" * 70)

# Get all tables
print("\n📋 TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(f"   • {table[0]}")

# Check users
print("\n👥 USERS:")
try:
    cursor.execute("SELECT id, username, email, created_at FROM users")
    users = cursor.fetchall()
    if users:
        for user in users:
            print(f"   ID: {user[0]} | Username: {user[1]} | Email: {user[2]} | Created: {user[3]}")
    else:
        print("   ⚠️  No users found")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Check calculation history
print("\n📈 CALCULATION HISTORY:")
try:
    cursor.execute("""
        SELECT id, user_id, operation_type, expression, result, created_at 
        FROM calculation_history 
        ORDER BY created_at DESC 
        LIMIT 20
    """)
    histories = cursor.fetchall()
    if histories:
        print(f"   Total records: {len(histories)}")
        for h in histories:
            print(f"   [{h[0]}] User {h[1]} | {h[2]:12} | {h[3]:20} = {h[4]:12} | {h[5]}")
    else:
        print("   ⚠️  No calculation history found")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary by user
print("\n📊 CALCULATION SUMMARY BY USER:")
try:
    cursor.execute("""
        SELECT u.id, u.username, COUNT(ch.id) as count
        FROM users u
        LEFT JOIN calculation_history ch ON u.id = ch.user_id
        GROUP BY u.id
        ORDER BY count DESC
    """)
    summary = cursor.fetchall()
    for row in summary:
        print(f"   User {row[0]} ({row[1]}): {row[2]} calculations")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Database file info
print(f"\n📁 DATABASE FILE INFO:")
if os.path.exists(DB_PATH):
    size = os.path.getsize(DB_PATH)
    print(f"   Location: {os.path.abspath(DB_PATH)}")
    print(f"   Size: {size} bytes ({size / 1024:.2f} KB)")

print("\n" + "=" * 70)

conn.close()
