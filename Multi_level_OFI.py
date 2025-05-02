import numpy as np
import pandas as pd

# Reading the CSV file
file_path = 'first_25000_rows.csv'
df = pd.read_csv(file_path)

# Selecting columns for multiple levels (assuming your data has levels 00-09)
# Adjust the range if you have fewer or more levels
levels = range(10)  # from 00 to 09
level_cols = []

# Create lists of all relevant columns
for i in levels:
    level_cols.extend([
        f'bid_px_{i:02d}',
        f'ask_px_{i:02d}',
        f'bid_sz_{i:02d}',
        f'ask_sz_{i:02d}'
    ])

# Create a new DataFrame with these columns plus timestamp
multi_ofi_df = df[['ts_event'] + level_cols].copy()

# Convert timestamp to datetime
multi_ofi_df['ts_event'] = pd.to_datetime(multi_ofi_df['ts_event'])

# Sort by timestamp
multi_ofi_df.sort_values('ts_event', inplace=True)

# Initialize OFI column
multi_ofi_df['multi_level_ofi'] = 0

# Calculate OFI for each level and sum them up
for i in levels:
    # Get column names for current level
    bid_px = f'bid_px_{i:02d}'
    ask_px = f'ask_px_{i:02d}'
    bid_sz = f'bid_sz_{i:02d}'
    ask_sz = f'ask_sz_{i:02d}'

    # Calculate deltas
    bid_delta = multi_ofi_df[bid_sz].diff().fillna(0)
    ask_delta = multi_ofi_df[ask_sz].diff().fillna(0)
    bid_price_change = multi_ofi_df[bid_px].diff().fillna(0)
    ask_price_change = multi_ofi_df[ask_px].diff().fillna(0)

    # Calculate OFI for this level
    level_ofi = (bid_delta * (bid_price_change >= 0).astype(int)) - \
                (ask_delta * (ask_price_change <= 0).astype(int))

    # Add to the total OFI (you might want to weight different levels)
    multi_ofi_df['multi_level_ofi'] += level_ofi

# Display the result
print(multi_ofi_df[['ts_event', 'multi_level_ofi']])