import unittest
import json
from backend import app

class BackendTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_journal_entry(self):
        # Test adding a new journal entry
        payload = {'entry': 'This is a test journal entry.'}
        response = self.app.post('/journal',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Journal entry added successfully')

    def test_get_journal_entries(self):
        # Test retrieving all journal entries
        response = self.app.get('/journal')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('entries', data)

if __name__ == '__main__':
    unittest.main()
