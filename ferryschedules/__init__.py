from flask import Flask

app = Flask(__name__)

from ferryschedules.views import homepage
from ferryschedules.views import state_pages
from ferryschedules.views import daily_schedules