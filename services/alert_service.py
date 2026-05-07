from models.alert_log import AlertLog
from models.alert import Alert
from models.user import db


def check_alert(usage):

    if usage >= 100:
        return "Budget Exceeded", "critical"

    elif usage >= 90:
        return "Critical Alert", "critical"

    elif usage >= 75:
        return "Warning Alert", "warning"

    return None, None


def save_alert(user_id, budget_id, message, severity):

    # create alert first
    alert = Alert(
        budget_id=budget_id,
        alert_type=severity,
        threshold=100
    )

    db.session.add(alert)
    db.session.commit()

    # create log
    log = AlertLog(
        alert_id=alert.alert_id,
        user_id=user_id,
        message=message,
        severity=severity
    )

    db.session.add(log)
    db.session.commit()