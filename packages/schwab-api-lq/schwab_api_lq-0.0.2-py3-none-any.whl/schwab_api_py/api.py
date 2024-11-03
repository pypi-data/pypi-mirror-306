import requests
import base64

class SchwabAPI:
    def __init__(self, app_key, app_secret, refresh_token):
        self.app_key = app_key
        self.app_secret = app_secret
        self.refresh_token = refresh_token
        self.base_url = "https://api.schwabapi.com/trader/v1/"
        self.access_token = None

    def _get_access_token(self):
        headers = {
            'Authorization': f'Basic {base64.b64encode(bytes(f"{self.app_key}:{self.app_secret}", "utf-8")).decode("utf-8")}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        response = requests.post('https://api.schwabapi.com/v1/oauth/token', headers=headers, data=data)
        tD = response.json()

        self.access_token = tD['access_token']
        self.refresh_token = tD['refresh_token']

    def fetch_data(self, endpoint):
        if self.access_token is None:
            self._get_access_token()

        response = requests.get(f'{self.base_url}/{endpoint}', headers={'Authorization': f'Bearer {self.access_token}'})
        return response.json()