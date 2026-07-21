# Arcback

Arcback is a backtesting framework (in active development) for evaluating trading indicators and algorithms against historical financial market data. The end goal is to deliver detailed performance reports across stocks, forex, cryptocurrencies, and commodities.

> **Status:** Backend complete. The full backtesting pipeline — data ingestion, strategy signals, the event-driven engine, portfolio accounting, risk management, and performance analysis — is implemented and covered by a pytest suite. The frontend is the next phase.

---

## Features

### Implemented

- **Multi-source market data ingestion** via the [`Loader`](src/backend/data/loader.py) class
  - **Twelve Data API** — stocks, forex pairs, and cryptocurrencies (time series, EOD and intraday)
  - **Alpha Vantage API** — commodities (WTI, Brent, copper, wheat, aluminum, corn, cotton, sugar, coffee, natural gas)
  - Supported intraday + daily/weekly/monthly intervals (`1min` → `1month`)
  - Lookup of supported symbols per asset type
  - Robust HTTP error handling (connection errors, timeouts, HTTP errors, JSON decode errors, API-level error responses)
- **SQLite persistence layer** via the [`Processor`](src/backend/data/processor.py) class
  - Auto-initialized schema with three tables: `time_series_data`, `commodity_prices`, `last_updated`
  - Composite primary keys to prevent duplicate rows (`INSERT OR IGNORE`)
  - Context manager support for safe connection handling
  - Formatted output as pandas DataFrames ready for downstream processing
- **Interval-aware caching** via the [`DataManager`](src/backend/data/data_manager.py) coordinator
  - Tracks the date range already cached per `(symbol, interval)` pair in the `last_updated` table
  - Computes the missing date range and only fetches what isn't already in the local DB, minimizing redundant API calls
- **Strategy & indicators** via [`Algorithms`](src/backend/strategy/algorithms.py) and [`Indicators`](src/backend/strategy/indicators.py)
  - Indicator library (SMA, EMA, ATR, …) and a moving-average-crossover strategy that emits `1` / `-1` / `0` entry signals
- **Event-driven backtest engine** via the [`Engine`](src/backend/engine/engine.py) class
  - Bar-by-bar simulation over historical data for both time-series and commodity assets
  - Opens positions on entry signals, tracks open trades, and closes them on exit signals — returning populated positions and equity DataFrames
  - Positions modeled by the [`Positions`](src/backend/engine/positions.py) dataclass
- **Portfolio accounting** via the [`Portfolio`](src/backend/portfolio/portfolio.py) class — equity tracking and per-trade PnL adjustment across the backtest timeline
- **Risk management** via [`Entry`](src/backend/risk/entry.py), [`Exits`](src/backend/risk/exits.py), and [`Sizing`](src/backend/risk/sizing.py)
  - Volatility-targeted position sizing (risk-% + ATR multiplier)
  - ATR-based stop-loss / take-profit levels and exit checks
- **Performance analysis** via the [`Analysis`](src/backend/analysis/analysis.py) class
  - Final / high / low equity, gross & net revenue, equity % change
  - Win percentage, profit factor, risk/reward ratio, avg win/loss, winners/losers counts
  - Max drawdown, Sharpe ratio, average trade duration
- **Environment-based API key management** via [`Constants`](src/backend/constants.py) using `python-dotenv`
- **Test suite** — pytest coverage for every backend module under [`tests/test_backend/`](tests/test_backend/) (data, strategy, risk, engine, portfolio, analysis)

### Next phase

- **Frontend** — a web UI under [`src/frontend/`](src/frontend/) to configure backtests and visualize results (currently just `index.html`)

---

## Project Structure

```
Arcback/
├── requirements.txt
├── .env.example                    # Template for required API keys
├── reference_data/                 # Sample API response payloads (gitignored)
├── tests/
│   └── test_backend/               # pytest suite mirroring src/backend/
└── src/
    ├── backend/
    │   ├── constants.py            # API key loader (uses python-dotenv)
    │   ├── data/
    │   │   ├── loader.py           # Twelve Data + Alpha Vantage HTTP client
    │   │   ├── processor.py        # SQLite schema, inserts, queries
    │   │   └── data_manager.py     # Coordinates loader + processor with caching
    │   ├── strategy/
    │   │   ├── indicators.py       # SMA, EMA, ATR, …
    │   │   └── algorithms.py       # Signal-emitting strategies (MA crossover)
    │   ├── engine/
    │   │   ├── engine.py           # Event-driven bar-by-bar backtest loop
    │   │   └── positions.py        # Position dataclass
    │   ├── portfolio/
    │   │   └── portfolio.py        # Equity + PnL accounting
    │   ├── risk/
    │   │   ├── entry.py            # Entry checks, SL/TP levels
    │   │   ├── exits.py            # Exit checks
    │   │   └── sizing.py           # Volatility-targeted position sizing
    │   └── analysis/
    │       └── analysis.py         # Performance metrics
    └── frontend/                   # (next phase)
        └── index.html
```

---

## Installation

### Prerequisites

- Python 3.12+
- API keys for:
  - [Twelve Data](https://twelvedata.com/) — stocks, forex, crypto
  - [Alpha Vantage](https://www.alphavantage.co/) — commodities

### Setup

```bash
# Clone the repo
git clone https://github.com/<your-username>/Arcback.git
cd Arcback

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# then edit .env and fill in your keys
```

### `.env` format

```env
ALPHAVANTAGE_API_KEY=your_API_key_here
TWELVE_DATA_API_KEY=your_API_key_here
```

---

## Usage

> A CLI / configuration-driven runner and the frontend are not yet wired up; the backend is currently used programmatically.

### Running a full backtest

```python
from src.backend import DataManager, Algorithms, Engine, Analysis

# 1. Fetch, process, and cache market data
with DataManager() as dm:
    df = dm.get_formatted_time_series_data(symbol="NVDA", interval="1day")

# 2. Generate entry signals from a strategy
signals = Algorithms.ma_crossover(
    price_data=df["close"], dt_series=df.index, short_period=12, long_period=20
)

# 3. Run the event-driven backtest
engine = Engine(initial_equity=100_000.00, asset_type="tseries", interval="1day", symbol="NVDA")
positions_df, equity_df = engine.trade_entry_execution(
    signal_df=signals, risk_pct=0.01, atr_multiplier=2
)

# 4. Analyze results
analysis = Analysis(final_pos_df=positions_df, final_equity_df=equity_df)
print(analysis.final_equity(), analysis.net_revenue(), analysis.win_percentage())
print(analysis.drawdown(), analysis.sharpe_ratio(), analysis.profit_factor())
```

The first data fetch hits the API and populates the SQLite DB. Subsequent calls covering the same range are served entirely from the local cache; calls extending the range only fetch the missing window.

### Fetching commodities data

```python
from src.backend import DataManager

with DataManager() as dm:
    wti = dm.get_formatted_commodities_data(commodity_type="WTI", interval="daily")
    print(wti.head())
```

---

## Supported Assets & Intervals

### Twelve Data (stocks / forex / crypto)
Intervals: `1min`, `5min`, `15min`, `30min`, `45min`, `1h`, `2h`, `4h`, `8h`, `1day`, `1week`, `1month`

### Alpha Vantage (commodities)

| Commodity | Supported Intervals |
|---|---|
| WTI, Brent, Natural Gas | `daily`, `weekly`, `monthly` |
| Copper, Wheat, Aluminum, Corn, Cotton, Sugar, Coffee | `monthly`, `quarterly`, `annual` |

---

## Data Storage

A SQLite database (`financial_data.db`) is created next to [`processor.py`](src/backend/data/processor.py) on first run.

| Table | Columns | Primary Key |
|---|---|---|
| `time_series_data` | symbol, interval, datetime, open, high, low, close, volume | (symbol, datetime, interval) |
| `commodity_prices` | interval, commodity_type, date, price | (commodity_type, interval, date) |
| `last_updated` | symbol, interval, start_date, last_date | (symbol, interval) |

The DB file is gitignored.

---

## Tech Stack

- **Language:** Python 3.12+
- **HTTP:** `requests`
- **Storage:** `sqlite3` (stdlib)
- **Config:** `python-dotenv`
- **Numerics / data:** `numpy`, `pandas`
- **Testing:** `pytest`
- **Tooling:** `black` for formatting

---

## Roadmap

- [x] Twelve Data integration (stocks / forex / crypto)
- [x] Alpha Vantage integration (commodities)
- [x] SQLite persistence with composite primary keys
- [x] Interval-aware caching to skip redundant API calls
- [x] Strategy / indicator interface
- [x] Event-driven backtest engine
- [x] Portfolio and order management
- [x] Risk management (sizing, stops, exposure)
- [x] Performance analysis
- [x] Backend test suite (pytest)
- [ ] Frontend UI for configuring backtests and visualizing results
- [ ] CLI / configuration-driven runs

---

## License

[MIT](LICENSE) © 2026 Joshua J.