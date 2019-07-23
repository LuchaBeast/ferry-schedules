from flask import Flask
from ferryschedules.models.worksheet import Worksheet

app = Flask(__name__)
worksheet = Worksheet()

from ferryschedules.views import homepage
from ferryschedules.views import state_pages
from ferryschedules.views import daily_schedules