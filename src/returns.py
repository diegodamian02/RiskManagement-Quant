import numpy as np
import pandas as pd
from config import AppConfig


def log_returns(prices: pd.Series) -> pd.Series:
    return np.log(prices / prices.shift(1)).dropna()


#why log returns? They're time additive and approximate simple returns for small moves

def rolling_vol(returns: pd.Series, window: int = 21) -> pd.Series:
    return returns.rolling(window).std() * np.sqrt(252)


def ewma_vol(returns: pd.Series, cfg: AppConfig = AppConfig()) -> pd.Series:
    lam = cfg.ewma_lambda
    var = []
    prev = returns.var()

    for r in returns:
        prev = lam * prev + (1 - lam) * (r ** 2)
        var.append(prev)
    vol = pd.Series(var, index=returns.index).pow(0.5) * np.sqrt(252)
    return vol


def drawdown_curve(prices: pd.Series) -> pd.Series:
    cum_max = prices.cummax()
    return prices / cum_max - 1.0