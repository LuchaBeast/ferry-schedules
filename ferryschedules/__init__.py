from flask import Flask
from ferryschedules.models.worksheet import Gsheet
import bmemcached
import os

app = Flask(__name__)
gsheet = Gsheet()

servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
user = os.environ.get('MEMCACHIER_USERNAME', '')
passw = os.environ.get('MEMCACHIER_PASSWORD', '')

cache = bmemcached.Client(servers, username=user, password=passw)

cache.enable_retry_delay(True)  # Enabled by default. Sets retry delay to 5s.

from ferryschedules.views import homepage
from ferryschedules.views import state_pages
from ferryschedules.views import schedule_pages