from ferryschedules import gsheet
from ferryschedules import cache

class Sitemap:
    SITEMAP_WORKSHEET_NUMBER = 0
    SCHEDULE_ID = 1
    ROOT_COLUMN = 2
    SLUG_COLUMN = 3
    ANCHOR_TEXT_COLUMN = 4
    SHORT_DESCRIPTION_COLUMN=5
    BREADCRUMB_TEXT=6

    # Retrieve sitemap worksheet from google sheet
    def __init__(self):
        self.worksheet = gsheet.get_worksheet(self.SITEMAP_WORKSHEET_NUMBER)


    def retrieve_all_links(self, california=False, newyork=False, washington=False):
        self.link_lists = []

        # Create list of lists containing all link values from the worksheet
        self.schedule_id_column = cache.get('cached_schedule_id_column')
        if self.schedule_id_column == None:
            self.schedule_id_column = self.worksheet.col_values(self.SCHEDULE_ID)
            cache.set('cached_schedule_id_column', schedule_id_column)
        self.link_lists.append(self.schedule_id_column)


        self.link_lists.append(self.worksheet.col_values(self.ROOT_COLUMN))
        self.link_lists.append(self.worksheet.col_values(self.SLUG_COLUMN))
        self.link_lists.append(self.worksheet.col_values(self.ANCHOR_TEXT_COLUMN))
        self.link_lists.append(self.worksheet.col_values(self.SHORT_DESCRIPTION_COLUMN))
        self.link_lists.append(self.worksheet.col_values(self.BREADCRUMB_TEXT))

        # Transpose link list to pair up each link's info into its own list
        self.link_lists = list(map(list, zip(*self.link_lists)))


        if california:
            self.ca_links = []
            for link in self.link_lists:
                if link[1] == '/ca/':
                    self.ca_links.append(link)
            return self.ca_links
        elif newyork:
            self.ny_links = []
            for link in self.link_lists:
                if link[1] == '/ny/':
                    self.ny_links.append(link)
            return self.ny_links
        elif washington:
            self.wa_links = []
            for link in self.link_lists:
                if link[1] == '/wa/':
                    self.wa_links.append(link)
            return self.wa_links
        else:
            return self.link_lists