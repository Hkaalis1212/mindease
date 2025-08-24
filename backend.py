from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)

# Initialize SQLite database connection and create table
try:
    conn = sqlite3.connect('journal.db', check_same_thread=False)
    conn.execute(
        'CREATE TABLE IF NOT EXISTS journal_entries ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'entry TEXT NOT NULL)'
    )
    conn.commit()
except sqlite3.Error:
    conn = None

@app.route('/journal', methods=['POST'])
def add_journal_entry():
    """
    Adds a new journal entry.

    The request body should be a JSON object with an 'entry' key.
    Example: {'entry': 'This is a journal entry.'}

    Returns:
        A JSON response with a success message and a 201 status code,
        or an error message and a 400 status code if the request is invalid.
    """
    data = request.get_json()
    if not data or 'entry' not in data:
        return jsonify({'error': 'Invalid request body'}), 400

    entry = data['entry']
    try:
        if conn is None:
            raise sqlite3.Error('Database connection not available')
        conn.execute('INSERT INTO journal_entries (entry) VALUES (?)', (entry,))
        conn.commit()
        # In a real application, you would perform AI analysis on the entry here
        return jsonify({'message': 'Journal entry added successfully'}), 201
    except sqlite3.Error:
        return jsonify({'error': 'Database error'}), 500

@app.route('/journal', methods=['GET'])
def get_journal_entries():
    """
    Retrieves all journal entries.

    Returns:
        A JSON response with a list of all journal entries.
    """
    try:
        if conn is None:
            raise sqlite3.Error('Database connection not available')
        cursor = conn.execute('SELECT entry FROM journal_entries')
        entries = [row[0] for row in cursor.fetchall()]
        return jsonify({'entries': entries})
    except sqlite3.Error:
        return jsonify({'error': 'Database error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
