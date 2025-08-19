
import os
import pandas as pd
from typing import Optional
from config import AppConfig
import yfinance as yf


def _cache_path(ticker, cfg: AppConfig) -> str:
    ticker = str(ticker)
    safe = ticker.replace('/', '_').upper()
    return os.path.join(cfg.cache_dir, f"{safe}.csv")


def fetch_prices(ticker: str, start: Optional[str] = None, end: Optional[str] = None,
                 cfg: Optional[AppConfig] = None) -> pd.DataFrame:
    cfg = cfg or AppConfig()
    os.makedirs(cfg.cache_dir, exist_ok=True)
    path = _cache_path(ticker, cfg)

    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=['Date']).set_index('Date')
        return df

    df = yf.download(str(ticker), start=start, end=end, auto_adjust=False, progress=False)

    if df is None or df.empty:
        raise ValueError(f"No data found for {ticker}")

    #Handle MultiIndex vs single-index columns
    def extract_adj_close(frame: pd.DataFrame) -> pd.Series:
        if isinstance(frame.columns, pd.MultiIndex):
            lv10 = frame.columns.get_level_values(0)
            if "Adj Close" in lv10:
                s = frame["Adj Close"]
            elif "Close" in lv10:
                s = frame["Close"]
            else:
                raise KeyError(f"Expected 'Adj Close' or 'Close' column in frame: {list(set(lv10))}")

            #If it's still a DataFrame (multiple tickers), pick the first column
            if isinstance(s, pd.DataFrame):
                s = s.iloc[:, 0]
                return s
            else:
                if "Adj Close" in frame.columns:
                    return frame["Adj Close"]
                if "Close" in frame.columns:
                    return frame["Close"]
                raise KeyError(f"Expected 'Adj Close' or 'Close' column : {frame.columns.tolist()}")
    s = extract_adj_close(df)
    out = s.rename("adj_close").to_frame()
    out.to_csv(path, index=True, index_label="Date")
    return out
