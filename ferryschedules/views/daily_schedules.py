from ferryschedules import app
from ferryschedules.models.schedule import Schedule

@app.route('/wa/bremerton-seattle/')
def retrieve_schedule():
    schedule = Schedule(1)
    departure_schedule = schedule.retrieve_departure_schedule(4)
    print(departure_schedule)
    return 'This is a daily schedule'