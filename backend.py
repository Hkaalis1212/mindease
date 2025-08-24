from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# In-memory storage for journal entries (for demonstration purposes)
journal_entries = []

@app.route('/journal', methods=['POST'])
def add_journal_entry():
    """
    Adds a new journal entry.

    The request body should be a JSON object with a 'message' key.
    Example: {'message': 'This is a journal entry.'}

    Returns:
        A JSON response with a success message and a 201 status code,
        or an error message and a 400 status code if the request is invalid.
        Returns a 500 status code if an unexpected error occurs.
    """
    try:
        data = request.get_json(silent=True)
        if not data or 'message' not in data:
            return jsonify({'error': "'message' field is required"}), 400
        message = data['message']
        if not isinstance(message, str):
            return jsonify({'error': "'message' must be a string"}), 400

        journal_entries.append(message)
        # In a real application, you would perform AI analysis on the entry here
        return jsonify({'message': 'Journal entry added successfully'}), 201
    except Exception:
        app.logger.exception('Unhandled exception in add_journal_entry')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/journal', methods=['GET'])
def get_journal_entries():
    """
    Retrieves all journal entries.

    Returns:
        A JSON response with a list of all journal entries.
    """
    try:
        return jsonify({'entries': journal_entries})
    except Exception:
        app.logger.exception('Unhandled exception in get_journal_entries')
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
