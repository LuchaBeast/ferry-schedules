from flask import Flask, render_template, url_for, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string

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
    
    # Create list of url routes
    links_list = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links_list.append((url, rule.endpoint))
    
    # Sort list and then delete homepage from list
    links_list.sort()
    del links_list[0]

    # Convert list to dictionary
    links = dict(links_list)

    # Modify the endpoints into pretty names
    for k, v in links.items():
        update_name = {k: v.title().replace('_',' ')}
        links.update(update_name)
        
    return render_template('index.html', links=links.items())

# Bremerton Ferry Schedule route
@app.route('/bremerton-seattle/')
def bremerton_schedule():
    
    # Set standard schedule variable to true
    # to indicate no special schedules
    standard_schedule = True
    
    # Get worksheet with schedules
    ws = sheet.get_worksheet(1)

    # Set title tag variable
    title = ws.acell('B1').value
    
    # Set h1 tag variable
    h1 = ws.acell('B2').value

    # Set leadcopy variable
    leadcopy = ws.acell('B3').value

    # Set table headers for each schedule
    table_headers_1 = {ws.acell('D1').value:ws.acell('E1').value}
    table_headers_2 = {ws.acell('G1').value:ws.acell('H1').value}

    h2_1 = ws.acell('B5').value
    h2_2 = ws.acell('B6').value

    ### Depart Bremerton schedule code begins

    # Get the cells for each schedule and delete header cell from list
    depart_bremerton_schedule = ws.col_values(4)
    arrive_seattle_schedule = ws.col_values(5)
    del depart_bremerton_schedule[0]
    del arrive_seattle_schedule[0]

    times_1 = dict(zip(depart_bremerton_schedule, arrive_seattle_schedule))

    ### Depart Bremerton schedule code ends

    ### Depart Seattle schedule code begins
    
    # Get the cells for each schedule
    depart_seattle_schedule = ws.col_values(7)
    arrive_bremerton_schedule = ws.col_values(8)
    del depart_seattle_schedule[0]
    del arrive_bremerton_schedule[0]

    # Convert schedule columns into a single dictionary
    times_2 = dict(zip(depart_seattle_schedule, arrive_bremerton_schedule))

    ### Depart Seattle schedule code ends
    
    return render_template('schedule.html',
                           standard_schedule=standard_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           h2_1=h2_1,
                           h2_2=h2_2)

# Bainbridge Ferry Schedule route
@app.route('/bainbridge-seattle/')
def bainbridge_schedule():
    
    # Set special schedule variable to true
    # to indicate special schedule template
    special_schedule = True

    # Get worksheet with schedules
    ws = sheet.get_worksheet(2)

    # Set title tag variable
    title = ws.acell('B1').value
    
    # Set h1 tag variable
    h1 = ws.acell('B2').value

    # Set leadcopy variable
    leadcopy = ws.acell('B3').value

    # Set table headers for each schedule
    table_headers_1 = {ws.acell('E1').value:ws.acell('F1').value}
    table_headers_2 = {ws.acell('G1').value:ws.acell('H1').value}

    # Set H2 tags for each schedule
    h2_1 = ws.acell('B5').value
    h2_2 = ws.acell('B6').value

    # Set H3 tags for each schedule
    h3_1 = ws.acell('D1').value
    h3_2 = ws.acell('I1').value

    ### Depart Bainbridge schedule code begins

    # Get each schedule and delete header cells
    depart_bainbridge_weekday_schedule = ws.col_values(5)
    arrive_seattle_weekday_schedule = ws.col_values(6)
    del depart_bainbridge_weekday_schedule[0]
    del arrive_seattle_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_1 = dict(zip(depart_bainbridge_weekday_schedule, arrive_seattle_weekday_schedule))

    ### Depart Bainbridge schedule code ends

    ### Depart Seattle schedule code

    # Get each schedule and delete header cells
    depart_seattle_weekday_schedule = ws.col_values(7)
    arrive_bainbridge_weekday_schedule = ws.col_values(8)
    del depart_seattle_weekday_schedule[0]
    del arrive_bainbridge_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_2 = dict(zip(depart_seattle_weekday_schedule, arrive_bainbridge_weekday_schedule))

    # Get each schedule and delete header cells
    depart_bainbridge_weekend_schedule = ws.col_values(10)
    arrive_seattle_weekend_schedule = ws.col_values(11)
    del depart_bainbridge_weekend_schedule[0]
    del arrive_seattle_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_3 = dict(zip(depart_bainbridge_weekend_schedule, arrive_seattle_weekend_schedule))

    ### Depart Bremerton schedule code ends

    ### Depart Seattle schedule code

    # Get each schedule and delete header cells
    depart_seattle_weekend_schedule = ws.col_values(12)
    arrive_bainbridge_weekend_schedule = ws.col_values(13)
    del depart_seattle_weekend_schedule[0]
    del arrive_bainbridge_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_4 = dict(zip(depart_seattle_weekend_schedule, arrive_bainbridge_weekend_schedule))

    ### Depart Seattle schedule code ends
    
    return render_template('schedule.html',
                           special_schedule=special_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           times_3=times_3.items(),
                           times_4=times_4.items(),
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           h2_1=h2_1,
                           h2_2=h2_2,
                           h3_1=h3_1,
                           h3_2=h3_2)

# Staten Island Ferry schedule route
@app.route('/staten-island/')
def staten_island_schedule():
    return 'Staten Island'
    


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)