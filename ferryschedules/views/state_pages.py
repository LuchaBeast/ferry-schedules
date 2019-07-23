from ferryschedules import app

@app.route('/wa/')
def state_page():
    return 'This is a state page'