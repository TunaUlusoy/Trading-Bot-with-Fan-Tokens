import os
import pandas as pd

def merge_ticker_csv_files(team_name, symbol):
    print(f"Merging csv files of {symbol} ticker...")
    csv_files_path = os.path.join(os.getcwd(), f"ticker_csv/{team_name}/1_mn")

    csv_files = []
    for file in os.listdir(csv_files_path):
        df = pd.read_csv(os.path.join(csv_files_path, file))
        csv_files.append(df)

    merged_df = pd.concat(csv_files, ignore_index=True)

    merged_df = merged_df.sort_values("Open Time")
    merged_df = merged_df.drop_duplicates()

    merged_df.to_csv(f"ticker_csv/{team_name}/1_mn/{team_name}_ticker.csv", index=False)