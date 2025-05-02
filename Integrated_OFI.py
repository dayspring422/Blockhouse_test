import numpy as np
import pandas as pd

file_path = 'first_25000_rows.csv'
df = pd.read_csv(file_path)

def calculate_integrated_ofi(file_path, levels=10, weighting_scheme='linear'):
    """
    Calculate Integrated OFI from raw data file

    Parameters:
    - file_path: path to CSV file with order book data
    - levels: number of order book levels to consider
    - weighting_scheme: 'linear', 'exponential', or 'equal' weighting

    Returns:
    - DataFrame with integrated OFI values
    """

    # Read the data
    df = pd.read_csv(file_path)

    # Prepare the DataFrame
    ofi_df = df[['ts_event']].copy()
    ofi_df['ts_event'] = pd.to_datetime(ofi_df['ts_event'])
    ofi_df.sort_values('ts_event', inplace=True)

    # Initialize OFI columns
    ofi_df['integrated_ofi'] = 0

    # Calculate weights based on the scheme
    if weighting_scheme == 'linear':
        weights = [1/(i+1) for i in range(levels)]  # Linear decay
    elif weighting_scheme == 'exponential':
        weights = [np.exp(-i) for i in range(levels)]  # Exponential decay
    else:  # equal weighting
        weights = [1 for _ in range(levels)]

    # Normalize weights to sum to 1
    weights = np.array(weights) / sum(weights)

    # Calculate OFI for each level and integrate
    for i in range(levels):
        # Get column names (with zero-padding)
        bid_px = f'bid_px_{i:02d}'
        ask_px = f'ask_px_{i:02d}'
        bid_sz = f'bid_sz_{i:02d}'
        ask_sz = f'ask_sz_{i:02d}'

        # Verify columns exist
        if not all(col in df.columns for col in [bid_px, ask_px, bid_sz, ask_sz]):
            print(f"Warning: Level {i} columns not found. Using available levels.")
            break

        # Calculate deltas
        bid_delta = df[bid_sz].diff().fillna(0)
        ask_delta = df[ask_sz].diff().fillna(0)
        bid_price_change = df[bid_px].diff().fillna(0)
        ask_price_change = df[ask_px].diff().fillna(0)

        # Calculate OFI for this level
        level_ofi = (bid_delta * (bid_price_change >= 0).astype(int)) - \
                    (ask_delta * (ask_price_change <= 0).astype(int))

        # Add weighted OFI to integrated OFI
        ofi_df['integrated_ofi'] += level_ofi * weights[i]

    return ofi_df

file_path = 'first_25000_rows.csv'
integrated_ofi_result = calculate_integrated_ofi(file_path, levels=5, weighting_scheme='exponential')
print(integrated_ofi_result.head())