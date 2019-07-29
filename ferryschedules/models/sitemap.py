from ferryschedules import gsheet

class Sitemap:
    SITEMAP_WORKSHEET_NUMBER = 0
    ROOT_COLUMN = 1
    SLUG_COLUMN = 2
    ANCHOR_TEXT_COLUMN = 3
    SHORT_DESCRIPTION_COLUMN=4

    # Retrieve sitemap worksheet from google sheet
    def __init__(self):
        self.worksheet = gsheet.get_worksheet(self.SITEMAP_WORKSHEET_NUMBER)

    def retrieve_all_links(self):
        self.link_lists = []

        # Create list of lists containing all link values from the worksheet
        self.link_lists.append(self.worksheet.col_values(self.ROOT_COLUMN))
        self.link_lists.append(self.worksheet.col_values(self.SLUG_COLUMN))
        self.link_lists.append(self.worksheet.col_values(self.ANCHOR_TEXT_COLUMN))
        self.link_lists.append(self.worksheet.col_values(self.SHORT_DESCRIPTION_COLUMN))

        # Transpose link list to pair up each link's info into its own list
        self.link_lists = list(map(list, zip(*self.link_lists)))       

        return self.link_lists