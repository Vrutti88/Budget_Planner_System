from flask import request, jsonify
from routes import budget_bp
from models.user import db
from models.budget import Budget

@budget_bp.route('/api/v1/budgets', methods=['POST'])
def create_budget():
    data = request.json

    budget = Budget(
        user_id=data['user_id'],
        category_id=data['category_id'],
        amount=data['amount'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )

    if float(data['amount']) <= 0:

        return jsonify({
            "message": "Invalid budget amount"
        }), 400

    db.session.add(budget)
    db.session.commit()

    return jsonify({"status": "success"})


@budget_bp.route('/api/v1/budgets', methods=['GET'])
def get_budgets():
    budgets = Budget.query.all()

    return jsonify([{
        "budget_id": b.budget_id,
        "amount": float(b.amount)
    } for b in budgets])

@budget_bp.route('/api/v1/budgets/<int:id>', methods=['PUT'])
def update_budget(id):

    budget = Budget.query.get(id)

    if not budget:

        return jsonify({
            "message": "Budget not found"
        }), 404

    data = request.json

    budget.amount = data['amount']
    budget.start_date = data['start_date']
    budget.end_date = data['end_date']

    db.session.commit()

    return jsonify({
        "message": "Budget updated"
    })

@budget_bp.route('/api/v1/budgets/<int:id>', methods=['DELETE'])
def delete_budget(id):

    budget = Budget.query.get(id)

    if not budget:

        return jsonify({
            "message": "Budget not found"
        }), 404

    db.session.delete(budget)

    db.session.commit()

    return jsonify({
        "message": "Budget deleted"
    })