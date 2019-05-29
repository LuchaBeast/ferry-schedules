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
    return 'Homepage'

@app.route('/bremerton-seattle/')
def schedule():
    schedule = sheet.get_worksheet(1)

    depart_bremerton = []
    arrive_seattle = []

    depart_bremerton_cells = schedule.range('A1:A15')
    arrive_seattle_cells = schedule.range('B1:B15')

    for cell in depart_bremerton_cells:
        depart_bremerton.append(cell.value)

    for cell in arrive_seattle_cells:
        arrive_seattle.append(cell.value)

    times = dict(zip(depart_bremerton, arrive_seattle))

    return render_template('schedule.html', times=times.items())

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)