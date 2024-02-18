from flask import Flask
from flask_login import LoginManager
from database import db
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY environment variable is not set.")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))


# Register the Blueprint
from routes import main as main_blueprint

app.register_blueprint(main_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
