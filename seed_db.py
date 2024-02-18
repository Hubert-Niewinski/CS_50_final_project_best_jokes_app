import os
from app import app
from database import db
from models import Joke, JokeCategory, User
from werkzeug.security import generate_password_hash

# List of starting test jokes created by ChatGPT
jokes = [
    {
        "content": "I only know 25 letters of the alphabet. I don't know y.",
        "category": JokeCategory.DAD,
    },
    {
        "content": "I told my wife she should embrace her mistakes. She gave me a hug.",
        "category": JokeCategory.DAD,
    },
    {"content": "Can February March? No, but April May!", "category": JokeCategory.DAD},
    {
        "content": "Knock, knock. Who’s there? Lettuce. Lettuce who? Lettuce in, it's cold out here!",
        "category": JokeCategory.KNOCK_KNOCK,
    },
    {
        "content": "Knock, knock. Who’s there? Atch. Atch who? Bless you!",
        "category": JokeCategory.KNOCK_KNOCK,
    },
    {
        "content": "Knock, knock. Who’s there? Cow says. Cow says who? Cow says moooo!",
        "category": JokeCategory.KNOCK_KNOCK,
    },
    {
        "content": "I'm reading a book on anti-gravity. It's impossible to put down!",
        "category": JokeCategory.PUNS,
    },
    {
        "content": "I would tell a chemistry joke, but I know I wouldn't get a reaction.",
        "category": JokeCategory.PUNS,
    },
    {
        "content": "I'm trying to organize a hide and seek contest, but it's hard to find good players. They're always hiding!",
        "category": JokeCategory.PUNS,
    },
    {
        "content": "What do you call a fish wearing a crown? A king fish.",
        "category": JokeCategory.ANIMAL,
    },
    {
        "content": "Why do cows have hooves instead of feet? Because they lactose.",
        "category": JokeCategory.ANIMAL,
    },
    {
        "content": "How do you catch a squirrel? Climb a tree and act like a nut.",
        "category": JokeCategory.ANIMAL,
    },
    {
        "content": "Why was the computer cold? It left its Windows open.",
        "category": JokeCategory.TECH,
    },
    {
        "content": "Why don't programmers like nature? It has too many bugs.",
        "category": JokeCategory.TECH,
    },
    {
        "content": "There are 10 types of people in the world: those who understand binary, and those who don't.",
        "category": JokeCategory.TECH,
    },
    {
        "content": "A sandwich walks into a bar. The barman says, 'Sorry, we don’t serve food here.'",
        "category": JokeCategory.BAR,
    },
    {
        "content": "Two antennas met on a roof, fell in love and got married. The ceremony wasn’t much, but the reception was excellent.",
        "category": JokeCategory.BAR,
    },
    {
        "content": "A jumper cable walks into a bar. The bartender says, \"I'll serve you, but don't start anything.\"",
        "category": JokeCategory.BAR,
    },
    {
        "content": "Why did the blonde get excited after finishing her puzzle in 6 months? The box said 2-4 years.",
        "category": JokeCategory.BLONDE,
    },
    {
        "content": "How do you keep a blonde busy? Write 'Please turn over' on both sides of a piece of paper.",
        "category": JokeCategory.BLONDE,
    },
    {
        "content": 'Why did the blonde stare at the orange juice bottle? Because it said "Concentrate."',
        "category": JokeCategory.BLONDE,
    },
    # Add more jokes if needed
]


# Function to seed the database with the test jokes
def seed_db():
    print("Seeding the database with test jokes...")
    # Query for a user with the username "admin"
    user = User.query.filter_by(username="admin").first()

    # If no such user exists, create one
    if user is None:
        admin_password = os.getenv("ADMIN_PASSWORD")
        hashed_password = generate_password_hash(admin_password)
        user = User(username="admin", password=hashed_password)
        db.session.add(user)
        db.session.commit()

    # Insert each joke into the database
    for joke in jokes:
        new_joke = Joke(
            content=joke["content"],
            category=joke["category"],
            user_id=user.id,
            keywords=[],
        )
        db.session.add(new_joke)

    # Commit the changes
    db.session.commit()
    print("Done!")


if __name__ == "__main__":
    with app.app_context():
        seed_db()
