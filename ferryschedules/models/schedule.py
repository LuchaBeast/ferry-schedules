from ferryschedules import gsheet
# import gspread

class Schedule:
    def __init__(self, worksheet_number):
        self.worksheet = gsheet.get_worksheet(worksheet_number)

    # Retrieve cell values from sheet for all meta data, headers and tags
    def retrieve_meta_data(self):
        self.title_tag = self.worksheet.acell('B1').value
        self.h1 = self.worksheet.acell('B2').value
        self.lead_copy = self.worksheet.acell('B3').value
        self.effective_dates = self.worksheet.acell('B4').value
        self.h2_1 = self.worksheet.acell('B5').value
        self.h2_2 = self.worksheet.acell('B6').value
        self.next_departure_card_header_1 = self.worksheet.acell('B7').value
        self.next_departure_card_header_2 = self.worksheet.acell('B8').value
        self.md = {
                          "Title Tag": self.title_tag,
                          "H1": self.h1,
                          "Lead Copy": self.lead_copy,
                          "Effective Dates": self.effective_dates,
                          "H2 1": self.h2_1,
                          "H2 2": self.h2_2,
                          "Next Departure Card Header 1": self.next_departure_card_header_1,
                          "Next Departure Card Header 2": self.next_departure_card_header_2
                         }
        return self.md

    # Retrieve departure schedule using column numbers as args
    def retrieve_departure_schedule(self, start_column):
        
        self.departure_schedule = []

        column = start_column

        while self.worksheet.col_values(column) != []:
            self.departure_schedule.append(self.worksheet.col_values(column))
            column += 1

        return self.departure_schedule
        

    # Retrieve return schedule using column numbers as args
    def retrieve_return_schedule(self, *args):
        return args