import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def _make_supervised(values: np.ndarray, lookback: int):
    x, y = [], []
    for idx in range(lookback, len(values)):
        x.append(values[idx - lookback:idx])
        y.append(values[idx])
    return np.asarray(x), np.asarray(y)


def forecast_prices(close: pd.Series, horizon: int = 3, lookback: int = 20):
    """Treina com divisão cronológica e prevê recursivamente os próximos dias."""
    values = pd.to_numeric(close, errors="coerce").dropna().to_numpy(dtype=float)
    if horizon < 1:
        raise ValueError("O horizonte precisa ser maior que zero.")
    if lookback < 2 or len(values) <= lookback + 10:
        raise ValueError("Histórico insuficiente para a janela escolhida.")

    x, y = _make_supervised(values, lookback)
    split = int(len(x) * 0.8)
    if split < 5 or len(x) - split < 2:
        raise ValueError("Não há amostras suficientes para treino e teste.")

    model = make_pipeline(StandardScaler(), LinearRegression())
    model.fit(x[:split], y[:split])
    test_predictions = model.predict(x[split:])
    mae = mean_absolute_error(y[split:], test_predictions)
    r2 = r2_score(y[split:], test_predictions) if len(y[split:]) > 1 else float("nan")

    history = list(values[-lookback:])
    future = []
    for step in range(horizon):
        next_value = float(model.predict(np.asarray(history[-lookback:]).reshape(1, -1))[0])
        future.append(next_value)
        history.append(next_value)

    result = pd.DataFrame({
        "Dia": [f"D+{i}" for i in range(1, horizon + 1)],
        "Preço previsto": future,
    })
    return result, {"mae": float(mae), "r2": float(r2)}
