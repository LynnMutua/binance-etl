# Binance ETL

A lightweight Python ETL pipeline that fetches live cryptocurrency prices from Binance, converts them into Kenyan Shillings using an exchange rate from Frankfurter, and loads the results into a terminal table, JSON, CSV, or PostgreSQL.

## Overview

The application does the following:

- Fetches crypto prices from the Binance ticker API.
- Retrieves the USD/KES exchange rate from Frankfurter.
- Converts each asset price to KES using the formula:
  - price_kes = price_usdt × usd_kes_rate
- Outputs the data in one of these formats:
  - table (default console output)
  - json
  - csv
  - postgres

## Project structure

```text
.
├── app/
│   ├── extractor.py   # Binance and Frankfurter API calls
│   ├── loader.py      # Output formatting and database loading
│   ├── transformer.py # conversion logic
│   └── test.ipynb    # exploratory notebook
├── data/              # CSV output directory
├── main.py            # CLI entry point
├── docker-compose.yml # Postgres + app service setup
├── Dockerfile         # container image definition
├── .env               # environment variables
├── pyproject.toml     # project metadata and dependencies
├── requirements.txt   # pip dependencies
├── uv.lock            # lock file for uv
└── README.md          # project documentation
```

## Requirements

- Python 3.14+
- Optional: uv for package management
- PostgreSQL for the `postgres` output mode

## Setup

### 1) Create a virtual environment

Using uv:

```bash
uv sync
```

Or using venv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment variables

Create a `.env` file in the project root with values similar to:

```env
Binance=https://api.binance.com/api/v3/ticker/price
Frankfurter=https://api.frankfurter.dev/v2/rate/USD/KES
POSTGRES_PASSWORD=your_password
```

For PostgreSQL, the app also reads the following optional environment variables:

```env
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=crypto
POSTGRES_USER=postgres
```

## Usage

Run the ETL from the command line:

```bash
python main.py --symbol BTCUSDT ETHUSDT BNBUSDT --output table
```

### Supported output formats

- `table` — prints a formatted console table
- `json` — prints JSON to stdout
- `csv` — saves a CSV file to `data/crypto_prices.csv`
- `postgres` — writes to PostgreSQL using SQLAlchemy

### Example commands

```bash
# Console table output
python main.py --symbol BTCUSDT --output table

# JSON output
python main.py --symbol BTCUSDT ETHUSDT --output json

# CSV output
python main.py --symbol BTCUSDT ETHUSDT --output csv

# PostgreSQL output
python main.py --symbol BTCUSDT ETHUSDT --output postgres
```

Note: `--symbol` accepts one or more symbols and can be passed as repeated flags or as a comma-separated string.

## Docker

This repo includes a Docker Compose setup for PostgreSQL and the ETL app.

### Start services

```bash
docker compose up --build
```

The default Compose command runs:

```yaml
command: ["--symbol", "BTCUSDT", "ETHUSDT", "BNBUSDT", "--output", "postgres"]
```

This starts:

- a PostgreSQL database on port `5433`
- the ETL application, which pushes results to the database

## Example output

```text
---------------------------------------------------------------
SYMBOL         USDT PRICE             APPROXIMATE KES
---------------------------------------------------------------
BTCUSDT        $62,000.00            KSh 8,555,000.00
ETHUSDT        $3,200.00             KSh 441,600.00
---------------------------------------------------------------
```

## Notes

- The app expects valid Binance symbols such as `BTCUSDT`, `ETHUSDT`, or `BNBUSDT`.
- If the exchange rate or API request fails, the script exits with an error.
- CSV output is saved under `data/` and PostgreSQL writes to the `crypto_prices` table.

## License

This project is provided as-is for local ETL experimentation and learning purposes.
