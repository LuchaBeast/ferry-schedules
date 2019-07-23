from ferryschedules import app

@app.route('/')
def homepage():
    return "hello, world"