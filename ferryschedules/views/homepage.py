from ferryschedules import app
from ferryschedules.models.sitemap import Sitemap
from ferryschedules.views import navbar
from flask import render_template

@app.route('/')
def homepage():

    # Retrieve all schedule links for homepage and navbar
    links = navbar.retrieve_links()
    ca_links = links['California']
    ny_links = links['New York']
    wa_links = links['Washington']

    return render_template('index.html',
                            ca_links=ca_links,
                            ny_links=ny_links,
                            wa_links=wa_links)   