import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

class Gsheet:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(parentDirectory, 'fssite', 'client_secret.json'), scope)
        self._refresh_auth()

    def _refresh_auth(self):
        client = gspread.authorize(self.creds)
        self.sheet = client.open_by_key('1sh4UaaL4ZVAIz4ffvYTeTo8se83rxGFaGbN4C2wjfAI')

    def _decorate(self, method):
        def safe_method(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except gspread.exceptions.HTTPError as e:
                self._refresh_auth()
                return getattr(self.sheet, method.__name__)(*args, **kwargs)
        return safe_method

    def __getattr__(self, attr):
        return self._decorate(getattr(self.sheet, attr))