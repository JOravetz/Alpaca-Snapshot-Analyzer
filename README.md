# Alpaca Snapshot Analyzer

The Alpaca Snapshot Analyzer is a Python script that fetches and analyzes stock snapshots using the Alpaca API. It provides real-time and historical data insights for multiple symbols, including trade, quote, minute bar, daily bar, and previous daily bar information.

With the Alpaca Snapshot Analyzer, you can easily retrieve key data points for stocks and extract relevant information such as timestamps, prices, volumes, and more. The script offers flexibility in filtering data by type, allowing you to focus on specific aspects of the stock snapshots.

Getting started is simple. You just need Python 3.x installed on your machine and valid Alpaca API credentials, including an API key ID and secret key ID. Optionally, you can provide a stock symbol list file to analyze specific stocks. Once set up, the script fetches the snapshots, processes the data, and presents the results in a structured format for further analysis or reporting.

## Key Features

- Fetch stock snapshots for multiple symbols simultaneously.
- Extract trade, quote, minute bar, daily bar, and previous daily bar data.
- Filter the data by type to focus on specific subsets.
- Sort the output by any available column.
- Omit specific columns from the output.
- Output the processed data in a structured format for easy analysis.

The Alpaca Snapshot Analyzer is designed for traders, investors, and analysts who require detailed and up-to-date stock data. It provides valuable insights for making informed decisions, identifying trends, and performing data-driven analysis.

Contributions to the Alpaca Snapshot Analyzer project are welcome. If you encounter any issues, have suggestions for improvements, or would like to contribute new features, please feel free to open an issue or submit a pull request.

The project is open source and released under the MIT License, allowing you to modify, distribute, and use the code according to the license terms.

Get started with the Alpaca Snapshot Analyzer today and gain valuable insights into stock snapshots to enhance your trading and investment strategies.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed on your machine.
- Alpaca API credentials (API key ID and secret key ID).
- Stock symbol list file (optional).

## Installation

1. Clone this repository to your local machine:

```
git clone https://github.com/JOravetz/alpaca-snapshot-analyzer.git
```
2. Install the required dependencies using pip:

```
pip install -r requirements.txt
```

3. Set up your Alpaca API credentials by exporting them as environment variables:

```
export APCA_API_KEY_ID=<your-api-key-id>
export APCA_API_SECRET_KEY=<your-secret-key-id>
export APCA_API_BASE_URL=<base-url>
```

## Usage

1. Run the script with the desired options:

```
python snapshot_analyzer.py [-l <symbol-list-file>] [-t <data-type>] [-s <sort-by>] [-o <sort-order>] [-oc <omit-columns>]
```

- <symbol-list-file> (optional): Path to the file containing the stock symbols.
- <data-type> (optional): Type of data to output (all, trade, quote, minute_bar, daily_bar, prev_daily_bar).
- <sort-by> (optional): Column to sort the output by. Default is 'symbol'.
- <sort-order> (optional): Order to sort the output in. Default is 'ascending'.
- <omit-columns> (optional): Comma-separated list of columns to omit from the output.

If a stock symbol list file is not provided, the script will use active symbols with a symbol length less than 5.

2. The script will fetch the snapshots, process the data, and output the results in a structured format.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

