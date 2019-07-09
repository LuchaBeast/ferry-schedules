from flask import Flask, render_template, url_for, jsonify, request
#from flask_caching import Cache
from oauth2client.service_account import ServiceAccountCredentials
import string
import gspread
import pendulum
#import pylibmc
import bmemcached
import os

app = Flask(__name__)
# cache = Cache()

# cache_servers = os.environ.get('MEMCACHIER_SERVERS')
# if cache_servers == None:
#     cache.init_app(app, config={'CACHE_TYPE': 'simple'})
# else:
#     cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
#     cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
#     cache.init_app(app,
#         config={'CACHE_TYPE': 'saslmemcached',
#                 'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
#                 'CACHE_MEMCACHED_USERNAME': cache_user,
#                 'CACHE_MEMCACHED_PASSWORD': cache_pass,
#                 'CACHE_OPTIONS': { 'behaviors': {
#                     # Faster IO
#                     'tcp_nodelay': True,
#                     # Keep connection alive
#                     'tcp_keepalive': True,
#                     # Timeout for set/get requests
#                     'connect_timeout': 2000, # ms
#                     'send_timeout': 750 * 1000, # us
#                     'receive_timeout': 750 * 1000, # us
#                     '_poll_timeout': 2000, # ms
#                     # Better failover
#                     'ketama': True,
#                     'remove_failed': 1,
#                     'retry_timeout': 2,
#                     'dead_timeout': 30}}})

# servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
# user = os.environ.get('MEMCACHIER_USERNAME', '')
# passw = os.environ.get('MEMCACHIER_PASSWORD', '')

# mc = pylibmc.Client(servers, binary=True,
#                     username=user, password=passw,
#                     behaviors={
#                       # Faster IO
#                       'tcp_nodelay': True,

#                       # Keep connection alive
#                       'tcp_keepalive': True,

#                       # Timeout for set/get requests
#                       'connect_timeout': 2000, # ms
#                       'send_timeout': 750 * 1000, # us
#                       'receive_timeout': 750 * 1000, # us
#                       '_poll_timeout': 2000, # ms

#                       # Better failover
#                       'ketama': True,
#                       'remove_failed': 1,
#                       'retry_timeout': 2,
#                       'dead_timeout': 30,
#                     })

servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
user = os.environ.get('MEMCACHIER_USERNAME', '')
passw = os.environ.get('MEMCACHIER_PASSWORD', '')

cache = bmemcached.Client(servers, username=user, password=passw)

cache.enable_retry_delay(True)  # Enabled by default. Sets retry delay to 5s.

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ferryschedules/ferry-schedules/client_secret.json',
                                                         scope)
client = gspread.authorize(creds)

sheet = client.open_by_key('1sh4UaaL4ZVAIz4ffvYTeTo8se83rxGFaGbN4C2wjfAI')


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def navbar():

    # Refresh access token
    if creds.access_token_expired:
        client.login()

    # Create list of url routes
    ca_links_list = []
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
            elif str(rule).find('/ca/') is 0:
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                ca_links_list.append((url, rule.endpoint))

    # Sort list and then delete homepage from list
    ca_links_list.sort()
    wa_links_list.sort()
    ny_links_list.sort()

    # Convert list to dictionary
    ca_nav_links = dict(ca_links_list)
    wa_nav_links = dict(wa_links_list)
    ny_nav_links = dict(ny_links_list)

    # Modify the endpoints into pretty names
    for k, v in ca_nav_links.items():
        update_name = {k: v.title().replace('_', ' ')}
        ca_nav_links.update(update_name)

    for k, v in wa_nav_links.items():
        update_name = {k: v.title().replace('_', ' ')}
        wa_nav_links.update(update_name)

    for k, v in ny_nav_links.items():
        update_name = {k: v.title().replace('_', ' ')}
        ny_nav_links.update(update_name)

    # Delete state directory pages
    # We do not want them listed in the nav
    del ca_nav_links['/ca/']
    del ny_nav_links['/ny/']
    del wa_nav_links['/wa/']

    return ny_nav_links.items(), wa_nav_links.items(), ca_nav_links.items()


def generate_breadcrumb():

    # Get path of the route
    url = request.path

    # Split each directory in the route
    split_url = url.split('/')

    # Filter out empty list items
    # Retrieve state path from list
    path_extract = list(filter(None, split_url))[0]

    # Rebuild path for state page
    bc_path = "/" + path_extract + "/"

    # Create the anchor text for the State part of the breadcrumb
    bc_state_text = path_extract.upper()

    # Get the endpoint name
    endpoint = request.endpoint

    # Replace underscores with spaces in endpoint name
    # Then convert to title case
    bc_schedule_text = endpoint.title().replace('_', ' ')

    return bc_path, bc_state_text, bc_schedule_text


@app.route('/')
def homepage():

    # Create instance of navbar()
    nav = navbar()

    homepage = True
    # Create list of url routes
    ca_links_list = []
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
            elif str(rule).find('/ca/') is 0:
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                ca_links_list.append((url, rule.endpoint))

    # Sort lists
    ca_links_list.sort()
    wa_links_list.sort()
    ny_links_list.sort()

    # Convert lists to dictionaries
    ca_links = dict(ca_links_list)
    wa_links = dict(wa_links_list)
    ny_links = dict(ny_links_list)

    # Modify the endpoints into pretty names
    for k, v in ca_links.items():
        update_name = {k: v.title().replace('_', ' ')}
        ca_links.update(update_name)

    for k, v in wa_links.items():
        update_name = {k: v.title().replace('_', ' ')}
        wa_links.update(update_name)

    for k, v in ny_links.items():
        update_name = {k: v.title().replace('_', ' ')}
        ny_links.update(update_name)

    # Delete state directory pages from dict
    # We do not want them listed on the page
    del ca_links['/ca/']
    del ny_links['/ny/']
    del wa_links['/wa/']

    return render_template('index.html',
                           homepage=homepage,
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2],
                           ca_links=ca_links.items(),
                           ny_links=ny_links.items(),
                           wa_links=wa_links.items())


# California directory page
@app.route('/ca/')
def california_ferry_schedules():

    # Create instance of navbar()
    nav = navbar()

    california = True

    # Create instance of generate_breadcrumb()
    bc = generate_breadcrumb()

    # Create empty list to store California links
    ca_schedule_list = []

    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            if str(rule).find('/ca/') is 0:
                ca_url = url_for(rule.endpoint, **(rule.defaults or {}))
                ca_schedule_list.append((ca_url, rule.endpoint))

    ca_schedule_list.sort()

    ca_schedules = dict(ca_schedule_list)

    for key, value in ca_schedules.items():
        update_name = {key: value.title().replace('_', ' ')}
        ca_schedules.update(update_name)

    del ca_schedules['/ca/']

    return render_template('ca.html',
                           california=california,
                           ca_schedules=ca_schedules.items(),
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2],
                           bc_state_text=bc[1])


# New York directory page
@app.route('/ny/')
def new_york_ferry_schedules():

    # Create instance of navbar()
    nav = navbar()

    new_york = True

    # Create instance of generate_breadcrumb()
    bc = generate_breadcrumb()

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
        update_name = {key: value.title().replace('_', ' ')}
        ny_schedules.update(update_name)

    del ny_schedules['/ny/']

    return render_template('ny.html',
                           new_york=new_york,
                           ny_schedules=ny_schedules.items(),
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2],
                           bc_state_text=bc[1])


# Washington directory page
@app.route('/wa/')
def washington_ferry_schedules():

    # Create instance of navbar()
    nav = navbar()

    washington = True

    # Create instance of generate_breadcrumb()
    bc = generate_breadcrumb()

    # Create empty list to store Washington links
    wa_schedule_list = []

    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            if str(rule).find('/wa/') is 0:
                wa_url = url_for(rule.endpoint, **(rule.defaults or {}))
                wa_schedule_list.append((wa_url, rule.endpoint))

    wa_schedule_list.sort()

    wa_schedules = dict(wa_schedule_list)

    for key, value in wa_schedules.items():
        update_name = {key: value.title().replace('_', ' ')}
        wa_schedules.update(update_name)

    del wa_schedules['/wa/']

    return render_template('wa.html',
                           washington=washington,
                           wa_schedules=wa_schedules.items(),
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2],
                           bc_state_text=bc[1])


# Bremerton Ferry Schedule route
@app.route('/wa/bremerton-seattle/')
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
    title = cache.get('cached_bremerton_title')
    if title == None:
        title = ws.acell('B1').value
        cache.set('cached_bremerton_title', title)

    # Set h1 tag variable
    h1 = cache.get('cached_bremerton_h1')
    if h1 == None:
        h1 = ws.acell('B2').value
        cache.set('cached_bremerton_h1', h1)

    # Set leadcopy variable
    leadcopy = cache.get('cached_bremerton_leadcopy')
    if leadcopy == None:
        leadcopy = ws.acell('B3').value
        cache.set('cached_bremerton_leadcopy', leadcopy)

    # Set table headers for each schedule
    table_headers_1 = cache.get('cached_bremerton_table_headers_1')
    if table_headers_1 == None:
        table_headers_1 = {ws.acell('D1').value: ws.acell('E1').value}
        cache.set('cached_bremerton_table_headers_1', table_headers_1)
    table_headers_2 = cache.get('cached_bremerton_table_headers_2')
    if table_headers_2 == None:
        table_headers_2 = {ws.acell('G1').value: ws.acell('H1').value}
        cache.set('cached_bremerton_table_headers_2', table_headers_2)

    # Set container headers
    th_1 = cache.get('cached_bremerton_th_1')
    if th_1 == None:
        th_1 = ws.acell('B5').value
        cache.set('cached_bremerton_th_1', th_1)
    
    th_2 = cache.get('cached_bremerton_th_2')
    if th_2 == None:
        th_2 = ws.acell('B6').value
        cache.set('cached_bremerton_th_2', th_2)

    # Set next departure card headers
    ndh_1 = cache.get('cached_bremerton_ndh_1')
    if ndh_1 == None:
        ndh_1 = ws.acell('B7').value
        cache.set('cached_bremerton_ndh_1', ndh_1)
    ndh_2 = cache.get('cached_bremerton_ndh_2')
    if ndh_2 == None:
        ndh_2 = ws.acell('B8').value
        cache.set('cached_bremerton_ndh_2', ndh_2)

    # ***Depart Bremerton schedule code begins***

    # Get the cells for each schedule and delete header cell from list
    departure_schedule_1 = cache.get('cached_departure_schedule_1')
    if departure_schedule_1 == None:
        departure_schedule_1 = ws.col_values(4)
        cache.set('cached_departure_schedule_1', departure_schedule_1)
    arrive_schedule_1 = cache.get('cached_arrive_schedule_1')
    if arrive_schedule_1 == None:
        arrive_schedule_1 = ws.col_values(5)
        cache.set('cached_arrive_schedule_1', arrive_schedule_1)

    del departure_schedule_1[0]
    del arrive_schedule_1[0]

    # Convert schedule lists into dictionary
    times_1 = dict(zip(departure_schedule_1, arrive_schedule_1))

    # ***Depart Bremerton schedule code ends***

    # ***Depart Seattle schedule code begins***

    # Get the cells for each schedule
    departure_schedule_2 = cache.get('cached_departure_schedule_2')
    if departure_schedule_2 == None:
        departure_schedule_2 = ws.col_values(7)
        cache.set('cached_departure_schedule_2', departure_schedule_2)
    arrive_schedule_2 = cache.get('cached_arrive_schedule_2')
    if arrive_schedule_2 == None:
        arrive_schedule_2 = ws.col_values(8)
        cache.set('cached_arrive_schedule_2', arrive_schedule_2)

    del departure_schedule_2[0]
    del arrive_schedule_2[0]

    # Convert schedule columns into a single dictionary
    times_2 = dict(zip(departure_schedule_2, arrive_schedule_2))

    # ***Depart Seattle schedule code ends***

    # Calculate next departure times
    # Retrieve current time in Seattle
    current_pacific_time = pendulum.now('America/Los_Angeles')

    # Set next Bremerton departure time
    # by comparing current time to each time in the schedule
    for departure in departure_schedule_1:
        format_time = pendulum.from_format(departure, 'h:mm A')\
                              .set(tz='America/Los_Angeles')
        if current_pacific_time < format_time:
            next_departure_1 = departure
            break

    # Set next Seattle departure time
    # by comparing current time to each time in the schedule
    for departure in departure_schedule_2:
        format_time = pendulum.from_format(departure, 'h:mm A')\
                              .set(tz='America/Los_Angeles')
        if current_pacific_time < format_time:
            next_departure_2 = departure
            break

    return render_template('schedule.html',
                           bremerton_schedule=bremerton_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           next_departure_1=next_departure_1,
                           next_departure_2=next_departure_2,
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           th_1=th_1,
                           th_2=th_2,
                           ndh_1=ndh_1,
                           ndh_2=ndh_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2])


# Bainbridge Ferry Schedule route
@app.route('/wa/bainbridge-island-seattle/')
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
    title = cache.get('cached_bainbridge_title')
    if title == None:
        title = ws.acell('B1').value
        cache.set('cached_bainbridge_title', title)

    # Set h1 tag variable
    h1 = cache.get('cached_bainbridge_h1')
    if h1 == None:
        h1 = ws.acell('B2').value
        cache.set('cached_bainbridge_h1', h1)

    # Set leadcopy variable
    leadcopy = cache.get('cached_bainbridge_leadcopy')
    if leadcopy == None:
        leadcopy = ws.acell('B3').value
        cache.set('cached_bainbridge_leadcopy', leadcopy)

    # Set table headers for each schedule
    table_headers_1 = cache.get('cached_bainbridge_table_headers_1')
    if table_headers_1 == None:
        table_headers_1 = {ws.acell('D1').value: ws.acell('E1').value}
        cache.set('cached_bainbridge_table_headers_1', table_headers_1)
    table_headers_2 = cache.get('cached_bainbridge_table_headers_2')
    if table_headers_2 == None:
        table_headers_2 = {ws.acell('G1').value: ws.acell('H1').value}
        cache.set('cached_bainbridge_table_headers_2', table_headers_2)

    # Set container headers
    th_1 = cache.get('cached_bainbridge_th_1')
    if th_1 == None:
        th_1 = ws.acell('B5').value
        cache.set('cached_bainbridge_th_1', th_1)
    
    th_2 = cache.get('cached_bainbridge_th_2')
    if th_2 == None:
        th_2 = ws.acell('B6').value
        cache.set('cached_bainbridge_th_2', th_2)

    # Set next departure card headers
    ndh_1 = cache.get('cached_bainbridge_ndh_1')
    if ndh_1 == None:
        ndh_1 = ws.acell('B7').value
        cache.set('cached_bainbridge_ndh_1', ndh_1)
    ndh_2 = cache.get('cached_bainbridge_ndh_2')
    if ndh_2 == None:
        ndh_2 = ws.acell('B8').value
        cache.set('cached_bainbridge_ndh_2', ndh_2)

    # Set H3 tags for each schedule
    h3_1 = cache.get('cached_bainbridge_h3_1')
    if h3_1 == None:
        h3_1 = ws.acell('D1').value
        cache.set('cached_bainbridge_h3_1', h3_1)
    h3_2 = cache.get('cached_bainbridge_h3_2')
    if h3_2 == None:
        h3_2 = ws.acell('I1').value
        cache.set('cached_bainbridge_h3_2', h3_2)

    # ***Depart Bainbridge weekday schedule code begins***

    # Get each schedule and delete header cells
    depart_bainbridge_weekday_schedule = cache.get('cached_depart_bainbridge_weekday_schedule')
    if depart_bainbridge_weekday_schedule == None:
        depart_bainbridge_weekday_schedule = ws.col_values(5)
        cache.set('cached_depart_bainbridge_weekday_schedule', depart_bainbridge_weekday_schedule)
    
    arrive_seattle_weekday_schedule = cache.get('cached_arrive_seattle_weekday_schedule')
    if arrive_seattle_weekday_schedule == None:
        arrive_seattle_weekday_schedule = ws.col_values(6)
        cache.set('cached_arrive_seattle_weekday_schedule', arrive_seattle_weekday_schedule)
    del depart_bainbridge_weekday_schedule[0]
    del arrive_seattle_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_1 = dict(zip(depart_bainbridge_weekday_schedule,
                       arrive_seattle_weekday_schedule))

    # ***Depart Bainbridge weekday schedule code ends***

    # ***Depart Seattle weekday schedule code begins***

    # Get each schedule and delete header cells
    depart_seattle_weekday_schedule = cache.get('cached_depart_seattle_weekday_schedule')
    if depart_seattle_weekday_schedule == None:
        depart_seattle_weekday_schedule = ws.col_values(7)
        cache.set('cached_depart_seattle_weekday_schedule', depart_seattle_weekday_schedule)
    
    arrive_bainbridge_weekday_schedule = cache.get('cached_arrive_bainbridge_weekday_schedule')
    if arrive_bainbridge_weekday_schedule == None:
        arrive_bainbridge_weekday_schedule = ws.col_values(8)
        cache.set('cached_arrive_bainbridge_weekday_schedule', arrive_bainbridge_weekday_schedule)
    del depart_seattle_weekday_schedule[0]
    del arrive_bainbridge_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_2 = dict(zip(depart_seattle_weekday_schedule,
                       arrive_bainbridge_weekday_schedule))

    # ***Depart seattle weekday schedule code ends***

    # ***Depart bainbridge weekend schedule code begins***

    # Get each schedule and delete header cells
    depart_bainbridge_weekend_schedule = cache.get('cached_depart_bainbridge_weekend_schedule')
    if depart_bainbridge_weekend_schedule == None:
        depart_bainbridge_weekend_schedule = ws.col_values(10)
        cache.set('cached_depart_bainbridge_weekend_schedule', depart_bainbridge_weekend_schedule)
    
    arrive_seattle_weekend_schedule = cache.get('cached_arrive_seattle_weekend_schedule')
    if arrive_seattle_weekend_schedule == None:
        arrive_seattle_weekend_schedule = ws.col_values(11)
        cache.set('cached_arrive_seattle_weekend_schedule', arrive_seattle_weekend_schedule)
    del depart_bainbridge_weekend_schedule[0]
    del arrive_seattle_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_3 = dict(zip(depart_bainbridge_weekend_schedule,
                       arrive_seattle_weekend_schedule))

    # ***Depart bainbridge weekend schedule code ends***

    # ***Depart Seattle weekend schedule code begins***

    # Get each schedule and delete header cells
    depart_seattle_weekend_schedule = cache.get('cached_depart_seattle_weekend_schedule')
    if depart_seattle_weekend_schedule == None:
        depart_seattle_weekend_schedule = ws.col_values(12)
        cache.set('cached_depart_seattle_weekend_schedule', depart_seattle_weekend_schedule)
    
    arrive_bainbridge_weekend_schedule = cache.get('cached_arrive_bainbridge_weekend_schedule')
    if arrive_bainbridge_weekend_schedule == None:
        arrive_bainbridge_weekend_schedule = ws.col_values(13)
        cache.set('cached_arrive_bainbridge_weekend_schedule', arrive_bainbridge_weekend_schedule)
    del depart_seattle_weekend_schedule[0]
    del arrive_bainbridge_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_4 = dict(zip(depart_seattle_weekend_schedule,
                       arrive_bainbridge_weekend_schedule))

    # ***Depart Seattle weekend schedule code ends***

    # Calculate next departures
    # Retrieve current time in Seattle
    current_pacific_time = pendulum.now('America/Los_Angeles')
    current_day = current_pacific_time.day_of_week

    # Check whether weekday or weekend and calculate Bainbridge next departures
    if current_day >= 1 and current_day <= 5:
        for departure in depart_bainbridge_weekday_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_1 = departure
                break
    else:
        for departure in depart_bainbridge_weekend_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_1 = departure
                break

    # Check whether weekday or weekend and calculate Seattle next departures
    if current_day >= 1 and current_day <= 5:
        for departure in depart_seattle_weekday_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_2 = departure
                break
    else:
        for departure in depart_seattle_weekend_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_2 = departure
                break

    return render_template('schedule.html',
                           bainbridge_schedule=bainbridge_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           times_3=times_3.items(),
                           times_4=times_4.items(),
                           next_departure_1=next_departure_1,
                           next_departure_2=next_departure_2,
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           th_1=th_1,
                           th_2=th_2,
                           ndh_1=ndh_1,
                           ndh_2=ndh_2,
                           h3_1=h3_1,
                           h3_2=h3_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2])


# Anacortes Ferry schedule route
@app.route('/wa/anacortes/')
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
    th_1 = ws.acell('B5').value
    th_2 = ws.acell('B6').value

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
        wb_temp_list = [wb_anacortes[c],
                        wb_lopez_island[c],
                        wb_shaw_island[c],
                        wb_orcas_island[c],
                        wb_san_juan[c],
                        wb_sidney_bc[c]]

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
        eb_temp_list = [eb_sidney_bc[c],
                        eb_san_juan[c],
                        eb_orcas_island[c],
                        eb_shaw_island[c],
                        eb_lopez_island[c],
                        eb_anacortes[c]]

        eb_schedule.append(eb_temp_list)
        c += 1

    return render_template('schedule.html',
                           anacortes_schedule=anacortes_schedule,
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           th_1=th_1,
                           th_2=th_2,
                           wb_table_headers=wb_table_headers,
                           eb_table_headers=eb_table_headers,
                           wb_schedule=wb_schedule,
                           eb_schedule=eb_schedule,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2])


# Kingston Ferry schedule route
@app.route('/wa/kingston-edmonds/')
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
    title = cache.get('cached_kingston_title')
    if title == None:
        title = ws.acell('B1').value
        cache.set('cached_kingston_title', title)

    # Set h1 tag variable
    h1 = cache.get('cached_kingston_h1')
    if h1 == None:
        h1 = ws.acell('B2').value
        cache.set('cached_kingston_h1', h1)

    # Set leadcopy variable
    leadcopy = cache.get('cached_kingston_leadcopy')
    if leadcopy == None:
        leadcopy = ws.acell('B3').value
        cache.set('cached_kingston_leadcopy', leadcopy)

    # Set table headers for each schedule
    table_headers_1 = cache.get('cached_kingston_table_headers_1')
    if table_headers_1 == None:
        table_headers_1 = {ws.acell('D1').value: ws.acell('E1').value}
        cache.set('cached_kingston_table_headers_1', table_headers_1)
    table_headers_2 = cache.get('cached_kingston_table_headers_2')
    if table_headers_2 == None:
        table_headers_2 = {ws.acell('G1').value: ws.acell('H1').value}
        cache.set('cached_kingston_table_headers_2', table_headers_2)

    # Set container headers
    th_1 = cache.get('cached_kingston_th_1')
    if th_1 == None:
        th_1 = ws.acell('B5').value
        cache.set('cached_kingston_th_1', th_1)
    
    th_2 = cache.get('cached_kingston_th_2')
    if th_2 == None:
        th_2 = ws.acell('B6').value
        cache.set('cached_kingston_th_2', th_2)

    # Set next departure card headers
    ndh_1 = cache.get('cached_kingston_ndh_1')
    if ndh_1 == None:
        ndh_1 = ws.acell('B7').value
        cache.set('cached_kingston_ndh_1', ndh_1)
    ndh_2 = cache.get('cached_kingston_ndh_2')
    if ndh_2 == None:
        ndh_2 = ws.acell('B8').value
        cache.set('cached_kingston_ndh_2', ndh_2)

    # ***Depart Kingston schedule code begins***

    # Get the cells for each schedule and delete header cell from list
    depart_kingston_schedule = cache.get('cached_depart_kingston_schedule')
    if depart_kingston_schedule == None:
        depart_kingston_schedule = ws.col_values(4)
        cache.set('cached_depart_kingston_schedule', depart_kingston_schedule)

    arrive_edmonds_schedule = cache.get('cached_arrive_edmonds_schedule')
    if arrive_edmonds_schedule == None:
        arrive_edmonds_schedule = ws.col_values(5)
        cache.set('cached_arrive_edmonds_schedule', arrive_edmonds_schedule)

    del depart_kingston_schedule[0]
    del arrive_edmonds_schedule[0]

    times_1 = dict(zip(depart_kingston_schedule, arrive_edmonds_schedule))

    # ***Depart Kingston schedule code ends***

    # ***Depart Edmonds schedule code begins***

    # Get the cells for each schedule
    depart_edmonds_schedule = cache.get('cached_depart_edmonds_schedule')
    if depart_edmonds_schedule == None:
        depart_edmonds_schedule = ws.col_values(7)
        cache.set('cached_depart_edmonds_schedule', depart_edmonds_schedule)

    arrive_kingston_schedule = cache.get('cached_arrive_kingston_schedule')
    if arrive_kingston_schedule == None:
        arrive_kingston_schedule = ws.col_values(8)
        cache.set('cached_arrive_kingston_schedule', arrive_kingston_schedule)

    del depart_edmonds_schedule[0]
    del arrive_kingston_schedule[0]

    # Convert schedule columns into a single dictionary
    times_2 = dict(zip(depart_edmonds_schedule, arrive_kingston_schedule))

    # ***Depart Edmonds schedule code ends***

    # Calculate next departure times
    # Retrieve current time in Seattle
    current_pacific_time = pendulum.now('America/Los_Angeles')

    # Set next Kingston departure time
    # by comparing current time to each time in the schedule
    for departure in depart_kingston_schedule:
        format_time = pendulum.from_format(departure, 'h:mm A')\
                              .set(tz='America/Los_Angeles')
        if current_pacific_time < format_time:
            next_departure_1 = departure
            break

    # Set next Edmonds departure time
    # by comparing current time to each time in the schedule
    for departure in depart_edmonds_schedule:
        format_time = pendulum.from_format(departure, 'h:mm A')\
                              .set(tz='America/Los_Angeles')
        if current_pacific_time < format_time:
            next_departure_2 = departure
            break

    return render_template('schedule.html',
                           kingston_schedule=kingston_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           next_departure_1=next_departure_1,
                           next_departure_2=next_departure_2,
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           ndh_1=ndh_1,
                           ndh_2=ndh_2,
                           th_1=th_1,
                           th_2=th_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2])


@app.route('/wa/southworth-vashon/')
def southworth_ferry_schedule():
    # Set southworth schedule variable to true
    # to indicate which template to use
    southworth_schedule = True

    # Create instance of navbar()
    nav = navbar()

    # Generate breadcrumb for this route
    bc = generate_breadcrumb()

    # Get worksheet with schedules
    ws = sheet.get_worksheet(7)

    # Set title tag variable
    title = cache.get('cached_southworth_title')
    if title == None:
        title = ws.acell('B1').value
        cache.set('cached_southworth_title', title)

    # Set h1 tag variable
    h1 = cache.get('cached_southworth_h1')
    if h1 == None:
        h1 = ws.acell('B2').value
        cache.set('cached_southworth_h1', h1)

    # Set leadcopy variable
    leadcopy = cache.get('cached_southworth_leadcopy')
    if leadcopy == None:
        leadcopy = ws.acell('B3').value
        cache.set('cached_southworth_leadcopy', leadcopy)

    # Set table headers for each schedule
    table_headers_1 = cache.get('cached_southworth_table_headers_1')
    if table_headers_1 == None:
        table_headers_1 = {ws.acell('D1').value: ws.acell('E1').value}
        cache.set('cached_southworth_table_headers_1', table_headers_1)
    table_headers_2 = cache.get('cached_southworth_table_headers_2')
    if table_headers_2 == None:
        table_headers_2 = {ws.acell('G1').value: ws.acell('H1').value}
        cache.set('cached_southworth_table_headers_2', table_headers_2)

    # Set container headers
    th_1 = cache.get('cached_southworth_th_1')
    if th_1 == None:
        th_1 = ws.acell('B5').value
        cache.set('cached_southworth_th_1', th_1)
    
    th_2 = cache.get('cached_southworth_th_2')
    if th_2 == None:
        th_2 = ws.acell('B6').value
        cache.set('cached_southworth_th_2', th_2)

    # Set next departure card headers
    ndh_1 = cache.get('cached_southworth_ndh_1')
    if ndh_1 == None:
        ndh_1 = ws.acell('B7').value
        cache.set('cached_southworth_ndh_1', ndh_1)
    ndh_2 = cache.get('cached_southworth_ndh_2')
    if ndh_2 == None:
        ndh_2 = ws.acell('B8').value
        cache.set('cached_southworth_ndh_2', ndh_2)

    # Set H3 tags for each schedule
    h3_1 = cache.get('cached_southworth_h3_1')
    if h3_1 == None:
        h3_1 = ws.acell('D1').value
        cache.set('cached_southworth_h3_1', h3_1)
    h3_2 = cache.get('cached_southworth_h3_2')
    if h3_2 == None:
        h3_2 = ws.acell('I1').value
        cache.set('cached_southworth_h3_2', h3_2)

    # ***Depart Southworth weekday schedule code begins***

    # Get each schedule and delete header cells
    depart_southworth_weekday_schedule = cache.get('cached_depart_southworth_weekday_schedule')
    if depart_southworth_weekday_schedule == None:
        depart_southworth_weekday_schedule = ws.col_values(5)
        cache.set('cached_depart_southworth_weekday_schedule', depart_southworth_weekday_schedule)
    arrive_vashon_weekday_schedule = cache.get('cached_arrive_vashon_weekday_schedule')
    if arrive_vashon_weekday_schedule == None:
        arrive_vashon_weekday_schedule = ws.col_values(6)
        cache.set('cached_arrive_vashon_weekday_schedule', arrive_vashon_weekday_schedule)
    del depart_southworth_weekday_schedule[0]
    del arrive_vashon_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_1 = dict(zip(depart_southworth_weekday_schedule,
                       arrive_vashon_weekday_schedule))

    # ***Depart southworth weekday schedule code ends***

    # ***Depart vashon weekday schedule code begins***

    # Get each schedule and delete header cells
    depart_vashon_weekday_schedule = cache.get('cached_depart_vashon_weekday_schedule')
    if depart_vashon_weekday_schedule == None:
        depart_vashon_weekday_schedule = ws.col_values(7)
        cache.set('cached_depart_vashon_weekday_schedule', depart_vashon_weekday_schedule)
    arrive_southworth_weekday_schedule = cache.get('cached_arrive_southworth_weekday_schedule')
    if arrive_southworth_weekday_schedule == None:
        arrive_southworth_weekday_schedule = ws.col_values(8)
        cache.set('cached_arrive_southworth_weekday_schedule', arrive_southworth_weekday_schedule)
    del depart_vashon_weekday_schedule[0]
    del arrive_southworth_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_2 = dict(zip(depart_vashon_weekday_schedule,
                       arrive_southworth_weekday_schedule))

    # ***Depart vashon weekday schedule code ends***

    # ***Depart southworth weekend schedule code begins***

    # Get each schedule and delete header cells
    depart_southworth_weekend_schedule = cache.get('cached_depart_southworth_weekend_schedule')
    if depart_southworth_weekend_schedule == None:
        depart_southworth_weekend_schedule = ws.col_values(10)
        cache.set('cached_depart_southworth_weekend_schedule', depart_southworth_weekend_schedule)
    arrive_vashon_weekend_schedule = cache.get('cached_arrive_vashon_weekend_schedule')
    if arrive_vashon_weekend_schedule == None:
        arrive_vashon_weekend_schedule = ws.col_values(11)
        cache.set('cached_arrive_vashon_weekend_schedule', arrive_vashon_weekend_schedule)
    del depart_southworth_weekend_schedule[0]
    del arrive_vashon_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_3 = dict(zip(depart_southworth_weekend_schedule,
                       arrive_vashon_weekend_schedule))

    # ***Depart southworth weekend schedule code ends***

    # ***Depart vashon weekend schedule code begins***

    # Get each schedule and delete header cells
    depart_vashon_weekend_schedule = cache.get('cached_depart_vashon_weekend_schedule')
    if depart_vashon_weekend_schedule == None:
        depart_vashon_weekend_schedule = ws.col_values(12)
        cache.set('cached_depart_vashon_weekend_schedule', depart_vashon_weekend_schedule)
    arrive_southworth_weekend_schedule = cache.get('cached_arrive_southworth_weekend_schedule')
    if arrive_southworth_weekend_schedule == None:
        arrive_southworth_weekend_schedule = ws.col_values(13)
        cache.set('cached_arrive_southworth_weekend_schedule', arrive_southworth_weekend_schedule)
    del depart_vashon_weekend_schedule[0]
    del arrive_southworth_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_4 = dict(zip(depart_vashon_weekend_schedule,
                       arrive_southworth_weekend_schedule))

    # ***Depart vashon weekend schedule code ends***

    # Calculate next departures
    # Retrieve current time in Seattle
    current_pacific_time = pendulum.now('America/Los_Angeles')
    current_day = current_pacific_time.day_of_week

    # Check whether weekday or weekend and calculate Bainbridge next departures
    if current_day >= 1 and current_day <= 5:
        for departure in depart_southworth_weekday_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_1 = departure
                break
    else:
        for departure in depart_southworth_weekend_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_1 = departure
                break

    # Check whether weekday or weekend and calculate Seattle next departures
    if current_day >= 1 and current_day <= 5:
        for departure in depart_vashon_weekday_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_2 = departure
                break
    else:
        for departure in depart_vashon_weekend_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_2 = departure
                break

    return render_template('schedule.html',
                           southworth_schedule=southworth_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           times_3=times_3.items(),
                           times_4=times_4.items(),
                           next_departure_1=next_departure_1,
                           next_departure_2=next_departure_2,
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           th_1=th_1,
                           th_2=th_2,
                           ndh_1=ndh_1,
                           ndh_2=ndh_2,
                           h3_1=h3_1,
                           h3_2=h3_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2])


# Staten Island Ferry Schedule route
@app.route('/ny/staten-island/')
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
    title = cache.get('cached_staten_island_title')
    if title == None:
        title = ws.acell('B1').value
        cache.set('cached_staten_island_title', title)

    # Set h1 tag variable
    h1 = cache.get('cached_staten_island_h1')
    if h1 == None:
        h1 = ws.acell('B2').value
        cache.set('cached_staten_island_h1', h1)

    # Set leadcopy variable
    leadcopy = cache.get('cached_staten_island_leadcopy')
    if leadcopy == None:
        leadcopy = ws.acell('B3').value
        cache.set('cached_staten_island_leadcopy', leadcopy)

    # Set table headers for each schedule
    table_headers_1 = cache.get('cached_staten_island_table_headers_1')
    if table_headers_1 == None:
        table_headers_1 = {ws.acell('D1').value: ws.acell('E1').value}
        cache.set('cached_staten_island_table_headers_1', table_headers_1)
    table_headers_2 = cache.get('cached_staten_island_table_headers_2')
    if table_headers_2 == None:
        table_headers_2 = {ws.acell('G1').value: ws.acell('H1').value}
        cache.set('cached_staten_island_table_headers_2', table_headers_2)

    # Set container headers
    th_1 = cache.get('cached_staten_island_th_1')
    if th_1 == None:
        th_1 = ws.acell('B5').value
        cache.set('cached_staten_island_th_1', th_1)
    
    th_2 = cache.get('cached_staten_island_th_2')
    if th_2 == None:
        th_2 = ws.acell('B6').value
        cache.set('cached_staten_island_th_2', th_2)

    # Set next departure card headers
    ndh_1 = cache.get('cached_staten_island_ndh_1')
    if ndh_1 == None:
        ndh_1 = ws.acell('B7').value
        cache.set('cached_staten_island_ndh_1', ndh_1)
    ndh_2 = cache.get('cached_staten_island_ndh_2')
    if ndh_2 == None:
        ndh_2 = ws.acell('B8').value
        cache.set('cached_staten_island_ndh_2', ndh_2)

    # Set H3 tags for each schedule
    h3_1 = cache.get('cached_staten_island_h3_1')
    if h3_1 == None:
        h3_1 = ws.acell('D1').value
        cache.set('cached_staten_island_h3_1', h3_1)
    h3_2 = cache.get('cached_staten_island_h3_2')
    if h3_2 == None:
        h3_2 = ws.acell('I1').value
        cache.set('cached_staten_island_h3_2', h3_2)

    # ***Depart Staten Island weekday schedule code begins***

    # Get each schedule and delete header cells
    depart_si_weekday_schedule = cache.get('cached_depart_si_weekday_schedule')
    if depart_si_weekday_schedule == None:
        depart_si_weekday_schedule = ws.col_values(5)
        cache.set('cached_depart_si_weekday_schedule', depart_si_weekday_schedule)
    arrive_manhattan_weekday_schedule = cache.get('cached_arrive_manhattan_weekday_schedule')
    if arrive_manhattan_weekday_schedule == None:
        arrive_manhattan_weekday_schedule = ws.col_values(6)
        cache.set('arrive_manhattan_weekday_schedule', arrive_manhattan_weekday_schedule)
    del depart_si_weekday_schedule[0]
    del arrive_manhattan_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_1 = dict(zip(depart_si_weekday_schedule,
                       arrive_manhattan_weekday_schedule))

    # ***Depart Staten Island weekday schedule code ends***

    # ***Depart Manhattan weekday schedule code

    # Get each schedule and delete header cells
    depart_manhattan_weekday_schedule = cache.get('cached_depart_manhattan_weekday_schedule')
    if depart_manhattan_weekday_schedule == None:
        depart_manhattan_weekday_schedule = ws.col_values(7)
        cache.set('cached_depart_manhattan_weekday_schedule', depart_manhattan_weekday_schedule)
    arrive_si_weekday_schedule = cache.get('cached_arrive_si_weekday_schedule')
    if arrive_si_weekday_schedule == None:
        arrive_si_weekday_schedule = ws.col_values(8)
        cache.set('cached_arrive_si_weekday_schedule', arrive_si_weekday_schedule)
    del depart_manhattan_weekday_schedule[0]
    del arrive_si_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_2 = dict(zip(depart_manhattan_weekday_schedule,
                       arrive_si_weekday_schedule))

    # ***Depart Manhattan weekday schedule code ends***

    # ***Depart Staten Island Weekend schedule code begins***
    # Get each schedule and delete header cells
    depart_si_weekend_schedule = cache.get('cached_depart_si_weekend_schedule')
    if depart_si_weekend_schedule == None:
        depart_si_weekend_schedule = ws.col_values(10)
        cache.set('cached_depart_si_weekend_schedule', depart_si_weekend_schedule)
    arrive_manhattan_weekend_schedule = cache.get('cached_arrive_manhattan_weekend_schedule')
    if arrive_manhattan_weekend_schedule == None:
        arrive_manhattan_weekend_schedule = ws.col_values(11)
        cache.set('arrive_manhattan_weekend_schedule', arrive_manhattan_weekend_schedule)
    del depart_si_weekend_schedule[0]
    del arrive_manhattan_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_3 = dict(zip(depart_si_weekend_schedule,
                       arrive_manhattan_weekend_schedule))

    # ***Depart Staten Island Weekday schedule code ends***

    # ***Depart Manhattan weekend schedule code begins***

    # Get each schedule and delete header cells
    depart_manhattan_weekend_schedule = cache.get('cached_depart_manhattan_weekend_schedule')
    if depart_manhattan_weekend_schedule == None:
        depart_manhattan_weekend_schedule = ws.col_values(12)
        cache.set('cached_depart_manhattan_weekend_schedule', depart_manhattan_weekend_schedule)
    arrive_si_weekend_schedule = cache.get('cached_arrive_si_weekend_schedule')
    if arrive_si_weekend_schedule == None:
        arrive_si_weekend_schedule = ws.col_values(13)
        cache.set('cached_arrive_si_weekend_schedule', arrive_si_weekend_schedule)
    del depart_manhattan_weekend_schedule[0]
    del arrive_si_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_4 = dict(zip(depart_manhattan_weekend_schedule,
                       arrive_si_weekend_schedule))

    # ***Depart Manhattan weekend schedule code ends***

    # Calculate next departures
    # Retrieve current time in Seattle
    current_eastern_time = pendulum.now('America/New_York')
    current_day = current_eastern_time.day_of_week

    # Check whether weekday or weekend and calculate Bainbridge next departures
    if current_day >= 1 and current_day <= 5:
        for departure in depart_si_weekday_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/New_York')
            if current_eastern_time < format_time:
                next_departure_1 = departure
                break
    else:
        for departure in depart_si_weekend_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/New_York')
            if current_eastern_time < format_time:
                next_departure_1 = departure
                break

    # Check whether weekday or weekend and calculate Seattle next departures
    if current_day >= 1 and current_day <= 5:
        for departure in depart_manhattan_weekday_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/New_York')
            if current_eastern_time < format_time:
                next_departure_2 = departure
                break
    else:
        for departure in depart_manhattan_weekend_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/New_York')
            if current_eastern_time < format_time:
                next_departure_2 = departure
                break

    return render_template('schedule.html',
                           staten_island_schedule=staten_island_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           times_3=times_3.items(),
                           times_4=times_4.items(),
                           next_departure_1=next_departure_1,
                           next_departure_2=next_departure_2,
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           th_1=th_1,
                           th_2=th_2,
                           ndh_1=ndh_1,
                           ndh_2=ndh_2,
                           h3_1=h3_1,
                           h3_2=h3_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2])


# Larkspur Ferry Schedule route
@app.route('/ca/larkspur-sf/')
def larkspur_ferry_schedule():
    # Set bainbridge schedule variable to true
    # to indicate which template to use
    larkspur_schedule = True

    # Create instance of navbar()
    nav = navbar()

    # Generate breadcrumb for this route
    bc = generate_breadcrumb()

    # Get worksheet with schedules
    ws = sheet.get_worksheet(6)

    # Set title tag variable
    title = cache.get('cached_larkspur_title')
    if title == None:
        title = ws.acell('B1').value
        cache.set('cached_larkspur_title', title)

    # Set h1 tag variable
    h1 = cache.get('cached_larkspur_h1')
    if h1 == None:
        h1 = ws.acell('B2').value
        cache.set('cached_larkspur_h1', h1)

    # Set leadcopy variable
    leadcopy = cache.get('cached_larkspur_leadcopy')
    if leadcopy == None:
        leadcopy = ws.acell('B3').value
        cache.set('cached_larkspur_leadcopy', leadcopy)

    # Set table headers for each schedule
    table_headers_1 = cache.get('cached_larkspur_table_headers_1')
    if table_headers_1 == None:
        table_headers_1 = {ws.acell('D1').value: ws.acell('E1').value}
        cache.set('cached_larkspur_table_headers_1', table_headers_1)
    table_headers_2 = cache.get('cached_larkspur_table_headers_2')
    if table_headers_2 == None:
        table_headers_2 = {ws.acell('G1').value: ws.acell('H1').value}
        cache.set('cached_larkspur_table_headers_2', table_headers_2)

    # Set container headers
    th_1 = cache.get('cached_larkspur_th_1')
    if th_1 == None:
        th_1 = ws.acell('B5').value
        cache.set('cached_larkspur_th_1', th_1)
    
    th_2 = cache.get('cached_larkspur_th_2')
    if th_2 == None:
        th_2 = ws.acell('B6').value
        cache.set('cached_larkspur_th_2', th_2)

    # Set next departure card headers
    ndh_1 = cache.get('cached_larkspur_ndh_1')
    if ndh_1 == None:
        ndh_1 = ws.acell('B7').value
        cache.set('cached_larkspur_ndh_1', ndh_1)
    ndh_2 = cache.get('cached_larkspur_ndh_2')
    if ndh_2 == None:
        ndh_2 = ws.acell('B8').value
        cache.set('cached_larkspur_ndh_2', ndh_2)

    # Set H3 tags for each schedule
    h3_1 = cache.get('cached_larkspur_h3_1')
    if h3_1 == None:
        h3_1 = ws.acell('D1').value
        cache.set('cached_larkspur_h3_1', h3_1)
    h3_2 = cache.get('cached_larkspur_h3_2')
    if h3_2 == None:
        h3_2 = ws.acell('I1').value
        cache.set('cached_larkspur_h3_2', h3_2)

    # ***Depart Larkspur weekday schedule code begins***

    # Get each schedule and delete header cells
    depart_larkspur_weekday_schedule = cache.get('cached_larkspur_weekday_schedule')
    if depart_larkspur_weekday_schedule == None:
        depart_larkspur_weekday_schedule = ws.col_values(5)
        cache.set('cached_larkspur_weekday_schedule', depart_larkspur_weekday_schedule)
    arrive_sf_weekday_schedule = cache.get('cached_arrive_sf_weekday_schedule')
    if arrive_sf_weekday_schedule == None:
        arrive_sf_weekday_schedule = ws.col_values(6)
        cache.set('cached_arrive_sf_weekday_schedule', arrive_sf_weekday_schedule)
    del depart_larkspur_weekday_schedule[0]
    del arrive_sf_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_1 = dict(zip(depart_larkspur_weekday_schedule,
                       arrive_sf_weekday_schedule))

    # ***Depart Larkspur weekday schedule code ends***

    # ***Depart SF weekday schedule code begins***

    # Get each schedule and delete header cells
    depart_sf_weekday_schedule = cache.get('cached_depart_sf_weekday_schedule')
    if depart_sf_weekday_schedule == None:
        depart_sf_weekday_schedule = ws.col_values(7)
        cache.set('cached_depart_sf_weekday_schedule', depart_sf_weekday_schedule)
    arrive_larkspur_weekday_schedule = cache.get('cached_arrive_larkspur_weekday_schedule')
    if arrive_larkspur_weekday_schedule == None:
        arrive_larkspur_weekday_schedule = ws.col_values(8)
        cache.set('cached_arrive_larkspur_weekday_schedule', arrive_larkspur_weekday_schedule)
    del depart_sf_weekday_schedule[0]
    del arrive_larkspur_weekday_schedule[0]

    # Convert both lists into a single dictionary
    times_2 = dict(zip(depart_sf_weekday_schedule,
                       arrive_larkspur_weekday_schedule))

    # ***Depart SF weekday schedule code ends***

    # ***Depart Larkspur weekend schedule code begins***

    # Get each schedule and delete header cells
    depart_larkspur_weekend_schedule = cache.get('cached_larkspur_weekend_schedule')
    if depart_larkspur_weekend_schedule == None:
        depart_larkspur_weekend_schedule = ws.col_values(10)
        cache.set('cached_larkspur_weekend_schedule', depart_larkspur_weekend_schedule)
    arrive_sf_weekend_schedule = cache.get('cached_arrive_sf_weekend_schedule')
    if arrive_sf_weekend_schedule == None:
        arrive_sf_weekend_schedule = ws.col_values(11)
        cache.set('cached_arrive_sf_weekend_schedule', arrive_sf_weekend_schedule)
    del depart_larkspur_weekend_schedule[0]
    del arrive_sf_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_3 = dict(zip(depart_larkspur_weekend_schedule,
                       arrive_sf_weekend_schedule))

    # ***Depart Larkspur weekend schedule code ends***

    # ***Depart SF weekend schedule code begins***

    # Get each schedule and delete header cells
    depart_sf_weekend_schedule = cache.get('cached_depart_sf_weekend_schedule')
    if depart_sf_weekend_schedule == None:
        depart_sf_weekend_schedule = ws.col_values(12)
        cache.set('cached_depart_sf_weekend_schedule', depart_sf_weekend_schedule)
    arrive_larkspur_weekend_schedule = cache.get('cached_arrive_larkspur_weekend_schedule')
    if arrive_larkspur_weekend_schedule == None:
        arrive_larkspur_weekend_schedule = ws.col_values(13)
        cache.set('cached_arrive_larkspur_weekend_schedule', arrive_larkspur_weekend_schedule)
    del depart_sf_weekend_schedule[0]
    del arrive_larkspur_weekend_schedule[0]

    # Convert both lists into a single dictionary
    times_4 = dict(zip(depart_sf_weekend_schedule,
                       arrive_larkspur_weekend_schedule))

    # ***Depart SF weekend schedule code ends***

    # Calculate next departures
    # Retrieve current pacific
    current_pacific_time = pendulum.now('America/Los_Angeles')
    current_day = current_pacific_time.day_of_week

    # Check whether weekday or weekend and calculate Larkspur next departures
    if current_day >= 1 and current_day <= 5:
        for departure in depart_larkspur_weekday_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_1 = departure
                break
    else:
        for departure in depart_larkspur_weekend_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_1 = departure
                break

    # Check whether weekday or weekend and calculate SF next departures
    if current_day >= 1 and current_day <= 5:
        for departure in depart_sf_weekday_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_2 = departure
                break
    else:
        for departure in depart_sf_weekend_schedule:
            format_time = pendulum.from_format(departure, 'h:mm A')\
                                  .set(tz='America/Los_Angeles')
            if current_pacific_time < format_time:
                next_departure_2 = departure
                break

    return render_template('schedule.html',
                           larkspur_schedule=larkspur_schedule,
                           times_1=times_1.items(),
                           times_2=times_2.items(),
                           times_3=times_3.items(),
                           times_4=times_4.items(),
                           next_departure_1=next_departure_1,
                           next_departure_2=next_departure_2,
                           table_headers_1=table_headers_1.items(),
                           table_headers_2=table_headers_2.items(),
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           th_1=th_1,
                           th_2=th_2,
                           ndh_1=ndh_1,
                           ndh_2=ndh_2,
                           h3_1=h3_1,
                           h3_2=h3_2,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2])


# Vallejo Ferry Schedule route
@app.route('/ca/vallejo-sf/')
# cache.cached(timeout=30)
def vallejo_ferry_schedule():
    # Set anacortes schedule variable to true
    # to indicate which template to use
    vallejo_schedule = True

    # Create instance of navbar()
    nav = navbar()

    # Generate breadcrumb for this route
    bc = generate_breadcrumb()

    # Get Anacortes schedule worksheet
    ws = sheet.get_worksheet(8)

    # Set title tag variable
    title = ws.acell('B1').value

    # Set h1 tag variable
    h1 = ws.acell('B2').value

    # Set leadcopy variable
    leadcopy = ws.acell('B3').value

    # Set H2 tags for each schedule
    th_1 = ws.acell('B5').value
    th_2 = ws.acell('B6').value

    # Initiate blank lists to store vallejo weekday schedules
    dv_weekday_schedule = []
    dv_weekday_temp_list = []
    dv_weekday_table_headers = []

    # Retrieve vallejo weekday schedule times
    depart_mare_island_weekday = ws.col_values(5)
    depart_vallejo_weekday = ws.col_values(6)
    arrive_sf_fb_weekday = ws.col_values(7)
    arrive_sf_pier_weekday = ws.col_values(8)

    # Create list of depart vallejo weekday table headers
    dv_weekday_table_headers.extend([depart_mare_island_weekday[0],
                                     depart_vallejo_weekday[0],
                                     arrive_sf_fb_weekday[0],
                                     arrive_sf_pier_weekday[0]])

    # Remove table headers
    del depart_mare_island_weekday[0]
    del depart_vallejo_weekday[0]
    del arrive_sf_fb_weekday[0]
    del arrive_sf_pier_weekday[0]

    # Set counter = 0
    c = 0

    # Create temp list for each vallejo weekday time row
    # Append temp list to schedule list
    while c < len(depart_mare_island_weekday):
        dv_weekday_temp_list = [depart_mare_island_weekday[c],
                                depart_vallejo_weekday[c],
                                arrive_sf_fb_weekday[c],
                                arrive_sf_pier_weekday[c]]
        dv_weekday_schedule.append(dv_weekday_temp_list)
        c += 1

    # Initiate blank lists to store vallejo weekend schedules
    dv_weekend_schedule = []
    dv_weekend_temp_list = []
    dv_weekend_table_headers = []

    # Retrieve vallejo weekend schedule times
    depart_mare_island_weekend = ws.col_values(10)
    depart_vallejo_weekend = ws.col_values(11)
    arrive_sf_fb_weekend = ws.col_values(12)
    arrive_sf_pier_weekend = ws.col_values(13)

    # Create list of depart vallejo weekend table headers
    dv_weekend_table_headers.extend([depart_mare_island_weekend[0],
                                     depart_vallejo_weekend[0],
                                     arrive_sf_fb_weekend[0],
                                     arrive_sf_pier_weekend[0]])

    # Remove table headers
    del depart_mare_island_weekend[0]
    del depart_vallejo_weekend[0]
    del arrive_sf_fb_weekend[0]
    del arrive_sf_pier_weekend[0]

    # Set counter = 0
    c = 0

    # Create temp list for each vallejo weekend time row
    # Append temp list to schedule list
    while c < len(depart_mare_island_weekend):
        dv_weekend_temp_list = [depart_mare_island_weekend[c],
                                depart_vallejo_weekend[c],
                                arrive_sf_fb_weekend[c],
                                arrive_sf_pier_weekend[c]]
        dv_weekend_schedule.append(dv_weekend_temp_list)
        c += 1

    # Initiate blank lists to store sf weekday schedules
    sf_weekday_schedule = []
    sf_weekday_temp_list = []
    sf_weekday_table_headers = []

    # Retrieve sf weekday schedule times
    depart_sf_fb_weekday = ws.col_values(15)
    depart_sf_pier_weekday = ws.col_values(16)
    arrive_vallejo_weekday = ws.col_values(17)
    arrive_mare_island_weekday = ws.col_values(18)

    # Create list of depart sf weekday table headers
    sf_weekday_table_headers.extend([depart_sf_fb_weekday[0],
                                    depart_sf_pier_weekday[0],
                                    arrive_vallejo_weekday[0],
                                    arrive_mare_island_weekday[0]])

    # Remove table headers
    del depart_sf_fb_weekday[0]
    del depart_sf_pier_weekday[0]
    del arrive_vallejo_weekday[0]
    del arrive_mare_island_weekday[0]

    # Set counter = 0
    c = 0

    # Create temp list for each depart sf weekday time row
    # Append temp list to sf weekday schedule list
    while c < len(depart_sf_fb_weekday):
        sf_weekday_temp_list = [depart_sf_fb_weekday[c],
                                depart_sf_pier_weekday[c],
                                arrive_vallejo_weekday[c],
                                arrive_mare_island_weekday[c]]
        sf_weekday_schedule.append(sf_weekday_temp_list)
        c += 1

    # Initiate blank lists to store sf weekday schedules
    sf_weekend_schedule = []
    sf_weekend_temp_list = []
    sf_weekend_table_headers = []

    # Retrieve sf weekend schedule times
    depart_sf_fb_weekend = ws.col_values(20)
    depart_sf_pier_weekend = ws.col_values(21)
    arrive_vallejo_weekend = ws.col_values(22)
    arrive_mare_island_weekend = ws.col_values(23)

    # Create list of depart sf weekend table headers
    sf_weekend_table_headers.extend([depart_sf_fb_weekend[0],
                                    depart_sf_pier_weekend[0],
                                    arrive_vallejo_weekend[0],
                                    arrive_mare_island_weekend[0]])

    # Remove table headers
    del depart_sf_fb_weekend[0]
    del depart_sf_pier_weekend[0]
    del arrive_vallejo_weekend[0]
    del arrive_mare_island_weekend[0]

    # Set counter = 0
    c = 0

    # Create temp list for each depart sf weekend time row
    # Append temp list to sf weekend schedule list
    while c < len(depart_sf_fb_weekend):
        sf_weekend_temp_list = [depart_sf_fb_weekend[c],
                                depart_sf_pier_weekend[c],
                                arrive_vallejo_weekend[c],
                                arrive_mare_island_weekend[c]]
        sf_weekend_schedule.append(sf_weekend_temp_list)
        c += 1

    return render_template('schedule.html',
                           vallejo_schedule=vallejo_schedule,
                           title=title,
                           h1=h1,
                           leadcopy=leadcopy,
                           th_1=th_1,
                           th_2=th_2,
                           dv_weekday_schedule=dv_weekday_schedule,
                           dv_weekday_table_headers=dv_weekday_table_headers,
                           dv_weekend_schedule=dv_weekend_schedule,
                           dv_weekend_table_headers=dv_weekend_table_headers,
                           sf_weekday_schedule=sf_weekday_schedule,
                           sf_weekday_table_headers=sf_weekday_table_headers,
                           sf_weekend_schedule=sf_weekend_schedule,
                           sf_weekend_table_headers=sf_weekend_table_headers,
                           bc_path=bc[0],
                           bc_state_text=bc[1],
                           bc_schedule_text=bc[2],
                           ny_nav_links=nav[0],
                           wa_nav_links=nav[1],
                           ca_nav_links=nav[2])


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
