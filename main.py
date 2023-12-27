import os
import datetime
import requests
import sys
import yagmail
from jinja2 import Environment, FileSystemLoader

# goals
WEEKLY_DISTANCE_GOAL = 10
MONTHLY_DISTANCE_GOAL = 100

# config from environment variables
ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
GOOGLE_USER=os.environ['GOOGLE_USER']
GOOGLE_PASSWORD=os.environ['GOOGLE_PASSWORD']
RECIPIENT_EMAIL=os.environ['RECIPIENT_EMAIL']

# dev config
REQUEST_PAGE_SIZE=200 # 200 seems to be the maximum

a_year_ago = datetime.date.today() - datetime.timedelta(365)
a_year_ago_timestamp = a_year_ago.strftime("%s")

headers = {
  "Authorization": "Bearer " + ACCESS_TOKEN,
  "Accept": "application/json",
}

page = 1
activities = []

while True:
  url = f"https://www.strava.com/api/v3/athlete/activities?per_page={REQUEST_PAGE_SIZE}&page={page}&after={a_year_ago_timestamp}"
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    # Parse the response as JSON
    data = response.json()
    if len(data) == 0:
      break
    activities.extend(data)
  else:
      print(f"Error while getting activities: {response.status_code} - {response.text}")
      sys.exit(1)
  page+=1

print(len(activities))

ordered_activities = sorted(activities, key=lambda x: x["start_date"])

# Calculate progress TODO

weekly_progress = [
    {"dates": "Dec 18 - Dec 24", "progress": 80, "distance_all": 8, "distance_cycling": 0, "distance_running": 8},
    {"dates": "Dec 11 - Dec 17", "progress": 100, "distance_all": 15, "distance_cycling": 5, "distance_running": 10},
    {"dates": "Dec 4 - Dec 10", "progress": 20, "distance_all": 2, "distance_cycling": 0, "distance_running": 2},
    {"dates": "Nov 27 - Dec 3", "progress": 50, "distance_all": 5, "distance_cycling": 5, "distance_running": 0},
    {"dates": "Nov 20 - Nov 26", "progress": 100, "distance_all": 10, "distance_cycling": 0, "distance_running": 10},
]

monthly_progress = [
    {"dates": "November", "progress": 80, "distance_all": 80, "distance_cycling": 60, "distance_running": 20},
    {"dates": "October", "progress": 100, "distance_all": 150, "distance_cycling": 120, "distance_running": 30},
]

# Template email
jinja_env = Environment(loader=FileSystemLoader("./templates"))
template = jinja_env.get_template("email.html")

email_html = template.render(weekly_progress=weekly_progress, monthly_progress=monthly_progress)

# Send email
yag = yagmail.SMTP(GOOGLE_USER, GOOGLE_PASSWORD)
yag.send(
  to = RECIPIENT_EMAIL,
  subject = 'Your weekly Strava progress report',
  contents = email_html.replace("\n","") # newlines get converted to <br> which messes up the table
)
