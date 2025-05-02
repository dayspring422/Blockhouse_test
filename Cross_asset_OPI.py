import numpy as np
import pandas as pd
from datetime import datetime
import os

def calculate_single_asset_ofi(df, levels=5, weighting_scheme='linear'):
    """
    Calculate OFI for a single asset (best levels + multi-level)
    """
    ofi_df = df[['ts_event']].copy()
    ofi_df['best_level_ofi'] = 0  # Best bid/ask OFI (level 00)
    ofi_df['multi_level_ofi'] = 0  # Weighted OFI across multiple levels

    # Calculate weights for multi-level OFI
    if weighting_scheme == 'linear':
        weights = [1/(i+1) for i in range(levels)]  # Linear decay
    elif weighting_scheme == 'exponential':
        weights = [np.exp(-i) for i in range(levels)]  # Exponential decay
    else:  # equal weighting
        weights = [1 for _ in range(levels)]

    weights = np.array(weights) / sum(weights)  # Normalize

    # Calculate OFI for each level
    for i in range(levels):
        bid_px = f'bid_px_{i:02d}'
        ask_px = f'ask_px_{i:02d}'
        bid_sz = f'bid_sz_{i:02d}'
        ask_sz = f'ask_sz_{i:02d}'

        if not all(col in df.columns for col in [bid_px, ask_px, bid_sz, ask_sz]):
            print(f"Stopping at level {i} (columns missing)")
            break

        bid_delta = df[bid_sz].diff().fillna(0)
        ask_delta = df[ask_sz].diff().fillna(0)
        bid_price_change = df[bid_px].diff().fillna(0)
        ask_price_change = df[ask_px].diff().fillna(0)

        level_ofi = (bid_delta * (bid_price_change >= 0).astype(int)) - \
                    (ask_delta * (ask_price_change <= 0).astype(int))

        ofi_df['multi_level_ofi'] += level_ofi * weights[i]

        if i == 0:
            ofi_df['best_level_ofi'] = level_ofi

    return ofi_df

# Main execution
if __name__ == "__main__":
    file_path = 'first_25000_rows.csv'

    # Read data
    df = pd.read_csv(file_path)

    # Convert timestamp
    df['ts_event'] = pd.to_datetime(df['ts_event'])

    # Sort by time
    df.sort_values('ts_event', inplace=True)

    # Calculate OFI
    ofi_results = calculate_single_asset_ofi(df, levels=5, weighting_scheme='linear')

    # Save results
    output_file = 'ofi_results.csv'
   # ofi_results.to_csv(output_file, index=False)

    print(f"\nSuccess! Results saved to '{output_file}'")
    print("\nFirst 5 rows:")
    print(ofi_results.head())
