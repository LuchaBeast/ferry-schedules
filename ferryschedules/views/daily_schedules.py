from ferryschedules import app
from ferryschedules.models.schedule import Schedule

@app.route('/wa/bremerton-seattle/')
def retrieve_schedule():
    schedule = Schedule(1)
    meta_data = schedule.retrieve_meta_data()
    print(meta_data)
    return 'This is a daily schedule'