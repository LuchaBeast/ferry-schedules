from ferryschedules import gsheet

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

    # Retrieve all schedule columns from the worksheet
    # start_column is the corresponding column in the google sheet where the timetable starts
    # schedule_type should be either "D" for Daily or "WWH" for Weekday Weekend Holiday
    def retrieve_schedules(self, start_column, schedule_type):
        self.schedule = []
        temp_schedule = []

        column = start_column
        st = schedule_type

        # Aggregate each schedule column into a list of lists
        while self.worksheet.col_values(column) != []:
            temp_schedule.append(self.worksheet.col_values(column))
            column += 1

        # Get each schedule block by taking first and second half of temp_schedule list 
        schedule_1 = temp_schedule[:len(temp_schedule)//2]
        schedule_2 = temp_schedule[len(temp_schedule)//2:]

        # If it is a Daily schedule, then no further splitting of the lists is necessary
        if st == "D":
            # Tranpose each list into a timetable
            schedule_1 = list(map(list, zip(*schedule_1)))
            schedule_2 = list(map(list, zip(*schedule_2)))
            self.schedule.extend([schedule_1, schedule_2])
        
        # If it is a Weekday/Weekend/Holiday Schedule, we must split the lists further into appropriate schedules
        elif st == "WWH":
            weekday_schedule_1 = schedule_1[:len(schedule_1)//2]
            weekday_schedule_2 = schedule_1[len(schedule_1)//2:]

            weekend_holiday_schedule_1 = schedule_2[:len(schedule_2)//2]
            weekend_holiday_schedule_2 = schedule_2[len(schedule_2)//2:]

            #Transpose each list into a timetable
            weekday_schedule_1 = list(map(list, zip(*weekday_schedule_1)))
            weekday_schedule_2 = list(map(list, zip(*weekday_schedule_2)))
            weekend_holiday_schedule_1 = list(map(list, zip(*weekend_holiday_schedule_1)))
            weekend_holiday_schedule_2 = list(map(list, zip(*weekend_holiday_schedule_2)))

            self.schedule.extend([weekday_schedule_1, weekday_schedule_2, weekend_holiday_schedule_1, weekend_holiday_schedule_2])
            

        return self.schedule
