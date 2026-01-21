from app.database import engine, Base
from app.models.user import User
from app.models.calculation import CalculationHistory

print("Creating tables...")
print(f"Engine: {engine}")
print(f"Base metadata tables: {Base.metadata.tables.keys()}")

Base.metadata.create_all(engine)

print("✅ Tables created!")

# Verify
import sqlite3
conn = sqlite3.connect("calculator.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nVerification - Tables in database: {tables}")
conn.close()
