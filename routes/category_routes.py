from flask import request, jsonify
from routes import category_bp
from models.user import db
from models.categories import Category

@category_bp.route('/api/v1/categories', methods=['GET'])
def get_categories():
    user_id = request.args.get('user_id')

    categories = Category.query.filter_by(
        user_id=user_id
    ).all()
    return jsonify([{
        "category_id": c.category_id,
        "name": c.name
    } for c in categories])


@category_bp.route('/api/v1/categories', methods=['POST'])
def create_category():
    data = request.json

    category = Category(
        user_id=data['user_id'],
        name=data['name']
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({"status": "success"})

@category_bp.route(
    '/api/v1/categories/default/<int:user_id>',
    methods=['GET']
)
def create_default_categories(user_id):

    names = [
        "Food",
        "Travel",
        "Shopping",
        "Entertainment",
        "Bills"
    ]

    for name in names:

        existing = Category.query.filter_by(
            user_id=user_id,
            name=name
        ).first()

        if not existing:

            category = Category(
                user_id=user_id,
                name=name
            )

            db.session.add(category)

    db.session.commit()

    return jsonify({
        "message": "Default categories added"
    })