from models.user import db

class Alert(db.Model):
    __tablename__ = 'alerts'

    alert_id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.budget_id'), nullable=False)
    alert_type = db.Column(db.Enum('warning', 'critical', 'exceeded'), nullable=False)
    threshold = db.Column(db.Numeric(5, 2), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())