import os
import yagmail

# local imports
import date, strava, templating

# config
WEEKLY_DISTANCE_GOAL = 10
MONTHLY_DISTANCE_GOAL = 100
NUMBER_OF_WEEKS_IN_THE_EMAIL = 12
NUMBER_OF_MONTHS_IN_THE_EMAIL = 12

# config from environment variables
ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
GOOGLE_USER=os.environ['GOOGLE_USER']
GOOGLE_PASSWORD=os.environ['GOOGLE_PASSWORD']
RECIPIENT_EMAIL=os.environ['RECIPIENT_EMAIL']

print("Getting activities from the Strava API")
from_timestamp = date.get_timestamp_days_ago(max(NUMBER_OF_WEEKS_IN_THE_EMAIL*7, NUMBER_OF_MONTHS_IN_THE_EMAIL*31))
activities = strava.get_activities(from_timestamp, ACCESS_TOKEN)

print("Calculating progress")
weekly_progress = strava.get_progress(activities, "week", NUMBER_OF_WEEKS_IN_THE_EMAIL, WEEKLY_DISTANCE_GOAL)
monthly_progress = strava.get_progress(activities, "month", NUMBER_OF_MONTHS_IN_THE_EMAIL, MONTHLY_DISTANCE_GOAL)

print("Preparing email")
email_html = templating.get_templated_email(weekly_progress=weekly_progress, monthly_progress=monthly_progress)

print("Sending email")
yag = yagmail.SMTP(GOOGLE_USER, GOOGLE_PASSWORD)
yag.send(
  to = RECIPIENT_EMAIL,
  subject = 'Your weekly Strava progress report',
  contents = email_html.replace("\n","") # newlines get converted to <br> which messes up the table
)

print("Completed")
