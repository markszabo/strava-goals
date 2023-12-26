import os
import datetime
import requests
import sys

ACCESS_TOKEN=os.environ['ACCESS_TOKEN']

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

# Print the result
#for activity in ordered_activities:
#    print(f"{activity['name']}: {activity['start_date']}")

