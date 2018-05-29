from django.core.urlresolvers import reverse
from unittest import TestCase
from fitbit import Fitbit
import copy
import json, mock, requests_mock, unittest


class TestFitbit(TestCase):
    client_kwargs = {
        'client_id': '228DDB',
        'client_secret': 'fbf2bdaeb30b9e8b5fd26d9cc1be8a5a',
        'redirect_uri': 'http://127.0.0.1:8000/en/user/add_fitbit',
        'scope': 'weight'
    }

    def test_authorize_token_url(self):
        # authorize_token_url calls oauth and returns a URL
        fb = Fitbit(**self.client_kwargs)
        retval = fb.client.authorize_token_url()
        self.assertEqual(
            retval[0],
            'https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=228DDB&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fen%2Fuser%2Fadd_fitbit&scope=activity+nutrition+heartrate+location+nutrition+profile+settings+sleep+social+weight&state=' + retval[1])

    def test_fetch_access_token(self):
        # tests the fetching of access token using code and redirect_URL
        fb = Fitbit(**self.client_kwargs)
        fake_code = "fake_code"
        with requests_mock.mock() as m:
            m.post(fb.client.access_token_url, text=json.dumps({
                'access_token': 'fake_return_access_token',
                'refresh_token': 'fake_return_refresh_token'
            }))
            retval = fb.client.fetch_access_token(fake_code)
        self.assertEqual("fake_return_access_token", retval['access_token'])
        self.assertEqual("fake_return_refresh_token", retval['refresh_token'])

    def test_refresh_token(self):
        # test of refresh function
        kwargs = copy.copy(self.client_kwargs)
        kwargs['access_token'] = 'fake_access_token'
        kwargs['refresh_token'] = 'fake_refresh_token'
        kwargs['refresh_cb'] = lambda x: None
        fb = Fitbit(**kwargs)
        with requests_mock.mock() as m:
            m.post(fb.client.refresh_token_url, text=json.dumps({
                'access_token': 'fake_return_access_token',
                'refresh_token': 'fake_return_refresh_token'
            }))
            retval = fb.client.refresh_token()
        self.assertEqual("fake_return_access_token", retval['access_token'])
        self.assertEqual("fake_return_refresh_token", retval['refresh_token'])

if __name__ == '__main__':
    unittest.main()
    