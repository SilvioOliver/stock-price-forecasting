import pandas as pd
import yfinance as yf


def fetch_history(ticker: str, start_date, end_date) -> pd.DataFrame:
    """Baixa histórico de mercado. A data final do yfinance é exclusiva."""
    try:
        frame = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False,
            threads=False,
        )
    except Exception as exc:
        raise RuntimeError(f"Falha ao consultar Yahoo Finance para {ticker}: {exc}") from exc

    if frame is None or frame.empty:
        raise ValueError(f"Nenhum dado retornado para {ticker}. Verifique o ticker e o período.")

    # Algumas versões do yfinance retornam colunas MultiIndex mesmo para um ticker.
    if isinstance(frame.columns, pd.MultiIndex):
        frame.columns = frame.columns.get_level_values(0)

    required = {"Open", "High", "Low", "Close", "Volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Resposta da fonte sem colunas obrigatórias: {sorted(missing)}")

    return frame.sort_index()
