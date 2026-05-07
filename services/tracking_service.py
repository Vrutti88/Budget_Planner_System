from models.expense import Expense

def calculate_total_spent(budget_id):
    expenses = Expense.query.filter_by(budget_id=budget_id).all()
    return sum([float(e.amount) for e in expenses])


def calculate_usage(total_spent, budget_amount):
    if budget_amount == 0:
        return 0
    return (total_spent / float(budget_amount)) * 100


def calculate_remaining(budget_amount, total_spent):
    return float(budget_amount) - total_spent