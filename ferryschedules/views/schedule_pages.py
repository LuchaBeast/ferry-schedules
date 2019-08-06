from ferryschedules import app
from ferryschedules.models.schedule import Schedule
from ferryschedules.views import navbar
from ferryschedules.views import breadcrumb
from flask import render_template, request


@app.route('/wa/anacortes-san-juan-islands/')
@app.route('/wa/anacortes-sidney-bc/')
@app.route('/wa/bremerton-seattle/')
@app.route('/wa/kingston-edmonds/')
def daily_schedule_pages():
    url = request.path
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb(url)
    for value in links.values():
        for v in value:
            if v[2] == url:
                schedule_id = int(v[0])
                schedule = Schedule(schedule_id)
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
@app.route('/ny/staten-island/')
@app.route('/ca/larkspur-san-francisco/')
@app.route('/wa/southworth-vashon/')
@app.route('/ca/vallejo-san-francisco/')
def weekday_weekend_holiday_schedule_pages():
    url = request.path
    next_departures = False
    links = navbar.retrieve_links()
    bc = breadcrumb.create_breadcrumb(url)
    for value in links.values():
        for v in value:
            if v[2] == url:
                schedule_id = int(v[0])
                schedule = Schedule(schedule_id)
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