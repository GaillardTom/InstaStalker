import unittest
import json
from main import app, readTargets, addTarget, deleteTarget, huntSingleTarget, huntAll

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username', response.data)

    async def test_add_valid_target(self):
        response = await self.app.post('/addTarget', data=dict(target='google'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        for target in readTargets():
            if target == b'google\n':
                test = True
                break
            else:
                test = False
        self.assertTrue(test)
    def test_add_invalid_target(self):
        response = self.app.post('/addTarget', data=dict(target='testuser'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        test = False if b'testuser' in readTargets() else True
        self.assertTrue(test)


    def test_delete_target(self):
        self.app.post('/addTarget', data=dict(target='google'))
        response = self.app.post('/deleteTarget/google')
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertNotIn(b'google', readTargets())

    async def test_hunt_single_target(self):
        self.app.post('/addTarget', data=dict(target='google'))
        response = await self.app.post('/hunt/google')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Following', response.data)

    # def test_hunt_all(self):
    #     response = self.app.get('/hunt/all')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'All Following', response.data)

if __name__ == '__main__':
    unittest.main()