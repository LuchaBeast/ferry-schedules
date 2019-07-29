from ferryschedules import app
from ferryschedules.models.sitemap import Sitemap
from flask import render_template

@app.route('/')
def homepage():

    # Initiliaze empty link lists for each State
    ca_links = []
    ny_links = []
    wa_links = []

    sitemap = Sitemap()
    homepage_links = sitemap.retrieve_all_links()

    for link in homepage_links:
        if link[0] == '/ca/':
            ca_links.append(link)
        elif link[0] == '/ny/':
            ny_links.append(link)
        elif link[0] == '/wa/':
            wa_links.append(link)

    ca_links.sort(key = lambda ca_links: ca_links[2])
    ny_links.sort(key = lambda ny_links: ny_links[2])
    wa_links.sort(key = lambda wa_links: wa_links[2])

    return render_template('index.html',
                            ca_links=ca_links,
                            ny_links=ny_links,
                            wa_links=wa_links)   