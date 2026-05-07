from models.budget import Budget

def get_active_budget(user_id, category_id, date):
    return Budget.query.filter(
        Budget.user_id == user_id,
        Budget.category_id == category_id,
        Budget.start_date <= date,
        Budget.end_date >= date,
        Budget.status == 'active'
    ).first()