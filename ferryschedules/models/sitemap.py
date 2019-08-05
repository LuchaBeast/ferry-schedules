from ferryschedules import gsheet
from ferryschedules import cache

class Sitemap:
    SITEMAP_WORKSHEET_NUMBER = 0
    SCHEDULE_ID_COLUMN = 1
    ROOT_COLUMN = 2
    SLUG_COLUMN = 3
    ANCHOR_TEXT_COLUMN = 4
    SHORT_DESCRIPTION_COLUMN=5
    BREADCRUMB_TEXT_COLUMN=6

    # Retrieve sitemap worksheet from google sheet
    def __init__(self):
        self.worksheet = gsheet.get_worksheet(self.SITEMAP_WORKSHEET_NUMBER)


    def retrieve_all_links(self, california=False, newyork=False, washington=False):
        # self.link_lists = []

        # Create list of lists containing all link values from the worksheet
        # self.cached_schedule_id_column = cache.get('cached_schedule_id_column')
        # if self.cached_schedule_id_column == None:
        #     self.cached_schedule_id_column = self.worksheet.col_values(self.SCHEDULE_ID_COLUMN)
        #     cache.set('cached_schedule_id_column', self.cached_schedule_id_column)
        # self.link_lists.append(self.cached_schedule_id_column)

        # self.cached_root_column = cache.get('cached_root_column')
        # if self.cached_root_column == None:
        #     self.cached_root_column = self.worksheet.col_values(self.ROOT_COLUMN)
        #     cache.set('cached_root_column', self.cached_root_column)
        # self.link_lists.append(self.cached_root_column)

        # self.cached_slug_column = cache.get('cached_slug_column')
        # if self.cached_slug_column == None:
        #     self.cached_slug_column = self.worksheet.col_values(self.SLUG_COLUMN)
        #     cache.set('cached_slug_column', self.cached_slug_column)
        # self.link_lists.append(self.cached_slug_column)

        # self.cached_anchor_text_column = cache.get('cached_anchor_text_column')
        # if self.cached_anchor_text_column == None:
        #     self.cached_anchor_text_column = self.worksheet.col_values(self.ANCHOR_TEXT_COLUMN)
        #     cache.set('cached_anchor_text_column', self.cached_anchor_text_column)
        # self.link_lists.append(self.cached_anchor_text_column)

        # self.cached_short_description_column = cache.get('cached_short_description_column')
        # if self.cached_short_description_column == None:
        #     self.cached_short_description_column = self.worksheet.col_values(self.SHORT_DESCRIPTION_COLUMN)
        #     cache.set('cached_short_description_column', self.cached_short_description_column)
        # self.link_lists.append(self.cached_short_description_column)

        # self.cached_breadcrumb_text = cache.get('cached_breadcrumb_text')
        # if self.cached_breadcrumb_text == None:
        #     self.cached_breadcrumb_text = self.worksheet.col_values(self.BREADCRUMB_TEXT_COLUMN)
        #     cache.set('cached_breadcrumb_text', self.cached_breadcrumb_text)
        # self.link_lists.append(self.cached_breadcrumb_text)

        self.link_lists = cache.get('cached_link_lists')
        if self.link_lists == None:
            self.link_lists = []
            self.link_lists.append(self.worksheet.col_values(self.SCHEDULE_ID_COLUMN))
            self.link_lists.append(self.worksheet.col_values(self.ROOT_COLUMN))
            self.link_lists.append(self.worksheet.col_values(self.SLUG_COLUMN))
            self.link_lists.append(self.worksheet.col_values(self.ANCHOR_TEXT_COLUMN))
            self.link_lists.append(self.worksheet.col_values(self.SHORT_DESCRIPTION_COLUMN))
            self.link_lists.append(self.worksheet.col_values(self.BREADCRUMB_TEXT_COLUMN))

            # Transpose link list to pair up each link's info into its own list
            self.link_lists = list(map(list, zip(*self.link_lists)))

            cache.set('cached_link_lists', self.link_lists)

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