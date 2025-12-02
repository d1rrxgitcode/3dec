from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryCRUD:
    def get(self, db: Session, category_id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        return db.query(Category).offset(skip).limit(limit).all()

    def create(self, db: Session, category_in: CategoryCreate) -> Category:
        db_category = Category(**category_in.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    def update(self, db: Session, category_id: int, category_in: CategoryUpdate) -> Optional[Category]:
        db_category = self.get(db, category_id)
        if not db_category:
            return None
        
        update_data = category_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        
        db.commit()
        db.refresh(db_category)
        return db_category

    def delete(self, db: Session, category_id: int) -> bool:
        db_category = self.get(db, category_id)
        if not db_category:
            return False
        
        db.delete(db_category)
        db.commit()
        return True


category_crud = CategoryCRUD()