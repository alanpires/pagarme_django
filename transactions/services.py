from datetime import datetime
import calendar

def converted_date(date):
    # converted_data
        month = datetime.strptime(date, "%m-%Y").month
        year = datetime.strptime(date, "%m-%Y").year
        last_day_of_the_month = calendar.monthrange(year, month)[1]
        converted_date = datetime.strptime(f"{last_day_of_the_month}-{month}-{year}", "%d-%m-%Y")
        
        return converted_date