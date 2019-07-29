from ferryschedules.models.sitemap import Sitemap

def retrieve_links():
    sitemap = Sitemap()

    ca_links = sitemap.retrieve_all_links(california=True)
    ny_links = sitemap.retrieve_all_links(newyork=True)
    wa_links = sitemap.retrieve_all_links(washington=True)

    ca_links.sort(key = lambda ca_links: ca_links[2])
    ny_links.sort(key = lambda ny_links: ny_links[2])
    wa_links.sort(key = lambda wa_links: wa_links[2])

    links = dict({'California': ca_links,
                  'New York': ny_links,
                  'Washington': wa_links})

    return links