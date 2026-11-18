import pandas as pd
import pytest
from src.quality.validations import validate_market_data


def sample_frame():
    idx = pd.date_range("2024-01-01", periods=35, freq="B")
    return pd.DataFrame({
        "Open": 10.0, "High": 11.0, "Low": 9.0,
        "Close": 10.0, "Volume": 1000,
    }, index=idx)


def test_valid_market_data_passes():
    validate_market_data(sample_frame())


def test_empty_data_fails():
    with pytest.raises(ValueError, match="não retornou"):
        validate_market_data(pd.DataFrame())


def test_null_close_fails():
    frame = sample_frame()
    frame.loc[frame.index[0], "Close"] = None
    with pytest.raises(ValueError, match="nulos"):
        validate_market_data(frame)
