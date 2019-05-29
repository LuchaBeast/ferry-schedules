from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open_by_key('1sh4UaaL4ZVAIz4ffvYTeTo8se83rxGFaGbN4C2wjfAI')

@app.route('/')
def homepage():
    schedule = sheet.get_worksheet(1).get_all_values()
    return render_template('index.html', schedule=schedule)

@app.route('/bremerton-seattle/')
def schedule():
    schedule = sheet.get_worksheet(1).get_all_values()
    return render_template('schedule.html', schedule=schedule)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)