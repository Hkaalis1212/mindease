import unittest
from unittest import mock
import json
from backend import app, journal_entries

class BackendTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        journal_entries.clear()

    def test_add_journal_entry(self):
        # Test adding a new journal entry
        payload = {'message': 'This is a test journal entry.'}
        response = self.app.post('/journal',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Journal entry added successfully')

    def test_add_journal_entry_missing_message(self):
        # Missing 'message' field should return 400
        payload = {}
        response = self.app.post('/journal',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data['error'])

    def test_add_journal_entry_invalid_type(self):
        # Non-string 'message' should return 400
        payload = {'message': 123}
        response = self.app.post('/journal',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('must be a string', data['error'])

    def test_add_journal_entry_internal_error(self):
        # Simulate internal server error
        payload = {'message': 'test'}
        class FailingList(list):
            def append(self, *args, **kwargs):
                raise Exception('DB failure')
        with mock.patch('backend.journal_entries', new=FailingList()):
            response = self.app.post('/journal',
                                     data=json.dumps(payload),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('Internal server error', data['error'])

    def test_get_journal_entries(self):
        # Test retrieving all journal entries
        payload = {'entry': 'Retrieval test entry'}
        self.app.post('/journal',
                      data=json.dumps(payload),
                      content_type='application/json')
        response = self.app.get('/journal')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('entries', data)
        self.assertIn(payload['entry'], data['entries'])

if __name__ == '__main__':
    unittest.main()
