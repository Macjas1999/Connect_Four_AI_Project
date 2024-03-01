import os
import pandas as pd
import numpy as np

def merge_csv(files, output_file):
    # Create an empty DataFrame to store the combined data
    combined_data = pd.DataFrame()

    # Iterate over the list of CSV files and concatenate them
    for file in files:
        df = pd.read_csv(file, index_col=None, header=None)
        combined_data = pd.concat([combined_data, df], ignore_index=True)

    # Write the combined DataFrame to a new CSV file
    combined_data.to_csv(output_file, index=False, header=False)

def remove_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")

if __name__ == "__main__":
    input_files = ["resultextract_player_2_v2.csv", "resultextract_player_2_v3.csv", "resultextract_player_2_v4.csv", "resultextract_player_2_v5.csv"]  # Add your CSV file names here
    output_file = "resultextract_player_2_v6.csv"  # Output file name

    merge_csv(input_files, output_file)




