import sqlite3
from flask import Flask, request

app = Flask(__name__)

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def find_user(self, username):
        # Sink: vulnerable SQL query
        query = "SELECT * FROM users WHERE username = '%s'" % username
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

@app.route("/login", methods=["POST"])
def login():
    # Source: form field
    username = request.form["username"]

    db = Database("users.db")
    user = db.find_user(username)

    if user:
        return "Welcome"
    return "Invalid"

if __name__ == "__main__":
    app.run(debug=True)
