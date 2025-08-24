import unittest
import json
from backend import app, journal_entries

class BackendTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        journal_entries.clear()

    def test_add_journal_entry(self):
        # Test adding a new journal entry
        payload = {'entry': 'This is a test journal entry.'}
        response = self.app.post('/journal',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Journal entry added successfully')

    def test_add_journal_entry_invalid_json(self):
        # Sending invalid JSON should return 400
        response = self.app.post('/journal', data='{invalid', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_journal_entry_missing_entry(self):
        # Missing 'entry' key should return 400
        payload = {}
        response = self.app.post('/journal',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_journal_entry_non_string_entry(self):
        # Non-string 'entry' should return 400
        payload = {'entry': 123}
        response = self.app.post('/journal',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_journal_entry_empty_entry(self):
        # Empty string 'entry' should return 400
        payload = {'entry': ''}
        response = self.app.post('/journal',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_journal_entries(self):
        # Test retrieving all journal entries
        response = self.app.get('/journal')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('entries', data)

if __name__ == '__main__':
    unittest.main()
