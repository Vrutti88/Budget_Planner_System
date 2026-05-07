from flask import request, jsonify
from routes import expense_bp
from models.user import db
from models.expense import Expense
from models.budget import Budget
from models.alert import Alert
from models.alert_log import AlertLog
from models.categories import Category

@expense_bp.route('/api/v1/expenses', methods=['POST'])
def create_expense():

    data = request.json

    if not data['amount']:

            return jsonify({
                "message": "Amount required"
            }), 400

    if float(data['amount']) <= 0:

        return jsonify({
            "message": "Invalid amount"
        }), 400

    # Find active budget

    budget = Budget.query.filter_by(
        category_id=data['category_id'],
        status='active'
    ).first()

    budget_id = budget.budget_id if budget else None

    # Save expense

    expense = Expense(
        user_id=data['user_id'],
        category_id=data['category_id'],
        budget_id=budget_id,
        amount=data['amount'],
        description=data['description'],
        expense_date=data['expense_date']
    )

    db.session.add(expense)
    db.session.commit()

    # No budget found

    if not budget:

        return jsonify({
            "status": "success",
            "message": "No budget found"
        })

    # Calculate total spent

    expenses = Expense.query.filter_by(
        budget_id=budget_id
    ).all()

    total_spent = sum([
        float(e.amount)
        for e in expenses
    ])

    usage = (
        total_spent / float(budget.amount)
    ) * 100

    remaining = (
        float(budget.amount) - total_spent
    )

    # Alert Logic

    category = Category.query.get(
        data['category_id']
    )

    category_name = category.name

    alert_message = None
    alert_type = None

    if usage >= 100:

        alert_message = f"""
        Budget exceeded for {category_name}.
        You spent ₹{total_spent}
        out of ₹{budget.amount}.
        """

        alert_type = "exceeded"

    elif usage >= 90:

        alert_message = f"""
        Critical warning for {category_name}.
        Budget usage reached
        {usage:.2f}% .
        """

        alert_type = "critical"

    elif usage >= 75:

        alert_message = f"""
        Warning for {category_name}.
        You already used
        {usage:.2f}% of your budget.
        """

        alert_type = "warning"

    # Create Alert + Alert Log

    existing_alert = Alert.query.filter_by(
    budget_id=budget_id,
    alert_type=alert_type
    ).first()

    if alert_message and not existing_alert:

        alert = Alert(
            budget_id=budget_id,
            alert_type=alert_type,
            threshold=usage
        )

        db.session.add(alert)
        db.session.commit()

        log = AlertLog(
            alert_id=alert.alert_id,
            user_id=data['user_id'],
            message=alert_message,
            severity=alert_type
        )

        db.session.add(log)
        db.session.commit()

    return jsonify({

        "status": "success",

        "total_spent": total_spent,

        "usage": usage,

        "remaining": remaining,

        "alert": alert_message
    })

from models.categories import Category

@expense_bp.route('/api/v1/expenses', methods=['GET'])
def get_expenses():

    expenses = Expense.query.order_by(
        Expense.expense_id.desc()
    ).all()

    result = []

    for e in expenses:

        category = Category.query.get(
            e.category_id
        )

        result.append({

            "expense_id": e.expense_id,

            "amount": float(e.amount),

            "description": e.description,

            "expense_date": str(e.expense_date),

            "category":
                category.name if category else "-"

        })

    return jsonify(result)

@expense_bp.route('/api/v1/expenses/<int:id>', methods=['PUT'])
def update_expense(id):

    expense = Expense.query.get(id)

    if not expense:

        return jsonify({
            "message": "Expense not found"
        }), 404

    data = request.json

    expense.amount = data['amount']
    expense.description = data['description']

    db.session.commit()

    return jsonify({
        "message": "Expense updated"
    })

@expense_bp.route('/api/v1/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):

    expense = Expense.query.get(id)

    if not expense:

        return jsonify({
            "message": "Expense not found"
        }), 404

    db.session.delete(expense)

    db.session.commit()

    return jsonify({
        "message": "Expense deleted"
    })