from ferryschedules import app
from ferryschedules.models.schedule import Schedule
from pprint import pprint

@app.route('/wa/bremerton-seattle/')
def schedule_page():
    schedule = Schedule(1)
    departure_schedule = schedule.retrieve_schedules(4)
    pprint(departure_schedule)
    return 'This is a schedule page'