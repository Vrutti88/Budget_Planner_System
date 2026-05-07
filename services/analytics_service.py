from models.budget import Budget
from models.expense import Expense

def get_dashboard_data():
    budgets = Budget.query.all()
    expenses = Expense.query.all()

    total_budget = sum([float(b.amount) for b in budgets])
    total_spent = sum([float(e.amount) for e in expenses])

    return {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining": total_budget - total_spent
    }