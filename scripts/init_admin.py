"""
Script to create an admin user for the Coffee Shop API.
Run this script after setting up the database.

Usage:
    python -m scripts.init_admin
    OR
    python scripts/init_admin.py (from project root)
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.utils.security import get_password_hash

def create_admin():
    """Create an admin user if it doesn't exist."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@coffeeshop.com").first()
        
        if admin:
            print("[ERROR] Admin user already exists!")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@coffeeshop.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            phone="+1234567890",
            address="Coffee Shop HQ",
            is_active=True,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("[SUCCESS] Admin user created successfully!")
        print("   Email: admin@coffeeshop.com")
        print("   Password: admin123")
        print("   [WARNING] Please change the password after first login!")
        
    except Exception as e:
        print(f"[ERROR] Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()

