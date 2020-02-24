import requests
from datetime import datetime
import json
token = "replace with your token"

day = datetime.today().strftime('%Y-%m-%d')
r = requests.get("https://api.the-odds-api.com/v3/odds/?sport=basketball_ncaab&mkt=spreads&region=us&apiKey=replace with your API key")
data = r.json()['data']
choices = []
position = 1
for game in data:
    if game['sites_count'] > 0:
        sites = game['sites']
        home_team = game['teams'][0]
        away_team = game['teams'][1]
        home_team_spread = sites[0]['odds']['spreads']['points'][0]
        choices.append({"text": home_team + ": " + home_team_spread, "position": position})
        position = position + 1
        if home_team_spread[0] == '-':
            choices.append({"text": away_team + ": " + home_team_spread[1:], "position": position})
            # print(home_team, home_team_spread, " vs ", away_team,  " +" + home_team_spread[1:])
        else:
            choices.append({"text": away_team + ": -" + home_team_spread, "position": position})
            # print(home_team, home_team_spread, " vs ", away_team, " -" + home_team_spread)
        position = position + 1

s = requests.Session()
s.headers.update({
  "Authorization": "Bearer %s" % token,
  "Content-Type": "application/json"
})
url = "https://api.surveymonkey.com/v3/surveys"
payload = {"title": day,
           "pages": [
               {
                   "title": "Lock of the Day",
                   "description": "Choose one team",
                   "position": 1,
                   "questions": [
                       {
                           "family": "single_choice",
                           "subtype": "vertical",
                           "answers": {
                               "choices": choices
                           },
                           "headings": [
                               {
                                   "heading": "Who is your lock of the day?"
                               }
                           ],
                           "position": 1
                       },
                       {
                           "family": "open_ended",
                           "subtype": "single",
                           "headings": [
                               {
                                   "heading": "What's your name?"
                               }
                           ],
                           "position": 2,
                       }
                   ]
               }
           ]
           }
response = s.post(url, json=payload)
print(response.json())

survey_id = response.json()["id"]
close_date = datetime.today().replace(hour=18,minute=0,second=0).strftime('%Y-%m-%dT%H:%M:%S-05:00')
payload = {
    "type": "weblink",
    "close_date": close_date
}
url = "https://api.surveymonkey.com/v3/surveys/%s/collectors" % survey_id
response = s.post(url, json=payload)
print(response.json())

# url = "https://api.surveymonkey.com/v3/surveys/%s/responses" % survey_id
# response = s.get(url, json={"per_page": 40})
# print(response.json())
