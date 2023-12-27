import requests
import sys

# local imports
import date

# dev config
REQUEST_PAGE_SIZE=200 # 200 seems to be the maximum

def get_activities(after, ACCESS_TOKEN):
  headers = {
    "Authorization": "Bearer " + ACCESS_TOKEN,
    "Accept": "application/json",
  }

  page = 1
  activities = []

  while True:
    url = f"https://www.strava.com/api/v3/athlete/activities?per_page={REQUEST_PAGE_SIZE}&page={page}&after={after}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      data = response.json()
      if len(data) == 0:
        break # exit the loop if we reached the end of the data
      activities.extend(data)
    else:
      raise Exception(f"Error while getting activities: {response.status_code} - {response.text}")
    page+=1
  
  return activities

def get_progress(activities, timeframe, number_of_periods, goal):
  progress = []
  
  for period_nr in range(number_of_periods):
    if timeframe == "week":
      timeframe_start, timeframe_end = date.get_start_and_end_of_prior_week(period_nr)
      timeframe_display = f"{timeframe_start.strftime('%b %d')} - {timeframe_end.strftime('%b %d')}"
    elif timeframe == "month":
      timeframe_start, timeframe_end = date.get_start_and_end_of_prior_month(period_nr)
      timeframe_display = timeframe_start.strftime('%B')
    else:
      raise ValueError(f"Unsupported timeframe. Got {timeframe}, but only 'week' and 'month' are supported")
    distance_all = 0
    distance_cycling = 0
    distance_running = 0
    for activity in activities:
      activity_start = date.get_starttime_from_activity(activity)
      if timeframe_start < activity_start and activity_start < timeframe_end:
        distance_all += activity["distance"]/1000 # distance is in meters
        if activity["type"] == "Ride":
          distance_cycling += activity["distance"]/1000
        elif activity["type"] == "Run":
          distance_running += activity["distance"]/1000
    
    progress.append({
      "dates": timeframe_display,
      "progress": min(round(distance_all/goal*100), 100),
      "distance_all": round(distance_all * 100) / 100, # only keep 2 decimal places, e.g. 12.34
      "distance_cycling": round(distance_cycling * 100) / 100,
      "distance_running": round(distance_running * 100) / 100,
    })

  return progress