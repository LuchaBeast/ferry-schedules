from flask import request
# from ferryschedules.views import navbar
from ferryschedules.models.sitemap import Sitemap

def create_breadcrumb(State=False):

    # Get path of the route
    url = request.path

    # Split each directory in the route
    split_url = url.split('/')

    # Filter out empty list items
    # Retrieve state path from list
    path_extract = list(filter(None, split_url))[0]

    # Rebuild path for state page
    breadcrumb_state_path = "/" + path_extract + "/"

    # Create the anchor text for the State part of the breadcrumb
    breadcrumb_state_text = path_extract.upper()

    if State:
        return breadcrumb_state_text
    else:
        sitemap = Sitemap()
        links = sitemap.retrieve_all_links()
        for link in links:
            if url == link[2]:
                breadcrumb_schedule_text = link[5]
        
        bc_dict = dict({'State Path': breadcrumb_state_path, 'State Breadcrumb Text': breadcrumb_state_text, 'Schedule Breadcrumb Text': breadcrumb_schedule_text})
        return bc_dict