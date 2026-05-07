from flask import jsonify
from routes import alert_bp
from models.alert_log import AlertLog

@alert_bp.route('/api/v1/alerts/logs', methods=['GET'])
def get_alert_logs():
    logs = AlertLog.query.all()

    return jsonify([{
        "log_id": l.log_id,
        "message": l.message,
        "severity": l.severity,
        "time": str(l.triggered_at)
    } for l in logs])