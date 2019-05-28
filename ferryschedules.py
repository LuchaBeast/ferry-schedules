from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open_by_key('1sh4UaaL4ZVAIz4ffvYTeTo8se83rxGFaGbN4C2wjfAI')

depart_seattle_am = sheet.get_worksheet(0)

@app.route('/')
def homepage():
    first_time = depart_seattle_am.acell('A1').value
    return first_time

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)