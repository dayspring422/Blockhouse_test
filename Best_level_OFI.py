import numpy as np
import pandas as pd

# Reading the CSV file
file_path = 'first_25000_rows.csv'
df = pd.read_csv(file_path)

# Selecting only necessary columns needed to calculate Best-Level OFI
# Creates a new DataFrame with only these columns
ofi_df = df[['ts_event', 'bid_px_00', 'ask_px_00', 'bid_sz_00', 'ask_sz_00']].copy()

# Converting timestamp to datetime format for easier manipulation with pandas
ofi_df['ts_event'] = pd.to_datetime(ofi_df['ts_event'])

# Sorting the data by timestamp to ensure calculations are done in chronological order
ofi_df.sort_values('ts_event', inplace=True)

# Calculate the deltas (change from previous row)
bid_delta = ofi_df['bid_sz_00'].diff().fillna(0)          # Change in bid size
ask_delta = ofi_df['ask_sz_00'].diff().fillna(0)          # Change in ask size
bid_price_change = ofi_df['bid_px_00'].diff().fillna(0)   # Change in bid price
ask_price_change = ofi_df['ask_px_00'].diff().fillna(0)   # Change in ask price

# Applying the Best-Level OFI formula
# Count bid size increases only when bid price stays the same or increases
# Count ask size increases only when ask price stays the same or decreases
ofi = (bid_delta * (bid_price_change >= 0).astype(int)) - \
      (ask_delta * (ask_price_change <= 0).astype(int))

# Store OFI values in the DataFrame
ofi_df['best_level_ofi'] = ofi

# Display the result
print(ofi_df[['ts_event', 'best_level_ofi']])
