import time
import requests
import pandas as pd

from datetime import timedelta

def get_goal(team_name, url, querystring, headers):
    print(f"Getting {querystring['season']} goals of {team_name}...")
    
    fixture_df = pd.read_csv(f"fixture_csv/{team_name}_fixture.csv")

    goal_time_dict = {}

    for _, row in fixture_df.iterrows():
        querystring = {"fixture": row["Id"]}

        while True:
            events = requests.get(url, headers=headers, params=querystring)    
            if events.status_code != 200:
                print("Access error...")
            else:
                events = events.json()
                if events["results"] != 0:
                    break
                else:
                    time.sleep(2)

        our_goal_list = []
        other_goal_list = []

        for i in events["response"]:
            if i["type"] == "Goal":
                if i["team"]["name"] == team_name:
                    if i["time"]["elapsed"] <= 45:
                        our_goal_list.append(pd.to_datetime(row["FH_Start_Time"]) + timedelta(minutes = i["time"]["elapsed"]))
                    else:
                        our_goal_list.append(pd.to_datetime(row["SH_Start_Time"]) + timedelta(minutes = i["time"]["elapsed"] - 45))
                else:
                    other_goal_list.append(i["time"]["elapsed"])
            
            if len(our_goal_list) > len(other_goal_list):
                goal_time_dict[row["FH_Start_Time"]] = our_goal_list

        if len(our_goal_list) > len(other_goal_list):
            our_goal_list.append(pd.to_datetime(row["SH_Start_Time"]) + timedelta(minutes=50))
            goal_time_dict[row["FH_Start_Time"]] = our_goal_list

        time.sleep(2)

    for key, value in goal_time_dict.items():
        goal_time_dict[key] = [value]
    
    goal_time_df = pd.DataFrame(goal_time_dict)
    goal_time_df = goal_time_df.T
    goal_time_df.columns = ["Goal_Times"]

    goal_time_df.to_csv(f"goal_csv/{team_name}_goal.csv", index=True)