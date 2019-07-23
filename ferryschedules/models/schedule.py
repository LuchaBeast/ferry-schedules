from ferryschedules import gsheet

class Schedule:
    def __init__(self, worksheet_number):
        self.worksheet = gsheet.get_worksheet(worksheet_number)