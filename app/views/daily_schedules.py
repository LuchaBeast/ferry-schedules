from app import app

@app.route('/wa/bremerton-seattle/')
def daily_schedule():
    return 'This is a daily schedule'