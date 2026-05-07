from models.categories import Category
from models.user import db

def create_category(data):
    category = Category(
        user_id=data['user_id'],
        name=data['name']
    )

    db.session.add(category)
    db.session.commit()

    return category