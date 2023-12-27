# strava-goals

An automation to send weekly emails about my progress towards my Strava goals

My Strava goals are:

* 10 km excercise per week (Monday-Sunday)
* 100 km excercise per calendar month

## Setup

### 1. Create a Strava App

Follow the instructions on https://developers.strava.com/docs/getting-started/

Get a refresh token for the scope `activity:read_all`, e.g.

```
https://www.strava.com/oauth/authorize?client_id=YOURCLIENTID&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all
```

Then exchange the authorization code from the redirect URL for a refresh token:

```sh
curl -X POST https://www.strava.com/oauth/token \
	-F client_id=YOURCLIENTID \
	-F client_secret=YOURCLIENTSECRET \
	-F code=AUTHORIZATIONCODE \
	-F grant_type=authorization_code
```

### 2. Configure the following GitHub Secrets

Based on the values from the previous step, create the following GitHub secrets.

```
STRAVA_APP_CLIENT_ID
STRAVA_APP_CLIENT_SECRET
STRAVA_APP_REFRESH_TOKEN
```

### 3. Create a GitHub PAT

Create a GitHub Fine-grained personal access token with the permission to read/write secrets on this repo, and add it to GitHub Secrets under `REPO_ACCESS_TOKEN`.

This will be used to continously update the refresh token (as it's single-use).

### 4. Create a Google App Password

Following the [instructions here](https://support.google.com/accounts/answer/185833) create a Google App Password for your account and store it in GitHub Secrets under `GOOGLE_PASSWORD`.
Also store the associated Google username in `GOOGLE_USER`.
These are used for sending the email, and the recipient can be different.

### 5. Configure the address to send the email to

Configure the address you want to receive the email to in the GitHub Secret `RECIPIENT_EMAIL`.
