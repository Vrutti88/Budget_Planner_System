from models.expense import Expense
from models.user import db

def create_expense(data, budget_id):
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

    return expense