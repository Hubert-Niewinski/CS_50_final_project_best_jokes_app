from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from models import *
import re

# Create a Blueprint instance
main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if not username or not password or not password_confirm:
            flash("Please, fill in all fields")
            return render_template("register.html")

        if password != password_confirm:
            flash("Passwords do not match")
            return render_template("register.html")

        if (
            len(password) < 8
            or not re.search(r"\d", password)
            or not re.search(r"\W", password)
        ):
            flash(
                "Password must be at least 8 characters long and contain at least 1 number and 1 special character"
            )
            return render_template("register.html")

        # Check if a user with the given username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash(
                "A user with this username already exists. Please choose a different username."
            )
            return render_template("register.html")

        new_user = User(
            username=username,
            password=generate_password_hash(password, method="pbkdf2:sha256"),
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please, fill in all fields", "error")
            return render_template("login.html")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful. Welcome, {}!".format(username), "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password", "error")
            return render_template("login.html")

    return render_template("login.html")


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/add-joke", methods=["GET", "POST"])
@login_required
def add_joke():
    if request.method == "POST":
        joke_content = request.form.get("joke_content")
        keywords = re.split(",| ", request.form.get("keywords"))
        category = request.form.get("category")
        new_joke = Joke(
            content=joke_content,
            user_id=current_user.id,
            keywords=keywords,
            category=category,
        )
        db.session.add(new_joke)
        db.session.commit()
        flash("Joke added successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("add_joke.html", categories=JokeCategory)


@main.route("/find-joke", methods=["GET", "POST"])
def find_joke():
    categories = JokeCategory
    if request.method == "POST":
        keywords = (
            re.split(",| ", request.form.get("keywords"))
            if request.form.get("keywords") and request.form.get("keywords").strip()
            else None
        )
        author = (
            request.form.get("author")
            if request.form.get("author") and request.form.get("author").strip()
            else None
        )
        rating = (
            request.form.get("rating")
            if request.form.get("rating") and request.form.get("rating").strip()
            else None
        )
        category = (
            request.form.get("category")
            if request.form.get("category") and request.form.get("category").strip()
            else None
        )

        parameters = [keywords, author, rating, category]
        if parameters.count(None) > 2:
            flash("Please provide at least 2 parameters to search", "error")
            return render_template("find_joke.html", categories=categories)

        jokes = Joke.query

        if author:
            author_user = User.query.filter_by(username=author).first()
            if author_user:
                jokes = jokes.filter_by(user_id=author_user.id)

        if rating:
            joke_ids = (
                db.session.query(Rating.joke_id)
                .group_by(Rating.joke_id)
                .having(func.avg(Rating.rating) > rating)
                .all()
            )
            joke_ids = [joke_id for joke_id, in joke_ids]
            jokes = jokes.filter(Joke.id.in_(joke_ids))

        if category:
            jokes = jokes.filter_by(category=category)

        jokes = jokes.all()

        # Manually filter jokes by keywords
        if keywords:
            jokes = [
                joke
                for joke in jokes
                if any(keyword in joke.keywords for keyword in keywords)
            ]
        user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
        return render_template(
            "find_joke.html",
            jokes=jokes,
            categories=categories,
            user_ratings=user_ratings,
        )

    return render_template("find_joke.html", categories=categories)


@main.route("/rate-joke/<int:joke_id>", methods=["POST"])
@login_required
def rate_joke(joke_id):
    joke = Joke.query.get_or_404(joke_id)
    rating_value = request.form.get("rating")
    if not rating_value:
        flash("No rating provided", "error")
        return redirect(url_for("main.find_joke"))

    existing_rating = Rating.query.filter_by(
        joke_id=joke.id, user_id=current_user.id
    ).first()
    if existing_rating:
        flash("You have already rated this joke", "error")
        return redirect(url_for("main.find_joke", _anchor="joke-{}".format(joke_id)))

    rating = Rating(joke_id=joke.id, user_id=current_user.id, rating=rating_value)
    db.session.add(rating)
    db.session.commit()

    flash("Successfully rated joke", "success")
    return redirect(url_for("main.find_joke", _anchor="joke-{}".format(joke_id)))


@main.route("/add-to-favorites/<int:joke_id>", methods=["POST"])
@login_required
def add_to_favorites(joke_id):
    joke = Joke.query.get_or_404(joke_id)

    # Check if the joke is already in the user's favorites
    if joke in current_user.favorite_jokes:
        flash("This joke is already in your favorites", "error")
        return redirect(url_for("main.find_joke", _anchor="joke-{}".format(joke_id)))

    # Add the joke to the user's favorites
    current_user.favorite_jokes.append(joke)
    db.session.commit()

    flash("Successfully added joke to favorites", "success")
    return redirect(url_for("main.find_joke", _anchor="joke-{}".format(joke_id)))


@main.route("/favorite-jokes", methods=["GET", "POST"])
@login_required
def favorite_jokes():
    if request.method == "POST":
        joke_id = request.form.get("joke_id")
        joke = Joke.query.get_or_404(joke_id)
        current_user.favorite_jokes.append(joke)
        db.session.commit()
        flash("Joke added to favorites", "success")
        return redirect(url_for("main.favorite_jokes"))

    favorite_jokes = current_user.favorite_jokes
    return render_template(
        "favorite_jokes.html", favorite_jokes=favorite_jokes, user=current_user
    )


from sqlalchemy.sql import func


from sqlalchemy.sql import func
from sqlalchemy import desc


@main.route("/jokes-ranking")
def jokes_ranking():
    # Get all joke_ids that have at least 3 ratings
    joke_ids = (
        db.session.query(Rating.joke_id)
        .group_by(Rating.joke_id)
        .having(func.count(Rating.joke_id) >= 3)
        .subquery()
    )

    # Get the average rating and count of ratings for each joke_id in joke_ids and order by highest average rating
    jokes = (
        db.session.query(
            Joke,
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.joke_id).label("rate_count"),
        )
        .join(Rating, Joke.id == Rating.joke_id)
        .filter(Joke.id.in_(joke_ids))
        .group_by(Joke.id)
        .order_by(desc("average_rating"))
        .all()
    )

    return render_template("jokes_ranking.html", jokes=jokes)
