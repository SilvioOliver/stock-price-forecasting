import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD, EMAIndicator, SMAIndicator


def add_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    """Retorna uma cópia enriquecida com indicadores técnicos."""
    if "Close" not in frame:
        raise ValueError("A coluna Close é obrigatória.")

    result = frame.copy()
    close = result["Close"].astype(float)

    bands = BollingerBands(close)
    macd = MACD(close)

    result["bb_upper"] = bands.bollinger_hband()
    result["bb_lower"] = bands.bollinger_lband()
    result["MACD"] = macd.macd()
    result["MACD_signal"] = macd.macd_signal()
    result["RSI"] = RSIIndicator(close).rsi()
    result["SMA_14"] = SMAIndicator(close, window=14).sma_indicator()
    result["EMA_14"] = EMAIndicator(close, window=14).ema_indicator()
    return result
