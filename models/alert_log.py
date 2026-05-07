from models.user import db

class AlertLog(db.Model):
    __tablename__ = 'alert_log'

    log_id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.alert_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    triggered_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)
    severity = db.Column(db.Enum('info', 'warning', 'critical', 'error', 'exceeded'), default='info')