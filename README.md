# Order Flow Imbalance (OFI) Calculator

This project is a lightweight Python tool designed to compute Order Flow Imbalance (OFI) from high-frequency order book data. It supports both best-level (Level 00) and multi-level OFI calculations and offers flexible weighting options like linear, exponential, or equal weights.

OFI is a useful feature in algorithmic trading and market microstructure research. It helps capture the pressure from buying and selling orders at various levels of the order book.

## What It Does

- Reads order book data from a CSV file
- Calculates both best-level and aggregated multi-level OFI
- Supports different weighting schemes to reflect order book depth
- Prints the results directly to your console for quick analysis

## How It Works

The script processes each snapshot in your dataset and computes the net pressure from bid and ask changes. You can choose how many levels to include (e.g., top 5 levels) and how heavily to weight each one.

## Getting Started

### Requirements
- Python 3.x
- pandas
- numpy

Author
Dayspring Idahosa
Computer Science & Physics Major
Stetson University | Presidential Fellow

