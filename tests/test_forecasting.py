import numpy as np
import pandas as pd
from src.forecasting.model import forecast_prices


def test_forecast_returns_requested_horizon():
    close = pd.Series(100 + np.arange(100) * 0.5)
    result, metrics = forecast_prices(close, horizon=4, lookback=10)
    assert len(result) == 4
    assert "mae" in metrics
    assert "r2" in metrics
