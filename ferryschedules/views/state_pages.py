from ferryschedules import app
from ferryschedules.models.sitemap import Sitemap
from ferryschedules.models.breadcrumb import Breadcrumb
from ferryschedules.views import navbar
from flask import render_template

@app.route('/ca/')
def ca_state_page():
    state_page = True
    
    # Retrieve all schedule links for homepage and navbar
    links = navbar.retrieve_links()

    breadcrumb = Breadcrumb(State=True)
    breadcrumb_state_text = breadcrumb.breadcrumb_state_text

    return render_template('ca.html',
                            state_page=state_page,
                            breadcrumb_state_text=breadcrumb_state_text,
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'])


@app.route('/ny/')
def ny_state_page():
    state_page = True
    
    # Retrieve all schedule links for homepage and navbar
    links = navbar.retrieve_links()

    breadcrumb = Breadcrumb(State=True)
    breadcrumb_state_text = breadcrumb.breadcrumb_state_text

    return render_template('ny.html',
                            state_page=state_page,
                            breadcrumb_state_text=breadcrumb_state_text,
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'])


@app.route('/wa/')
def wa_state_page():
    state_page = True

    # Retrieve all schedule links for homepage and navbar
    links = navbar.retrieve_links()

    breadcrumb = Breadcrumb(State=True)
    breadcrumb_state_text = breadcrumb.breadcrumb_state_text

    return render_template('wa.html',
                            state_page=state_page,
                            breadcrumb_state_text=breadcrumb_state_text,
                            ca_links=links['California'],
                            ny_links=links['New York'],
                            wa_links=links['Washington'])