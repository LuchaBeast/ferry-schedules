from flask import Flask

app = Flask(__name__)

from app.views import homepage
from app.views import state_pages
from app.views import daily_schedules