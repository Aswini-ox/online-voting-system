from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Connect to SQLite database
def get_db():
    conn = sqlite3.connect('voting.db')
    return conn

# Create tables
def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates
                 (id INTEGER PRIMARY KEY, name TEXT, party TEXT, votes INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS voters
                 (id TEXT PRIMARY KEY, name TEXT, has_voted BOOLEAN)''')
    conn.commit()
    conn.close()

@app.route('/api/candidates')
def get_candidates():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM candidates")
    candidates = c.fetchall()
    conn.close()
    return jsonify(candidates)

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.json
    # Add vote to database
    return jsonify({"message": "Vote recorded!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
