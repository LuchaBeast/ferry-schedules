from ferryschedules import app
from ferryschedules.models.schedule import Schedule
from ferryschedules.views import navbar
from ferryschedules.views import breadcrumb
from flask import render_template

@app.route('/wa/bremerton-seattle/')
def bremerton_seattle():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(1)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, D=True)
    return render_template('daily_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            schedule_1=timetables[0],
                            schedule_2=timetables[1],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])


@app.route('/wa/bainbridge-island-seattle/')
def bainbridge_island_seattle():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(2)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, WWH=True)
    return render_template('weekday_weekend_holiday_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            weekday_schedule_1=timetables[0],
                            weekday_schedule_2=timetables[1],
                            weekend_schedule_1=timetables[2],
                            weekend_schedule_2=timetables[3],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])


@app.route('/wa/anacortes-san-juan-islands/')
def anacortes_san_juan_islands():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(3)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, D=True)
    return render_template('daily_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            schedule_1=timetables[0],
                            schedule_2=timetables[1],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])


@app.route('/wa/kingston-edmonds/')
def kingston_edmonds():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(4)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, D=True)
    return render_template('daily_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            schedule_1=timetables[0],
                            schedule_2=timetables[1],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])


@app.route('/ny/staten-island/')
def staten_island():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(5)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, WWH=True)
    return render_template('weekday_weekend_holiday_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            weekday_schedule_1=timetables[0],
                            weekday_schedule_2=timetables[1],
                            weekend_schedule_1=timetables[2],
                            weekend_schedule_2=timetables[3],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])


@app.route('/ca/larkspur-san-francisco/')
def larkspur_sf():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(6)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, WWH=True)
    return render_template('weekday_weekend_holiday_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            weekday_schedule_1=timetables[0],
                            weekday_schedule_2=timetables[1],
                            weekend_schedule_1=timetables[2],
                            weekend_schedule_2=timetables[3],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])


@app.route('/wa/southworth-vashon/')
def southworth_vashon():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(7)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, WWH=True)
    return render_template('weekday_weekend_holiday_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            weekday_schedule_1=timetables[0],
                            weekday_schedule_2=timetables[1],
                            weekend_schedule_1=timetables[2],
                            weekend_schedule_2=timetables[3],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])


@app.route('/ca/vallejo-san-francisco/')
def vallejo_sf():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(8)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, WWH=True)
    return render_template('weekday_weekend_holiday_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            weekday_schedule_1=timetables[0],
                            weekday_schedule_2=timetables[1],
                            weekend_schedule_1=timetables[2],
                            weekend_schedule_2=timetables[3],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])


@app.route('/wa/anacortes-sidney-bc/')
def anacortes_sidney_bc():
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb()
    schedule = Schedule(9)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, D=True)
    return render_template('daily_schedule.html',
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            schedule_1=timetables[0],
                            schedule_2=timetables[1],
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'],
                            breadcrumb_path=bc['State Path'],
                            breadcrumb_state_text=bc['State Breadcrumb Text'],
                            breadcrumb_schedule_text=bc['Schedule Breadcrumb Text'])