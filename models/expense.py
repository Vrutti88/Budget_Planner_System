from models.user import db

class Expense(db.Model):
    __tablename__ = 'expenses'

    expense_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.budget_id'), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.Enum(
        'cash', 'credit_card', 'debit_card', 'upi', 'net_banking', 'other'
    ), default='cash')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())