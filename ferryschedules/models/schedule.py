from ferryschedules import gsheet
from ferryschedules import cache
import pendulum
import string

class Schedule:
    def __init__(self, worksheet_number):
        self.worksheet = gsheet.get_worksheet(worksheet_number)
        self.cache_meta_data_key = 'cached_meta_data_for_schedule_' + str(worksheet_number)
        self.cache_schedule_key = 'cached_timetables_for_schedule_' + str(worksheet_number)

    # Retrieve cell values from sheet for all meta data, headers and tags
    def retrieve_meta_data(self):
        
        self.md = cache.get(self.cache_meta_data_key)
        if self.md == None:
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
            cache.set(self.cache_meta_data_key, self.md)
        return self.md

    # Retrieve all schedule columns from the worksheet
    # start_column is the corresponding column in the google sheet where the timetable starts
    # schedule_type should be either "D" for Daily or "WWH" for Weekday Weekend Holiday
    def retrieve_schedules(self, start_column, D=False, WWH=False):
        self.schedule = cache.get(self.cache_schedule_key)
        if self.schedule == None:
            self.schedule = []
            temp_schedule = []
            column = start_column
            # Aggregate each schedule column into a list of lists
            while self.worksheet.col_values(column) != []:
                temp_schedule.append(self.worksheet.col_values(column))
                column += 1

            # Get each schedule block by taking first and second half of temp_schedule list 
            schedule_1 = temp_schedule[:len(temp_schedule)//2]
            schedule_2 = temp_schedule[len(temp_schedule)//2:]

            # If it is a Daily schedule, then no further splitting of the lists is necessary
            if D:
                # Tranpose each list into a timetable
                schedule_1 = list(map(list, zip(*schedule_1)))
                schedule_2 = list(map(list, zip(*schedule_2)))
                self.schedule.extend([schedule_1, schedule_2])
                cache.set(self.cache_schedule_key, self.schedule)
            
            # If it is a Weekday/Weekend/Holiday Schedule, we must split the lists further into appropriate schedules
            elif WWH:
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
                cache.set(self.cache_schedule_key, self.schedule)
            
        return self.schedule


    def calculate_next_departures(self, url, D=False, WWH=False):
        # if str(url).startswith('/ca/') or str(url).startswith('/wa/'):
        #     current_time = pendulum.now('America/Los_Angeles')
        # elif str(url).startswith('/ny/'):
        #     current_time = pendulum.now('America/New_York')

        if D and str(url).startswith('/ca/') or str(url).startswith('/wa/'):
            current_time = pendulum.now('America/Los_Angeles')
            print(self.schedule[0])
            for departure in self.schedule[0]:
                print(departure)
                print(departure[0])
                format_time = pendulum.from_format(departure[0], 'h:mm A')\
                              .set(tz='America/Los_Angeles')
                if current_time < format_time:
                    next_departure_1 = departure[0]
                    break
            for departure in self.schedule[1]:
                format_time = pendulum.from_format(departure[0], 'h:mm A')\
                              .set(tz='America/Los_Angeles')
                if current_time < format_time:
                    next_departure_2 = departure[0]
                    break

            self.next_departures = {'Next Departure 1': next_departure_1,
                                    'Next Departure 2': next_departure_2}
            
        return self.next_departures