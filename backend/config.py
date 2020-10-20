from logging import DEBUG

DEBUG = True

# Connect to the database
# DONE: IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:passwd123@localhost:5432/trivia_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False