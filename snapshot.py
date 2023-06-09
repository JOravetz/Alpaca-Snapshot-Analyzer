#!/usr/bin/python3

import os
import argparse
from alpaca_trade_api.rest import REST

# Load Alpaca API credentials from the environment variables
API_KEY_ID = os.environ["APCA_API_KEY_ID"]
SECRET_KEY_ID = os.environ["APCA_API_SECRET_KEY"]
BASE_URL = os.environ["APCA_API_BASE_URL"]

rest_api = REST(API_KEY_ID, SECRET_KEY_ID, BASE_URL)


def run(args):
    """
    This function fetches stock market data for a list of symbols provided in a file or for all active symbols if no list is provided.
    It then calculates various metrics and prints them out.

    Args:
        args: Command line arguments parsed by argparse.ArgumentParser
    """

    symbol_list = str(args.list)

    # Check if a symbol list was provided
    if symbol_list:
        # Open the list file and read all symbols into a list
        with open(symbol_list + ".lis", "r") as file:
            universe = [row.split()[0].upper() for row in file if row.strip() != ""]
    else:
        # If no list was provided, fetch all active symbols from Alpaca
        universe = [el.symbol for el in rest_api.list_assets(status="active") if len(el.symbol) < 5]

    # Fetch snapshot data for all symbols in the universe
    snapshots = rest_api.get_snapshots(universe)

    # For each symbol in the universe, calculate various metrics and print them out
    for symbol in universe:
        try:
            snapshot = snapshots.get(symbol)
            price_now = snapshot.latest_trade.price
            prev_close = snapshot.prev_daily_bar.close
            low = snapshot.daily_bar.low
            high = snapshot.daily_bar.high
            percent = ((price_now - prev_close) / prev_close) * 100
            percent_low = ((price_now - low) / low) * 100
            percent_high = ((price_now - high) / high) * 100
            volume = int(snapshot.daily_bar.volume)

            print(f"{symbol: <6} {price_now:9.3f} {percent:9.3f} {percent_low:8.3f} {percent_high:8.3f} {volume:10d}")

        except Exception as e:
            continue


if __name__ == "__main__":

    # Create a command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", type=str, default="", help="Symbol list (default=None)")

    # Parse command line arguments
    arguments = parser.parse_args()

    # Run the main function
    run(arguments)
