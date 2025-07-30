from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# In-memory storage for journal entries (for demonstration purposes)
journal_entries = []

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
    journal_entries.append(entry)
    # In a real application, you would perform AI analysis on the entry here
    return jsonify({'message': 'Journal entry added successfully'}), 201

@app.route('/journal', methods=['GET'])
def get_journal_entries():
    """
    Retrieves all journal entries.

    Returns:
        A JSON response with a list of all journal entries.
    """
    return jsonify({'entries': journal_entries})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
