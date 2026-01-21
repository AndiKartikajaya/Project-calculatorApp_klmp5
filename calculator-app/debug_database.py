#!/usr/bin/env python3
"""
Debug script to check database status and saved calculations
"""

from app.database import SessionLocal, engine
from app.models.calculation import CalculationHistory, User
from sqlalchemy import text

def check_database():
    """Check database connections and data"""
    try:
        db = SessionLocal()
        
        print("=" * 60)
        print("DATABASE DEBUG CHECK")
        print("=" * 60)
        
        # Check tables
        print("\n1. Checking tables...")
        inspector = engine.inspect(engine)
        tables = inspector.get_table_names()
        print(f"   Tables found: {tables}")
        
        # Check users
        print("\n2. Checking users...")
        users = db.query(User).all()
        print(f"   Total users: {len(users)}")
        for user in users:
            print(f"   - User ID {user.id}: {user.username}")
        
        # Check history
        print("\n3. Checking calculation history...")
        histories = db.query(CalculationHistory).all()
        print(f"   Total history records: {len(histories)}")
        
        if histories:
            print("\n   Recent calculations:")
            for h in sorted(histories, key=lambda x: x.created_at, reverse=True)[:10]:
                print(f"   - [{h.operation_type}] {h.expression} = {h.result} (User {h.user_id})")
        else:
            print("   ⚠️  No calculations found!")
        
        # Check by user
        if users:
            print("\n4. Checking calculations by user...")
            for user in users:
                count = db.query(CalculationHistory).filter(CalculationHistory.user_id == user.id).count()
                print(f"   - {user.username}: {count} calculations")
        
        print("\n" + "=" * 60)
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database()
