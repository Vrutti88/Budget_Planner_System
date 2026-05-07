from routes.auth_routes import auth_bp
from routes.category_routes import category_bp
from routes.budget_routes import budget_bp
from routes.expense_routes import expense_bp
from routes.alert_routes import alert_bp
from routes.analytics_routes import analytics_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(analytics_bp)