import asyncio
from collections import defaultdict
from datetime import datetime
from yfinance import AsyncWebSocket, download  
from rich.table import Table
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.align import Align

# Configurable items
SYMBOLS = {
    "BTC-USD": 100000,   # example book value
    "ETH-USD": None,    # example book value
}
# BLINK_DURATION = 1.0  # seconds

latest_data = defaultdict(dict)
previous_prices = {} 
flash_state = {} 

console = Console()


def preload_prices(symbols):

    tickers  = download(symbols, period="1d", interval="1m", progress=False, threads=True)
    if isinstance(tickers, tuple) or tickers.empty: # type: ignore
        console.print("[red]Failed to fetch initial data[/red]")
        return

    latest_row = tickers.tail(1) # type: ignore
    for sym in symbols:
        try:
            price = float(latest_row["Close"][sym].iloc[0])
            volume = int(latest_row["Volume"][sym].iloc[0])
            latest_data[sym] = {"price": price, "volume": volume}
            previous_prices[sym] = price
            
        except Exception:
            latest_data[sym] = {"price": "N/A", "volume": "N/A"}
            previous_prices[sym] = None


async def handle_message(msg: dict):

    symbol = msg.get("id", None)
    price = msg.get("price", 0)
    volume = msg.get("dayVolume", 0)

    latest_data[symbol] = {"price": price, "volume": volume}

    # Get previous price first
    prev_price = latest_data.get(symbol, {}).get("price")
    previous_prices[symbol] = prev_price
    # if isinstance(price, (int, float)) and isinstance(prev_price, (int, float)):
    #     if price > prev_price:
    #         flash_state[symbol] = {"color": "bright_green", "until": datetime.now() + timedelta(seconds=BLINK_DURATION)}
    #     elif price < prev_price:
    #         flash_state[symbol] = {"color": "bright_red", "until": datetime.now() + timedelta(seconds=BLINK_DURATION)}


def render_table():
    table = Table(title=f"📈 Live Yahoo Finance Ticker Stream ",
                title_style="bold cyan",
                header_style="bold white",
                # min_width=50,  # min   width
                expand=True
    )

    table.add_column("Symbol", style="white bold", justify="center")
    table.add_column("Price", style="green bold", justify="right")
    table.add_column("Volume", style="gray35", justify="right")
    table.add_column("Gain", justify="right")  
    now = datetime.now()
    
    for sym, book_value in SYMBOLS.items():
        data = latest_data.get(sym, {})
        price = data.get("price", "N/A")
        volume = data.get("volume", "N/A")

        prev = previous_prices.get(sym)
        color = "white"
        if isinstance(price, (int, float)) and isinstance(prev, (int, float)):
            if price > prev:
                color = "green bold"
            elif price < prev:
                color = "red bold"

        price_str = f"[{color}]$ {price}[/]" if price != "N/A" else "N/A"

        if book_value is None or not isinstance(price, (int, float)):
            gain_str = "[gray35]±0[/]"
        else:
            gain_val = price - book_value
            if gain_val > 0:
                gain_str = f"[bright_green]+{gain_val:.2f}[/]"
            elif gain_val < 0:
                gain_str = f"[bright_red]{gain_val:.2f}[/]"
            else:
                gain_str = "[gray35]±0[/]"

        table.add_row(sym, price_str, f"{volume}", gain_str)
    return table

    
def render_screen():
    
    layout = Layout()
    layout.split(
        Layout(name="table", ratio=3),
        Layout(name="footer", size=1)
    )

    layout["table"].update(render_table())

    now_str = f"🕰️ {datetime.now():%H:%M:%S}   "
    layout["footer"].update(
        Align.right(now_str, vertical="middle")
    )

    return layout


async def main():
    
    preload_prices(list(SYMBOLS.keys()))
    
    async with AsyncWebSocket(verbose=False) as ws:
        await ws.subscribe(list(SYMBOLS.keys()))
        
        listener = asyncio.create_task(ws.listen(message_handler=handle_message))

        with Live(render_screen(), refresh_per_second=2, console=console, transient=False) as live:
            while True:
                live.update(render_screen())
                await asyncio.sleep(0.25)
        await listener

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("Exiting gracefully..")
