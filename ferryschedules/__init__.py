from flask import Flask
from ferryschedules.models.worksheet import Gsheet

app = Flask(__name__)
gsheet = Gsheet()

from ferryschedules.views import navbar

links = navbar.retrieve_links()

from ferryschedules.views import homepage
from ferryschedules.views import state_pages
from ferryschedules.views import schedule_pages