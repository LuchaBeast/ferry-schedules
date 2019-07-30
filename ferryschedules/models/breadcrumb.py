from flask import request

class Breadcrumb:
    def __init__(self, State=False):
        if State:
            # Get path of the route
            url = request.path

            # Split each directory in the route
            split_url = url.split('/')

            # Filter out empty list items
            # Retrieve state path from list
            path_extract = list(filter(None, split_url))[0]

            # Rebuild path for state page
            # breadcrumb_path = "/" + path_extract + "/"

            # Create the anchor text for the State part of the breadcrumb
            self.breadcrumb_state_text = path_extract.upper()