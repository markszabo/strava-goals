import datetime
from dateutil.relativedelta import relativedelta
import calendar

def get_timestamp_days_ago(days_ago):
    a_year_ago = datetime.date.today() - datetime.timedelta(days_ago)
    return a_year_ago.strftime("%s")

def get_start_and_end_of_prior_week(nr_of_weeks_ago):
    now = datetime.datetime.now()
    days_passed_since_sunday = (now.weekday() - 6) % 7  # 6 represents Sunday, so we're finding the difference
    sunday = now - datetime.timedelta(days=nr_of_weeks_ago*7+days_passed_since_sunday)
    end_of_the_week = datetime.datetime(sunday.year, sunday.month, sunday.day, 23, 59, 59)
    monday = sunday - datetime.timedelta(days=6)
    start_of_the_week = datetime.datetime(monday.year, monday.month, monday.day, 0, 0, 0)
    return start_of_the_week, end_of_the_week

def get_start_and_end_of_prior_month(nr_of_months_ago):
    today = datetime.datetime.now()
    first_day = today - relativedelta(months=nr_of_months_ago, day=1)
    start_of_the_month = datetime.datetime(first_day.year, first_day.month, first_day.day, 0, 0, 0)
    first_day_of_next_month = today - relativedelta(months=nr_of_months_ago-1, day=1)
    end_of_the_month = datetime.datetime(first_day_of_next_month.year, first_day_of_next_month.month, first_day_of_next_month.day, 0, 0, 0) - datetime.timedelta(seconds=1)
    return start_of_the_month, end_of_the_month

def get_starttime_from_activity(activity):
    return datetime.datetime.strptime(activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
