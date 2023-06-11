import datetime, calendar
from datetime import datetime

def date(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d")
    day_name = date.strftime("%A")

    year, month, day = (int(x) for x in date_string.split('-'))

    #suffix
    last_digit = day % 10
    if last_digit == 1:
        suffix = "st"
    elif last_digit == 2:
        suffix = "nd"
    elif last_digit == 3:
        suffix = "rd"
    else:
        suffix = "th"

    #month name
    month_name = calendar.month_name[month]

    day_month_string = f'{day_name}, {month_name} {day}'
    
    return day_month_string, suffix, year
