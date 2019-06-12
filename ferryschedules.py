from flask import Flask, render_template, url_for, jsonify, request
from flask_caching import Cache
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open_by_key('1sh4UaaL4ZVAIz4ffvYTeTo8se83rxGFaGbN4C2wjfAI')

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def navbar():
    
    # Create list of url routes
    wa_links_list = []
    ny_links_list = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            if str(rule).find('/wa/') is 0:
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                wa_links_list.append((url, rule.endpoint))
            elif str(rule).find('/ny/') is 0:
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                ny_links_list.append((url, rule.endpoint))
    
    # Sort list and then delete homepage from list
    wa_links_list.sort()
    #del links_list[0]
    ny_links_list.sort()

    # Convert list to dictionary
    wa_nav_links = dict(wa_links_list)
    ny_nav_links = dict(ny_links_list)

    # Modify the endpoints into pretty names
    for k, v in wa_nav_links.items():
        update_name = {k: v.title().replace('_',' ')}
        wa_nav_links.update(update_name)

    for k, v in ny_nav_links.items():
        update_name = {k: v.title().replace('_',' ')}
        ny_nav_links.update(update_name)

    # Delete state directory pages
    # We do not want them listed in the nav
    del ny_nav_links['/ny/']
    del wa_nav_links['/wa/']

    return ny_nav_links.items(), wa_nav_links.items()

def generate_breadcrumb():
    
    # Get path of the route
    url = request.path

    # Split each directory in the route
    split_url = url.split('/')

    # Filter out empty list items and grab first path in list
    path_extract = list(filter(None, split_url))[0]

    # Rebuild path for state page
    bc_path = "/" + path_extract + "/"

    # Create the anchor text for the State part of the breadcrumb
    bc_state_text = path_extract.upper()

    # Get the endpoint name
    endpoint = request.endpoint

    # Replace underscores with spaces in endpoint name and convert to title case
    bc_schedule_text = endpoint.title().replace('_',' ')

    return bc_path, bc_state_text, bc_schedule_text

@app.route('/')
def homepage():
    
    # Create instance of navbar()
    nav = navbar()
    
    homepage = True
    # Create list of url routes
    wa_links_list = []
    ny_links_list = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            if str(rule).find('/wa/') is 0:
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                wa_links_list.append((url, rule.endpoint))
            elif str(rule).find('/ny/') is 0:
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                ny_links_list.append((url, rule.endpoint))
    
    # Sort list and then delete homepage from list
    wa_links_list.sort()
    #del links_list[0]
    ny_links_list.sort()

    # Convert list to dictionary
    wa_links = dict(wa_links_list)
    ny_links = dict(ny_links_list)

    # Modify the endpoints into pretty names
    for k, v in wa_links.items():
        update_name = {k: v.title().replace('_',' ')}
        wa_links.update(update_name)

    for k, v in ny_links.items():
        update_name = {k: v.title().replace('_',' ')}
        ny_links.update(update_name)

    # Delete state directory pages from dict
    # We do not want them listed on the page
    del ny_links['/ny/']
    del wa_links['/wa/']
        
    return render_template('index.html',
                           homepage=homepage,
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ny_links=ny_links.items(),
                           wa_links=wa_links.items())

# New York directory page
@app.route('/ny/')
def new_york_ferry_schedules():
    
    # Create instance of navbar()
    nav = navbar()

    # Create instance of generate_breadcrumb()
    # bc = generate_breadcrumb()

    # Create empty list to store New York links
    ny_schedule_list = []

    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            if str(rule).find('/ny/') is 0:
                ny_url = url_for(rule.endpoint, **(rule.defaults or {}))
                ny_schedule_list.append((ny_url, rule.endpoint))

    ny_schedule_list.sort()

    ny_schedules = dict(ny_schedule_list)

    for key, value in ny_schedules.items():
        update_name = {key: value.title().replace('_',' ')}
        ny_schedules.update(update_name)

    del ny_schedules['/ny/']

    return render_template('ny.html',
                           ny_schedules=ny_schedules.items(),
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1])

# Washington directory page
@app.route('/wa/')
def washington_ferry_schedules():
    
    # Create instance of navbar()
    nav = navbar()

    # Create instance of generate_breadcrumb()
    # bc = generate_breadcrumb()

    # Create empty list to store New York links
    wa_schedule_list = []

    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            if str(rule).find('/wa/') is 0:
                wa_url = url_for(rule.endpoint, **(rule.defaults or {}))
                wa_schedule_list.append((wa_url, rule.endpoint))

    wa_schedule_list.sort()

    wa_schedules = dict(wa_schedule_list)

    for key, value in wa_schedules.items():
        update_name = {key: value.title().replace('_',' ')}
        wa_schedules.update(update_name)

    del wa_schedules['/wa/']

    return render_template('wa.html',
                           ny_schedules=wa_schedules.items(),
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1])

# Bremerton Ferry Schedule route
@app.route('/wa/bremerton-seattle/')
#@cache.cached(timeout=30)
def bremerton_ferry_schedule():

    # Set bremerton schedule variable to true
    # to indicate which template to use
    bremerton_schedule = True

    # Create instance of navbar()
    nav = navbar()

    # Generate breadcrumb for this route
    bc = generate_breadcrumb()

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
                           bremerton_schedule=bremerton_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           h2_1=h2_1,
                           h2_2=h2_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1])

# Bainbridge Ferry Schedule route
@app.route('/wa/bainbridge-island-seattle/')
#@cache.cached(timeout=30)
def bainbridge_island_ferry_schedule():
    
    # Set bainbridge schedule variable to true
    # to indicate which template to use
    bainbridge_schedule = True

    # Create instance of navbar()
    nav = navbar()
    
    # Generate breadcrumb for this route
    bc = generate_breadcrumb()

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
                           bainbridge_schedule=bainbridge_schedule,
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
                           h3_2=h3_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1])

# Anacortes Ferry schedule route
@app.route('/wa/anacortes/')
#@cache.cached(timeout=30)
def anacortes_ferry_schedule():
    
    # Set anacortes schedule variable to true
    # to indicate which template to use
    anacortes_schedule = True

    # Create instance of navbar()
    nav = navbar()
    
    # Generate breadcrumb for this route
    bc = generate_breadcrumb()

    # Get Anacortes schedule worksheet
    ws = sheet.get_worksheet(3)

    # Set title tag variable
    title = ws.acell('B1').value
    
    # Set h1 tag variable
    h1 = ws.acell('B2').value

    # Set leadcopy variable
    leadcopy = ws.acell('B3').value

    # Set H2 tags for each schedule
    h2_1 = ws.acell('B5').value
    h2_2 = ws.acell('B6').value

    # Initiate blank lists to store westbound schedules
    wb_schedule = []
    wb_temp_list = []
    wb_table_headers = []

    # Retrieve westbound schedule times
    wb_anacortes = ws.col_values(5)
    wb_lopez_island = ws.col_values(6)
    wb_shaw_island = ws.col_values(7)
    wb_orcas_island = ws.col_values(8)
    wb_san_juan = ws.col_values(9)
    wb_sidney_bc = ws.col_values(10)

    # Create list of westbound table headers
    wb_table_headers.extend([wb_anacortes[0],
                             wb_lopez_island[0],
                             wb_shaw_island[0],
                             wb_orcas_island[0],
                             wb_san_juan[0],
                             wb_sidney_bc[0]])

    # Remove table headers
    del wb_anacortes[0]
    del wb_lopez_island[0]
    del wb_shaw_island[0]
    del wb_orcas_island[0]
    del wb_san_juan[0]
    del wb_sidney_bc[0]

    # Set counter = 0
    c = 0

    # Create temp list for each westbound time row
    # Append temp list to schedule list
    while c < len(wb_anacortes):
        wb_temp_list = [wb_anacortes[c], wb_lopez_island[c], wb_shaw_island[c], wb_orcas_island[c], wb_san_juan[c], wb_sidney_bc[c]]
        wb_schedule.append(wb_temp_list)
        c += 1

    
    # Initiate empty eastbound schedule variables
    eb_schedule = []
    eb_temp_list = []
    eb_table_headers = []

    # Retrieve eastbound schedule times
    eb_sidney_bc = ws.col_values(12)
    eb_san_juan = ws.col_values(13)
    eb_orcas_island = ws.col_values(14)
    eb_shaw_island = ws.col_values(15)
    eb_lopez_island = ws.col_values(16)
    eb_anacortes = ws.col_values(17)
    
    # Create list of eastbound table headers
    eb_table_headers.extend([eb_sidney_bc[0],
                             eb_san_juan[0],
                             eb_orcas_island[0],
                             eb_shaw_island[0],
                             eb_lopez_island[0],
                             eb_anacortes[0]])

    # Remove eastbound table headers from each list
    del eb_sidney_bc[0]
    del eb_san_juan[0]
    del eb_orcas_island[0]
    del eb_shaw_island[0]
    del eb_lopez_island[0]
    del eb_anacortes[0]

    # Set counter variable
    c = 0

    # Create temp list for each eastbound time row
    # Append temp list to schedule list
    while c < len(eb_anacortes):
        eb_temp_list = [eb_sidney_bc[c], eb_san_juan[c], eb_orcas_island[c], eb_shaw_island[c], eb_lopez_island[c], eb_anacortes[c]]
        eb_schedule.append(eb_temp_list)
        c += 1

    return render_template('schedule.html',
                           anacortes_schedule=anacortes_schedule,
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           h2_1=h2_1,
                           h2_2=h2_2,
                           wb_table_headers=wb_table_headers,
                           eb_table_headers=eb_table_headers,
                           wb_schedule=wb_schedule,
                           eb_schedule=eb_schedule,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1])

# Kingston Ferry schedule route
@app.route('/wa/kingston-edmonds/')
#@cache.cached(timeout=30)
def kingston_ferry_schedule():
    # Set kingston schedule variable to true
    # to indicate which template to use
    kingston_schedule = True

    # Create instance of navbar()
    nav = navbar()
    
    # Generate breadcrumb for this route
    bc = generate_breadcrumb()
    
    # Get worksheet with schedules
    ws = sheet.get_worksheet(4)

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

    ### Depart Kingston schedule code begins

    # Get the cells for each schedule and delete header cell from list
    depart_kingston_schedule = ws.col_values(4)
    arrive_edmonds_schedule = ws.col_values(5)
    del depart_kingston_schedule[0]
    del arrive_edmonds_schedule[0]

    times_1 = dict(zip(depart_kingston_schedule, arrive_edmonds_schedule))

    ### Depart Kingston schedule code ends

    ### Depart Edmonds schedule code begins
    
    # Get the cells for each schedule
    depart_edmonds_schedule = ws.col_values(7)
    arrive_kingston_schedule = ws.col_values(8)
    del depart_edmonds_schedule[0]
    del arrive_kingston_schedule[0]

    # Convert schedule columns into a single dictionary
    times_2 = dict(zip(depart_edmonds_schedule, arrive_kingston_schedule))

    ### Depart Edmonds schedule code ends
    
    return render_template('schedule.html',
                           kingston_schedule=kingston_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           h2_1=h2_1,
                           h2_2=h2_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1])

# Staten Island Ferry Schedule route
@app.route('/ny/staten-island/')
#@cache.cached(timeout=30)
def staten_island_ferry_schedule():
    
    # Set bainbridge schedule variable to true
    # to indicate which template to use
    staten_island_schedule = True

    # Create instance of navbar()
    nav = navbar()

    # Generate breadcrumb for this route
    bc = generate_breadcrumb()

    # Get worksheet with schedules
    ws = sheet.get_worksheet(5)

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

    ### Depart Staten Island weekday schedule code begins

    # Get each schedule and delete header cells
    depart_si_weekday_schedule = ws.col_values(5)
    arrive_manhattan_weekday_schedule = ws.col_values(6)
    del depart_si_weekday_schedule[0]
    del arrive_manhattan_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_1 = dict(zip(depart_si_weekday_schedule, arrive_manhattan_weekday_schedule))

    ### Depart Staten Island weekday schedule code ends

    ### Depart Manhattan weekday schedule code

    # Get each schedule and delete header cells
    depart_manhattan_weekday_schedule = ws.col_values(7)
    arrive_si_weekday_schedule = ws.col_values(8)
    del depart_manhattan_weekday_schedule[0]
    del arrive_si_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_2 = dict(zip(depart_manhattan_weekday_schedule, arrive_si_weekday_schedule))

    ### Depart Manhattan weekday schedule code ends

    ### Depart Staten Island Weekend schedule code begins 
    # Get each schedule and delete header cells
    depart_si_weekend_schedule = ws.col_values(10)
    arrive_manhattan_weekend_schedule = ws.col_values(11)
    del depart_si_weekend_schedule[0]
    del arrive_manhattan_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_3 = dict(zip(depart_si_weekend_schedule, arrive_manhattan_weekend_schedule))

    ### Depart Staten Island Weekday schedule code ends

    ### Depart Manhattan weekend schedule code begins

    # Get each schedule and delete header cells
    depart_manhattan_weekend_schedule = ws.col_values(12)
    arrive_si_weekend_schedule = ws.col_values(13)
    del depart_manhattan_weekend_schedule[0]
    del arrive_si_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_4 = dict(zip(depart_manhattan_weekend_schedule, arrive_si_weekend_schedule))

    ### Depart Manhattan weekend schedule code ends
    
    return render_template('schedule.html',
                           staten_island_schedule=staten_island_schedule,
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
                           h3_2=h3_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)