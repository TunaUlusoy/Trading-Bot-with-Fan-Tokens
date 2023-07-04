import pandas as pd
import requests

def get_fixture(team_name, url, querystring, headers):
    print(f"Getting {querystring['season']} fixture of {team_name}...")
    
    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    fixture_list = []
    for fixture in data["response"]:
        one_fixture = [fixture["fixture"]["id"], fixture["fixture"]["periods"]["first"], fixture["fixture"]["periods"]["second"], fixture["league"]["name"], fixture["teams"]["home"]["name"],
                    fixture["goals"]["home"], fixture["teams"]["away"]["name"], fixture["goals"]["away"]]
        fixture_list.append(one_fixture)

    fixture_df = pd.DataFrame(fixture_list,
                            columns=["Id", "FH_Start_Time", "SH_Start_Time", "League", "Home_Name", "Home_Goal", "Away_Name", "Away_Goal"])

    fixture_df["FH_Start_Time"] = pd.to_datetime(fixture_df["FH_Start_Time"], unit='s')
    fixture_df["SH_Start_Time"] = pd.to_datetime(fixture_df["SH_Start_Time"], unit='s')
    fixture_df.dropna(inplace=True)

    for column in fixture_df.columns:
        if fixture_df[column].dtype == "float64":
            fixture_df[column] = fixture_df[column].astype("int64")

    fixture_df = fixture_df.sort_values("FH_Start_Time")

    fixture_df.to_csv(f"fixture_csv/{team_name}_fixture.csv", index=False)
