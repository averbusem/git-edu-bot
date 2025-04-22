import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "git_education_bot"
USERS_COLLECTION = "users"
RESULTS_COLLECTION = "results"
