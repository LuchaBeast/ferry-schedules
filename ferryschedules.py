from flask import Flask, render_template, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open_by_key('1sh4UaaL4ZVAIz4ffvYTeTo8se83rxGFaGbN4C2wjfAI')

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/')
def homepage():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    links.sort()
    return render_template('index.html', links=links)

# Bremerton Ferry Schedule route
@app.route('/bremerton-seattle/')
def bremertonSchedule():
    # Get worksheet with schedules
    ws = sheet.get_worksheet(1)

    # Set title tag variable
    title = ws.acell('E2').value
    
    # Set h1 tag variable
    h1 = ws.acell('E3').value

    # Set leadcopy variable
    leadcopy = ws.acell('E4').value

    # Set table headers for each schedule
    table_headers_1 = {'Depart Bremerton':'Arrive Seattle'}
    table_headers_2 = {'Depart Seattle':'Arrive Bremerton'}

    ### Depart Bremerton schedule code begins
    
    # Create empty lists for storing schedule times
    depart_bremerton_schedule = []
    arrive_seattle_schedule = []

    # Get the cells for each schedule
    depart_bremerton_cells = ws.range('A2:A16')
    arrive_seattle_cells = ws.range('B2:B16')

    # Iterate through each set of cells
    # and add the value to each list
    for cell in depart_bremerton_cells:
        depart_bremerton_schedule.append(cell.value)

    for cell in arrive_seattle_cells:
        arrive_seattle_schedule.append(cell.value)

    # Convert both lists into a single dictionary
    times_1 = dict(zip(depart_bremerton_schedule, arrive_seattle_schedule))

    ### Depart Bremerton schedule code ends

    ### Depart Seattle schedule code
    
    # Create empty lists for storing schedule times
    depart_seattle_schedule = []
    arrive_bremerton_schedule = []

    # Get the cells for each schedule
    depart_seattle_cells = ws.range('A19:A33')
    arrive_bremerton_cells = ws.range('B19:B33')
    
    # Iterate through each set of cells
    # and add the value to each list
    for cell in depart_seattle_cells:
        depart_seattle_schedule.append(cell.value)

    for cell in arrive_bremerton_cells:
        arrive_bremerton_schedule.append(cell.value)

    # Convert both lists into a single dictionary
    times_2 = dict(zip(depart_seattle_schedule, arrive_bremerton_schedule))

    ### Depart Seattle schedule code ends
    
    return render_template('schedule.html',
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy)

# Bainbridge Ferry Schedule route
@app.route('/bainbridge-seattle/')
def bainbridgeSchedule():
    # Get worksheet with schedules
    ws = sheet.get_worksheet(3)

    # Set title tag variable
    title = ws.acell('E3').value
    
    # Set h1 tag variable
    h1 = ws.acell('E4').value

    # Set leadcopy variable
    leadcopy = ws.acell('E5').value

    # Set table headers for each schedule
    table_headers_1 = {'Depart Bainbridge Island':'Arrive Seattle'}
    table_headers_2 = {'Depart Seattle':'Arrive Bainbridge Island'}

    ### Depart Bremerton schedule code begins
    
    # Create empty lists for storing schedule times
    depart_bainbridge_schedule = []
    arrive_seattle_schedule = []

    # Get the cells for each schedule
    depart_bainbridge_cells = ws.range('A28:A50')
    arrive_seattle_cells = ws.range('B28:B50')

    # Iterate through each set of cells
    # and add the value to each list
    for cell in depart_bainbridge_cells:
        depart_bainbridge_schedule.append(cell.value)

    for cell in arrive_seattle_cells:
        arrive_seattle_schedule.append(cell.value)

    # Convert both lists into a single dictionary
    times_1 = dict(zip(depart_bainbridge_schedule, arrive_seattle_schedule))

    ### Depart Bremerton schedule code ends

    ### Depart Seattle schedule code
    
    # Create empty lists for storing schedule times
    depart_seattle_schedule = []
    arrive_bainbridge_schedule = []

    # Get the cells for each schedule
    depart_seattle_cells = ws.range('A3:A25')
    arrive_bainbridge_cells = ws.range('B3:B25')
    
    # Iterate through each set of cells
    # and add the value to each list
    for cell in depart_seattle_cells:
        depart_seattle_schedule.append(cell.value)

    for cell in arrive_bainbridge_cells:
        arrive_bainbridge_schedule.append(cell.value)

    # Convert both lists into a single dictionary
    times_2 = dict(zip(depart_seattle_schedule, arrive_bainbridge_schedule))

    ### Depart Seattle schedule code ends
    
    return render_template('schedule.html',
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy)

# Staten Island Ferry schedule route
@app.route('/staten-island/')
def statenIslandSchedule():
    return 'Staten Island'
    


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)