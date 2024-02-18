# Best Jokes Application

#### Video Demo: <URL HERE>

#### Description:

This is a Flask application that allows users to find, view, add, mark as favorite, and rate jokes from around the world. The application is designed to bring humor to users' lives by providing a platform where they can share and enjoy jokes. Users can search for jokes based on specific parameters, making it easy to find jokes that suit their sense of humor. The ability to add jokes allows users to share their own humor with the community. The favorite feature lets users save jokes they particularly enjoy, while the rating system helps highlight the most appreciated jokes in the community.

## Features

- **Register a new account**: Sign up to become a part of the community and gain access to all features.
- **Login to your account**: Securely login to your account to view, add, and rate jokes.
- **Find a joke**: Search for jokes based on your preferences.
- **Add a new joke**: Share your own joke with the community.
- **Add a joke to favorites**: Save jokes you particularly enjoy to your favorites.
- **View a list of favorite jokes**: Access your favorite jokes at any time.
- **View a ranking of jokes**: See the most appreciated jokes in the community based on user ratings.

## Project Structure

The application has a standard Flask project structure:

- `app.py`: This is the main application file where the Flask app is created and routes are defined.
- `models.py`: This file defines the database models using SQLAlchemy.
- `seed_db.py`: This script is used to seed the database with initial data.
- `.venv`: This directory contains the virtual environment.
- `requirements.txt`: This file lists the Python dependencies that can be installed with pip.
- `static`: This directory contains static files like CSS, JavaScript, and images.
  - `logo.jpg`: This is the logo image.
- `templates`: This directory contains Jinja2 templates. Each HTML file in this directory corresponds to a different page in the application.
  - `base.html`: This is the base template.
  - `index.html`: This is the home page template.
  - `add-joke.html`: This is the add joke page template.
  - `find-joke.html`: This is the find joke page template.
  - `login.html`: This is the login page template.
  - `register.html`: This is the registration page template.
  - `favorite-jokes.html`: This is the favorite jokes page template.
  - `jokes-ranking.html`: This is the jokes ranking page template.

## Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Create a virtual environment: `python3 -m venv .venv`
4. Activate the virtual environment: `source .venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`
6. Run the models script to create the database: `python models.py`
7. Set the environment variable for the admin password: `export ADMIN_PASSWORD={your_password}`
8. (OPTIONAL) Run the database seed script to add base jokes pool: `python seed_db.py`
9. Set the environment variable for the secret key: `export SECRET_KEY={your_password}`
10. Run the application: `flask run`

`export VARIABLE_NAME=value` applies to Linux and Mac Os command line, for Windows use:  
`set VARIABLE_NAME=value` (Command Prompt)  
`$env:VARIABLE_NAME="value"` (PowerShell)

## Usage

Navigate to `http://127.0.0.1:5000` in your web browser to use the application. You can login as admin using `username = admin` and `password={ADMIN_PASSWORD}`

## Author

Hubert Niewinski - Github: [Hubert-Niewinski](https://github.com/Hubert-Niewinski)

## AI tools usage

The application was built with the assistance of GitHub Copilot and OpenAI's ChatGPT. These AI tools were used to enhance productivity by enabling faster syntax retrieval and improved debugging capabilities. All functionalities and the design of the app were chosen by the app's author.
