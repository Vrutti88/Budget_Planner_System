from flask import jsonify
from routes import analytics_bp
from models.budget import Budget
from models.expense import Expense
from models.categories import Category

@analytics_bp.route('/api/v1/analytics/dashboard', methods=['GET'])
def dashboard():
    budgets = Budget.query.all()
    expenses = Expense.query.all()

    total_budget = sum([float(b.amount) for b in budgets])
    total_spent = sum([float(e.amount) for e in expenses])

    return jsonify({
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining": total_budget - total_spent
    })

@analytics_bp.route('/api/v1/analytics/categories/<int:user_id>',
                    methods=['GET'])
def category_analytics(user_id):

    budgets = Budget.query.filter_by(
        user_id=user_id
    ).all()

    result = []

    for budget in budgets:

        category = Category.query.get(
            budget.category_id
        )

        expenses = Expense.query.filter_by(
            budget_id=budget.budget_id
        ).all()

        total_spent = sum([
            float(e.amount)
            for e in expenses
        ])

        total_budget = float(
            budget.amount
        )

        remaining = (
            total_budget - total_spent
        )

        usage = 0

        if total_budget > 0:

            usage = (
                total_spent / total_budget
            ) * 100

        result.append({

            "category": category.name,

            "total_budget": total_budget,

            "total_spent": total_spent,

            "remaining": remaining,

            "usage": usage
        })

    return jsonify(result)