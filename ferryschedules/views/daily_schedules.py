from ferryschedules import app
from ferryschedules.models.schedule import Schedule

@app.route('/wa/bremerton-seattle/')
def retrieve_schedule():
    schedule = Schedule(1).worksheet
    print(schedule.col_values(4))
    return 'This is a daily schedule'