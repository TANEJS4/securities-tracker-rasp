# Real-Time Yahoo Finance Quotes Tracker

This script provides a real-time terminal dashboard for tracking live price and volume updates of selected financial symbols (e.g., cryptocurrencies) using Yahoo Finance data. It leverages `yfinance` for data streaming and `rich` for a visually appealing, interactive display.

## Features

- Live price and volume updates for specified symbols
- Color-coded price changes (green for gains, red for losses)
- Gain/loss calculation based on configurable book values
- Responsive terminal UI with current time

## Requirements

- Python 3
- `yfinance` (with websocket support)
- `rich`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Edit the `SYMBOLS` dictionary in `real_time_quotes.py` to specify the symbols and their book values.
2. Run the script:

```bash
python real_time_quotes.py
```

3. View the live dashboard in your terminal. Press `Ctrl+C` to exit gracefully.

## Example Output

```
📈 Live Yahoo Finance Ticker Stream
┏━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┓
┃ Symbol   ┃ Price    ┃ Volume   ┃ Gain   ┃
┡━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━┩
│ BTC-USD  │ $ 34500  │ 1200     │ +500.00│
│ ETH-USD  │ $ 1800   │ 800      │ ±0     │
└──────────┴──────────┴──────────┴────────┘
🕰️ 12:34:56
```

## Notes

- The script uses Yahoo Finance's websocket API for real-time updates.
- Book values are optional; if not set, gain/loss will show as ±0.
- You can add or remove symbols by editing the `SYMBOLS` dictionary.
