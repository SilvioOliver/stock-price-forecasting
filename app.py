import streamlit as st
from datetime import date, timedelta

from src.ingestion.yahoo_finance import fetch_history
from src.transformation.indicators import add_indicators
from src.quality.validations import validate_market_data
from src.forecasting.model import forecast_prices

TICKERS = {
    "Apple": "AAPL",
    "Google": "GOOG",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Netflix": "NFLX",
    "Meta": "META",
}

st.set_page_config(page_title="Inteligência Financeira", layout="wide")
st.title("Inteligência Financeira | Análise de ativos")

with st.sidebar:
    st.header("Parâmetros")
    company = st.selectbox("Empresa", list(TICKERS))
    end_date = st.date_input("Data final", date.today())
    start_date = st.date_input("Data inicial", end_date - timedelta(days=365))
    page = st.radio("Visualização", ["Indicadores", "Tabela de dados", "Previsão"])

if start_date >= end_date:
    st.error("A data inicial precisa ser anterior à data final.")
    st.stop()

ticker = TICKERS[company]

@st.cache_data(ttl=900, show_spinner="Coletando dados...")
def load_data(symbol, start, end):
    return fetch_history(symbol, start, end)

try:
    raw = load_data(ticker, start_date, end_date)
    validate_market_data(raw)
    data = add_indicators(raw)
except (ValueError, RuntimeError) as exc:
    st.error(str(exc))
    st.stop()

st.caption(f"Ativo: {ticker} | Registros: {len(data)} | Fonte: Yahoo Finance")

if page == "Indicadores":
    choice = st.selectbox(
        "Indicador",
        ["Preço de fechamento", "Bandas de Bollinger", "MACD", "RSI", "SMA 14", "EMA 14"],
    )
    if choice == "Preço de fechamento":
        st.line_chart(data["Close"])
    elif choice == "Bandas de Bollinger":
        st.line_chart(data[["Close", "bb_upper", "bb_lower"]])
    elif choice == "MACD":
        st.line_chart(data[["MACD", "MACD_signal"]])
    elif choice == "RSI":
        st.line_chart(data["RSI"])
    elif choice == "SMA 14":
        st.line_chart(data[["Close", "SMA_14"]])
    else:
        st.line_chart(data[["Close", "EMA_14"]])

elif page == "Tabela de dados":
    st.dataframe(data.tail(50), use_container_width=True)

else:
    horizon = st.number_input("Dias úteis a prever", min_value=1, max_value=10, value=3)
    lookback = st.slider("Janela histórica (dias úteis)", min_value=5, max_value=60, value=20)
    if st.button("Gerar previsão", type="primary"):
        try:
            predictions, metrics = forecast_prices(data["Close"], horizon=int(horizon), lookback=lookback)
            col1, col2 = st.columns(2)
            col1.metric("MAE no teste", f"{metrics['mae']:.3f}")
            col2.metric("R² no teste", f"{metrics['r2']:.3f}")
            st.subheader("Preços previstos (estimativa educacional)")
            st.dataframe(predictions, use_container_width=True)
            st.line_chart(predictions.set_index("Dia")["Preço previsto"])
        except ValueError as exc:
            st.error(str(exc))

st.caption("Projeto educacional. Não constitui recomendação de investimento.")
