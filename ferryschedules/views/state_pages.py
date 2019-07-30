from ferryschedules import app
from ferryschedules.models.sitemap import Sitemap
from ferryschedules.views import navbar
from flask import render_template

@app.route('/ca/')
def ca_state_page():
    # Retrieve all schedule links for homepage and navbar
    links = navbar.retrieve_links()

    return render_template('ca.html',
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'])


@app.route('/ny/')
def ny_state_page():
    # Retrieve all schedule links for homepage and navbar
    links = navbar.retrieve_links()

    return render_template('ny.html',
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'])


@app.route('/wa/')
def wa_state_page():
    # Retrieve all schedule links for homepage and navbar
    links = navbar.retrieve_links()

    return render_template('wa.html',
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'])