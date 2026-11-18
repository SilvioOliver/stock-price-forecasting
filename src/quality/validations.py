import pandas as pd


def validate_market_data(frame: pd.DataFrame) -> None:
    """Falha cedo quando o conjunto não atende aos requisitos mínimos."""
    if frame is None or frame.empty:
        raise ValueError("A consulta não retornou dados.")

    required = {"Open", "High", "Low", "Close", "Volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Colunas ausentes: {sorted(missing)}")

    if frame.index.has_duplicates:
        raise ValueError("Foram encontradas datas duplicadas.")

    if frame["Close"].isna().any():
        raise ValueError("Existem preços de fechamento nulos.")

    if (frame["Close"] <= 0).any():
        raise ValueError("Existem preços de fechamento inválidos (menores ou iguais a zero).")

    if len(frame) < 30:
        raise ValueError("Histórico insuficiente. Selecione um período com pelo menos 30 registros.")
