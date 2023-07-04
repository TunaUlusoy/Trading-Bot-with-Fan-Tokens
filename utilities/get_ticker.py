import os
import datetime
import requests
import json
import pandas as pd
import time

def get_ticker(team_name, url, symbol, interval, startTime, endTime):
    print(f"Getting OHLC of {symbol} ticker...")
    currentTime = startTime

    csv_index = 1
    while currentTime <= endTime:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": currentTime,
            "endTime": endTime
        }

        response = requests.get(url, params=params)

        data = json.loads(response.text)

        df = pd.DataFrame(data)
        df = df[[0, 1, 2, 3, 4, 6]]
        df.columns = ["Open Time", "Open", "High", "Low", "Close", "Close Time"]

        df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
        df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')

        csv_num = "{:02d}".format(csv_index)

        csv_path = "ticker_csv/{}/1_mn".format(team_name)

        if not os.path.exists(csv_path):
            os.mkdir(os.path.join(os.getcwd(), csv_path))

        df.to_csv("{}/{}_ticker_{}.csv".format(csv_path, team_name, csv_num), index=False)

        csv_index += 1
        currentTime += int(datetime.timedelta(hours=8).total_seconds() * 1000)
        
        time.sleep(1)


