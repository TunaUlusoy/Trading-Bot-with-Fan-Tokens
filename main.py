import os
import pandas as pd

from dotenv import load_dotenv
from pandas import Timestamp
from datetime import datetime, timedelta

from utilities.get_ticker import get_ticker
from utilities.dicts import teams, symbols, startTimes
from utilities.fixture import get_fixture
from utilities.goal import get_goal
from utilities.merge_ticker_csv_files import merge_ticker_csv_files


############################# changables #############################
team_name = "FC Porto" # "Lazio", "FC Porto", "Santos", "Galatasaray" 

fixture_flag = True
goal_flag = True
ticker_flag = True
merge_tickers_flag = True
manipulation_flag = True

time_list = []

season = 2022


############################# definitions #############################
# Load the environment variables from the .env file
load_dotenv()

fixture_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
event_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/events"

querystring = {"team": teams[team_name], "season": season}

# Access the API-FOOTBALL key and host
api_football_key = os.getenv("X-RapidAPI-Key")
api_football_host = os.getenv("X-RapidAPI-Host")

headers = {
	"content-type": "application/octet-stream",
	"X-RapidAPI-Key": api_football_key,
	"X-RapidAPI-Host": api_football_host
}

binance_url = "https://api.binance.com/api/v3/klines"

symbol = symbols[team_name]
interval = "1m" 
startTime = startTimes[team_name]
endTime = int(datetime.now().timestamp()*1000)


############################# get fixture #############################
if fixture_flag:
    get_fixture(team_name, fixture_url, querystring, headers)


############################# get goal #############################
if goal_flag:
    get_goal(team_name, event_url, querystring, headers)


############################# get tickers #############################
if not os.path.exists(os.path.join(os.getcwd(), f"ticker_csv/{team_name}/1_mn")):
    os.makedirs(os.path.join(os.getcwd(), f"ticker_csv/{team_name}/1_mn"))

if ticker_flag:
    get_ticker(team_name, binance_url, symbol, interval, startTime, endTime)


############################# merge ticker csv files #############################
if merge_tickers_flag:
    merge_ticker_csv_files(team_name, symbol)


############################## read csv files #############################
ticker_df = pd.read_csv(f"ticker_csv/{team_name}/1_mn/{team_name}_ticker.csv")
fixture_df = pd.read_csv(f"fixture_csv/{team_name}_fixture.csv")
goal_df = pd.read_csv(f"goal_csv/{team_name}_goal.csv")


############################## manipulations #############################
if manipulation_flag:
    # ticker manipulation 
    print("Ticker manipulation has started...")

    ticker_df = ticker_df[["Open Time", "Open"]]

    ticker_df["Open Time"] = pd.to_datetime(ticker_df["Open Time"])

    ticker_df.columns = ["Time", "Price"]

    # goal manipulation
    print("Goal manipulation has started...")
    
    for times in goal_df["Goal_Times"]:
        times = times[1:-1]
        times = times.split(", ")
        times = [Timestamp(eval(i)).to_pydatetime() for i in times]
        for i in times:
            time_list.append(i)

    # trade csv
    print(f"{team_name}_trade.csv has been creating...")
    
    # buy
    buy_time_s = pd.Series(time_list, name='Time')

    buy_df = pd.merge(ticker_df, buy_time_s, on='Time')

    buy_df.columns = ["Buy_Time", "Buy_Price"]

    # sell
    sell_time_s = pd.to_datetime(buy_df["Buy_Time"]) + timedelta(minutes=5)
    sell_time_s = sell_time_s.rename("Time")

    sell_df = pd.merge(ticker_df, sell_time_s, on='Time')

    sell_df.columns = ["Sell_Time", "Sell_Price"]
    
    # trade
    merged_df = pd.concat([buy_df, sell_df], axis=1)

    time_list = []
    price_list = []
    order_list = []
    for _, row in merged_df.iterrows():
        time_list.append(row["Buy_Time"])
        time_list.append(row["Sell_Time"])
        price_list.append(row["Buy_Price"])
        price_list.append(row["Sell_Price"])
        order_list.append(1)
        order_list.append(-1)

    merged_df = pd.DataFrame([time_list, price_list, order_list]).T
    merged_df.columns = ["Datetime", "Price", "Order"]

    merged_df.to_csv(f"trade_csv/{team_name}_trade.csv", index=False)

   
############################## profit/loss #############################
print(f"Profit/Loss has been calculating...")

trade_df = pd.read_csv(f"trade_csv/{team_name}_trade.csv")

first_money = 100

last_money = first_money

for index, row in trade_df.iterrows():
   if row["Order"] == 1:
       quantity = last_money / row["Price"]
   elif row["Order"] == -1:
       last_money = quantity * row["Price"]

if last_money/first_money < 1:
   print("\nTotal Loss : %{:.2f}".format((1.0-(last_money/first_money))*100))
else:
   print("\nTotal Profit : %{:.2f}".format((last_money/first_money-1.0)*100))
