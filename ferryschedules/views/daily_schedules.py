from ferryschedules import app
from ferryschedules.models.schedule import Schedule
from flask import render_template


@app.route('/wa/bremerton-seattle/')
def schedule_page():
    # daily_schedule = True
    next_departures = False
    schedule = Schedule(1)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, "D")
    return render_template('daily_schedule.html',
                            # daily_schedule=daily_schedule,
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            schedule_1=timetables[0],
                            schedule_2=timetables[1])

@app.route('/wa/anacortes-san-juan-islands/')
def schedule_2_page():
    # daily_schedule = True
    next_departures = False
    schedule = Schedule(3)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, "D")
    return render_template('daily_schedule.html',
                            # daily_schedule=daily_schedule,
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            schedule_1=timetables[0],
                            schedule_2=timetables[1])


@app.route('/wa/bainbridge-island-seattle/')
def schedule_3_page():
    # daily_schedule = True
    next_departures = False
    schedule = Schedule(2)
    meta_data = schedule.retrieve_meta_data()
    timetables = schedule.retrieve_schedules(5, "WWH")
    return render_template('weekday_weekend_holiday_schedule.html',
                            # daily_schedule=daily_schedule,
                            next_departures=next_departures,
                            title=meta_data['Title Tag'],
                            h1=meta_data['H1'],
                            leadcopy=meta_data['Lead Copy'],
                            h2_1=meta_data['H2 1'],
                            h2_2=meta_data['H2 2'],
                            weekday_schedule_1=timetables[0],
                            weekday_schedule_2=timetables[1],
                            weekend_schedule_1=timetables[2],
                            weekend_schedule_2=timetables[3])