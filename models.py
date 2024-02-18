from flask_login import UserMixin
from enum import Enum
from sqlalchemy import PickleType
from sqlalchemy.orm import relationship
from database import db
from app import app


class JokeCategory(Enum):
    DAD = "Dad Jokes"
    KNOCK_KNOCK = "Knock-Knock Jokes"
    PUNS = "Puns"
    ANIMAL = "Animal Jokes"
    TECH = "Tech Jokes"
    BAR = "Bar Jokes"
    BLONDE = "Blonde Jokes"
    POLITICAL = "Political Jokes"
    SCIENCE = "Science Jokes"
    MATH = "Math Jokes"
    OTHER = "Other"


favorite_jokes = db.Table(
    "favorite_jokes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("joke_id", db.Integer, db.ForeignKey("joke.id"), primary_key=True),
    extend_existing=True,
)


class User(db.Model, UserMixin):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    favorite_jokes = db.relationship(
        "Joke",
        secondary=favorite_jokes,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def get_id(self):
        return str(self.id)


class Joke(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="jokes")
    keywords = db.Column(PickleType, nullable=False)
    category = db.Column(db.Enum(JokeCategory), nullable=False)
    ratings = db.relationship("Rating", backref="joke", lazy=True)


class Rating(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False, default=1)
    joke_id = db.Column(db.Integer, db.ForeignKey("joke.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Done!")
