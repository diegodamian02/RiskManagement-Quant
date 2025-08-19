import numpy as np
import pandas as pd
from scipy.stats import norm


def historical_var(returns: pd.Series, alpha: float = 0.99) -> float:
    losses = -returns.dropna()
    return losses.quantile(alpha)


#0.99 of alpha means the 99% of daily losses that means that
#on 99% of days, losses will be smaller than this number. But 1% of days wil be worse

def historical_cvar(returns: pd.Series, alpha: float = 0.99) -> float:
    losses = -returns.dropna()
    var = losses.quantile(alpha)
    tail = losses[losses >= var]
    return tail.mean() if not tail.empty else var


def parametric_var(returns: pd.Series, alpha: float = 0.99) -> float:
    mu = returns.mean()
    sigma = returns.std()
    z = norm.ppf(alpha)
    return z * sigma - mu