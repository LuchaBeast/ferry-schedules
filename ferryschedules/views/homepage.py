from ferryschedules import app
from ferryschedules.models.sitemap import Sitemap
from flask import render_template

@app.route('/')
def homepage():

    sitemap = Sitemap()

    ca_links = sitemap.retrieve_all_links(ca=True)
    ny_links = sitemap.retrieve_all_links(ny=True)
    wa_links = sitemap.retrieve_all_links(wa=True)

    ca_links.sort(key = lambda ca_links: ca_links[2])
    ny_links.sort(key = lambda ny_links: ny_links[2])
    wa_links.sort(key = lambda wa_links: wa_links[2])

    return render_template('index.html',
                            ca_links=ca_links,
                            ny_links=ny_links,
                            wa_links=wa_links)   