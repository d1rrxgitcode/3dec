"""
Script to seed the database with sample data for Coffee Shop.

Usage:
    python -m scripts.seed_data
    OR
    python scripts/seed_data.py (from project root)
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Category, Product, User
from app.utils.security import get_password_hash


def seed_database():
    """Seed the database with sample data."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Category).count() > 0:
            print("[INFO] Database already contains data. Skipping seed.")
            return
        
        print("[INFO] Seeding database...")
        
        # Create categories
        categories = [
            Category(
                name="Кофе",
                description="Свежеобжаренный кофе из лучших зерен",
                image_url="https://example.com/coffee.jpg"
            ),
            Category(
                name="Чай",
                description="Ароматные чаи со всего мира",
                image_url="https://example.com/tea.jpg"
            ),
            Category(
                name="Десерты",
                description="Вкусные десерты к напиткам",
                image_url="https://example.com/desserts.jpg"
            ),
            Category(
                name="Аксессуары",
                description="Аксессуары для приготовления кофе",
                image_url="https://example.com/accessories.jpg"
            )
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()
        print("[SUCCESS] Categories created")
        
        # Get category IDs
        coffee_cat = db.query(Category).filter(Category.name == "Кофе").first()
        tea_cat = db.query(Category).filter(Category.name == "Чай").first()
        dessert_cat = db.query(Category).filter(Category.name == "Десерты").first()
        acc_cat = db.query(Category).filter(Category.name == "Аксессуары").first()
        
        # Create products
        products = [
            # Coffee
            Product(
                name="Эспрессо",
                description="Классический итальянский эспрессо",
                price=150.00,
                category_id=coffee_cat.id,
                stock_quantity=100,
                is_available=True,
                image_url="https://example.com/espresso.jpg"
            ),
            Product(
                name="Капучино",
                description="Эспрессо с молочной пенкой",
                price=200.00,
                category_id=coffee_cat.id,
                stock_quantity=100,
                is_available=True,
                image_url="https://example.com/cappuccino.jpg"
            ),
            Product(
                name="Латте",
                description="Нежный кофе с молоком",
                price=220.00,
                category_id=coffee_cat.id,
                stock_quantity=100,
                is_available=True,
                image_url="https://example.com/latte.jpg"
            ),
            Product(
                name="Американо",
                description="Эспрессо с горячей водой",
                price=180.00,
                category_id=coffee_cat.id,
                stock_quantity=100,
                is_available=True,
                image_url="https://example.com/americano.jpg"
            ),
            # Tea
            Product(
                name="Зеленый чай",
                description="Классический зеленый чай",
                price=120.00,
                category_id=tea_cat.id,
                stock_quantity=50,
                is_available=True,
                image_url="https://example.com/green-tea.jpg"
            ),
            Product(
                name="Черный чай",
                description="Крепкий черный чай",
                price=100.00,
                category_id=tea_cat.id,
                stock_quantity=50,
                is_available=True,
                image_url="https://example.com/black-tea.jpg"
            ),
            # Desserts
            Product(
                name="Тирамису",
                description="Классический итальянский десерт",
                price=300.00,
                category_id=dessert_cat.id,
                stock_quantity=20,
                is_available=True,
                image_url="https://example.com/tiramisu.jpg"
            ),
            Product(
                name="Чизкейк",
                description="Нежный чизкейк New York style",
                price=280.00,
                category_id=dessert_cat.id,
                stock_quantity=15,
                is_available=True,
                image_url="https://example.com/cheesecake.jpg"
            ),
            Product(
                name="Круассан",
                description="Свежий французский круассан",
                price=150.00,
                category_id=dessert_cat.id,
                stock_quantity=30,
                is_available=True,
                image_url="https://example.com/croissant.jpg"
            ),
            # Accessories
            Product(
                name="Кофейные зерна (1кг)",
                description="Свежеобжаренные зерна Арабики",
                price=1200.00,
                category_id=acc_cat.id,
                stock_quantity=50,
                is_available=True,
                image_url="https://example.com/beans.jpg"
            ),
            Product(
                name="Френч-пресс",
                description="Стеклянный френч-пресс 350мл",
                price=800.00,
                category_id=acc_cat.id,
                stock_quantity=10,
                is_available=True,
                image_url="https://example.com/french-press.jpg"
            ),
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        print("[SUCCESS] Products created")
        
        # Create demo user
        demo_user = User(
            email="demo@coffeeshop.com",
            username="demo",
            hashed_password=get_password_hash("demo123"),
            full_name="Demo User",
            phone="+1234567890",
            address="123 Demo Street",
            is_active=True,
            is_admin=False
        )
        db.add(demo_user)
        db.commit()
        print("[SUCCESS] Demo user created")
        
        print("\n[SUCCESS] Database seeded successfully!")
        print("\nDemo credentials:")
        print("   Email: demo@coffeeshop.com")
        print("   Password: demo123")
        print("\n[INFO] To create admin user, run: python scripts/init_admin.py")
        
    except Exception as e:
        print(f"[ERROR] Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

