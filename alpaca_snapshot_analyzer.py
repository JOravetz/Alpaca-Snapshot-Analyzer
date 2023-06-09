import os
import argparse
import pandas as pd
from alpaca_trade_api import REST
from alpaca_trade_api.rest import APIError

# Set pandas display options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# Load Alpaca API credentials from the environment variables
API_KEY_ID = os.getenv("APCA_API_KEY_ID")
SECRET_KEY_ID = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_API_BASE_URL")

# Create REST API instance
rest_api = REST(API_KEY_ID, SECRET_KEY_ID, BASE_URL)


def fetch_snapshots(symbols):
    """Fetch snapshots for given symbols.

    Args:
        symbols: List of symbols.

    Returns:
        A dictionary with symbols as keys and snapshot objects as values.
    """
    try:
        snapshots = rest_api.get_snapshots(symbols)
    except APIError as e:
        print(f"Failed to fetch snapshots: {e}")
        return {}
    return snapshots


def process_snapshot(symbol, snapshot):
    """Process a snapshot to extract relevant data.

    Args:
        symbol: The symbol of the snapshot.
        snapshot: The snapshot object.

    Returns:
        A dictionary with the processed data.
    """
    # Mapping for different data types within a snapshot
    base_mapping = {
        "t": "timestamp",
        "c": "conditions",
    }

    trade_mapping = {
        **base_mapping,
        "i": "id",
        "x": "exchange",
        "p": "price",
        "s": "size",
        "z": "tape",
    }
    quote_mapping = {
        **base_mapping,
        "ax": "ask_exchange",
        "ap": "ask_price",
        "as": "ask_size",
        "bx": "bid_exchange",
        "bp": "bid_price",
        "bs": "bid_size",
        "z": "tape",
    }
    bar_mapping = {
        **base_mapping,
        "o": "open",
        "h": "high",
        "l": "low",
        "c": "close",
        "v": "volume",
        "n": "trade_count",
        "vw": "vwap",
    }

    if snapshot is None:
        return {}

    trade_data = (
        {
            trade_mapping[key]: getattr(snapshot.latest_trade, key)
            for key in trade_mapping
            if hasattr(snapshot.latest_trade, key)
        }
        if snapshot.latest_trade
        else {}
    )
    quote_data = (
        {
            quote_mapping[key]: getattr(snapshot.latest_quote, key)
            for key in quote_mapping
            if hasattr(snapshot.latest_quote, key)
        }
        if snapshot.latest_quote
        else {}
    )
    minute_bar_data = (
        {
            bar_mapping[key]: getattr(snapshot.minute_bar, key)
            for key in bar_mapping
            if hasattr(snapshot.minute_bar, key)
        }
        if snapshot.minute_bar
        else {}
    )
    daily_bar_data = (
        {
            bar_mapping[key]: getattr(snapshot.daily_bar, key)
            for key in bar_mapping
            if hasattr(snapshot.daily_bar, key)
        }
        if snapshot.daily_bar
        else {}
    )
    prev_daily_bar_data = (
        {
            bar_mapping[key]: getattr(snapshot.prev_daily_bar, key)
            for key in bar_mapping
            if hasattr(snapshot.prev_daily_bar, key)
        }
        if snapshot.prev_daily_bar
        else {}
    )

    return {
        "symbol": symbol,
        "trade": trade_data,
        "quote": quote_data,
        "minute_bar": minute_bar_data,
        "daily_bar": daily_bar_data,
        "prev_daily_bar": prev_daily_bar_data,
    }


def fetch_and_process(symbols):
    """Fetch and process snapshots for given symbols.

    Args:
        symbols: List of symbols.

    Returns:
        A pandas DataFrame with the processed data.
    """
    snapshots = fetch_snapshots(symbols)
    data = [
        process_snapshot(symbol, snapshot)
        for symbol, snapshot in snapshots.items()
    ]
    return pd.json_normalize(data, sep="_")


def filter_data(df, data_type):
    """Filter data by type.

    Args:
        df: A pandas DataFrame with the data.
        data_type: The type of data to filter by.

    Returns:
        A filtered pandas DataFrame.
    """
    if data_type != "all":
        columns_to_keep = ["symbol"] + df.columns[df.columns.str.contains(data_type, case=False)].tolist()
        df = df[columns_to_keep]
    if not df.empty and "symbol" in df.columns:
        df = df[["symbol"] + [col for col in df.columns if col != "symbol"]]
    return df


def get_symbols_from_file(file_path):
    """Get symbols from a file.

    Args:
        file_path: The path to the file.

    Returns:
        A list of symbols, or None if the file does not exist or is empty.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return None

    with open(file_path, "r") as file:
        symbols = [line.strip().upper() for line in file]

    if not symbols:
        print(f"File {file_path} is empty.")
        return None

    return symbols

def main(args):
    """Main function to run the script.

    Args:
        args: Command line arguments.
    """
    symbols = None
    if args.list:
        if not os.path.exists(args.list):
            print(f"Stock symbol list file {args.list} does not exist.")
            return
        symbols = get_symbols_from_file(args.list)

    if not symbols:
        symbols = [
            el.symbol
            for el in rest_api.list_assets(status="active")
            if len(el.symbol) < 5
        ]

    df = fetch_and_process(symbols)
    df = filter_data(df, args.type)

    # Drop rows with NaN values
    df.dropna(inplace=True)

    # Sort the dataframe
    df = df.sort_values(by=args.sort_by, ascending=(args.sort_order == "ascending"))

    # Omit specified columns
    if args.omit_columns:
        columns_to_omit = args.omit_columns.split(',')
        df = df.drop(columns=columns_to_omit, errors='ignore')

    print(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--list",
        required=False,
        help="Path to the file containing the stock symbols",
    )
    parser.add_argument(
        "-t",
        "--type",
        default="all",
        choices=[
            "all",
            "trade",
            "quote",
            "minute_bar",
            "daily_bar",
            "prev_daily_bar",
        ],
        help="Type of data to output",
    )
    parser.add_argument(
        "-s",
        "--sort-by",
        default="symbol",
        help="Column to sort the output by. Default is 'symbol'.",
    )
    parser.add_argument(
        "-o",
        "--sort-order",
        default="ascending",
        choices=["ascending", "descending"],
        help="Order to sort the output in. Default is 'ascending'.",
    )
    parser.add_argument(
        "-oc",
        "--omit-columns",
        default="",
        help="Comma-separated list of column names to omit from the output.",
    )
    args = parser.parse_args()
    main(args)
