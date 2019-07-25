from ferryschedules import app
from ferryschedules.models.schedule import Schedule
from pprint import pprint
from flask import render_template

@app.route('/wa/bremerton-seattle/')
def schedule_page():
    # daily_schedule = True
    next_departures = False
    schedule = Schedule(1)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(4)
    return render_template('daily_schedule.html',
                            # daily_schedule=daily_schedule,
                            next_departures=next_departures,
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            schedule_1=timetables[0],
                            schedule_2=timetables[1])