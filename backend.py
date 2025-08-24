from flask import Flask, request, jsonify
import os
import logging
import json

app = Flask(__name__)


class JSONFormatter(logging.Formatter):
    """Format log records as JSON."""

    def format(self, record):
        log_record = {
            "level": record.levelname,
            "time": self.formatTime(record, self.datefmt),
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in (
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "message",
            ):
                log_record[key] = value
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


logger = app.logger
logger.setLevel(logging.INFO)
logger.handlers = []

formatter = JSONFormatter()

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("backend.log")
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

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
        logger.warning("Invalid journal entry request", extra={"data": data})
        return jsonify({'error': 'Invalid request body'}), 400

    entry = data['entry']
    journal_entries.append(entry)
    logger.info("Journal entry added", extra={"entry": entry})
    # In a real application, you would perform AI analysis on the entry here
    return jsonify({'message': 'Journal entry added successfully'}), 201

@app.route('/journal', methods=['GET'])
def get_journal_entries():
    """
    Retrieves all journal entries.

    Returns:
        A JSON response with a list of all journal entries.
    """
    logger.info("Retrieved journal entries", extra={"count": len(journal_entries)})
    return jsonify({'entries': journal_entries})


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    logger.info("Health check requested")
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
