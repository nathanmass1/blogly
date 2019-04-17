from app import app
import unittest


class IntegrationTest(unittest.TestCase):
#Integration tests

    def test_index(self):  
        """Testing status code of homepage """
        client = app.test_client()

        # test client makes a "request" to app
        # note: app is NOT actually running

        # make an assertion about the response
        result = client.get('/')

        self.assertEqual(result.status_code, 302)

    def test_users_page(self):  
        """Testing status code of users page """
        client = app.test_client()

        # test client makes a "request" to app
        # note: app is NOT actually running

        # make an assertion about the response
        result = client.get('/users')

        self.assertEqual(result.status_code, 200)

    def test_add_user(self):
        """testing if form data appears as desired"""
        client = app.test_client()

        result = client.post('/users', data={
            'first_name': 'Joe', 
            'last_name': 'Bob'
        }, follow_redirects=True)

        # self.assertEqual(result.status_code, 200)
        self.assertIn(b'Joe', result.data)



             