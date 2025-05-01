# test_app.py
import unittest
from app import app

class PQCAppTest(unittest.TestCase):
    def setUp(self):
        # Flask provides a built-in test client
        self.client = app.test_client()

    def test_full_kem_cycle(self):
        # 1) Key generation
        resp = self.client.post('/keygen')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('public_key', data)
        self.assertIn('private_key', data)

        pk = data['public_key']
        sk = data['private_key']

        # 2) Encapsulation (encrypt)
        resp = self.client.post('/encrypt', json={
            'public_key': pk,
            'message': 'ignored-by-kem-but-required'
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('ciphertext', data)
        self.assertIn('shared_secret', data)

        ct = data['ciphertext']
        ss1 = data['shared_secret']

        # 3) Decapsulation (decrypt)
        resp = self.client.post('/decrypt', json={
            'private_key': sk,
            'ciphertext': ct
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('shared_secret', data)

        ss2 = data['shared_secret']

        # 4) Verify shared secrets match
        self.assertEqual(ss1, ss2)

if __name__ == '__main__':
    unittest.main()

