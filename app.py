from flask import Flask, render_template
from models.user import db
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('index.html')

db.init_app(app)

# import models
from models.user import User
from models.categories import Category
from models.budget import Budget
from models.expense import Expense
from models.alert import Alert
from models.alert_log import AlertLog

# register routes
from routes.register_routes import register_routes
register_routes(app)

# create tables
with app.app_context():
    db.create_all()

# run app
if __name__ == "__main__":
    app.run(port=5000, debug=True)