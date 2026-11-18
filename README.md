# Stock Price Forecasting | Inteligência Financeira

Aplicação educacional para consultar histórico de ativos, calcular indicadores técnicos e gerar projeções demonstrativas de preço usando Python, Pandas, Streamlit e Scikit-learn.

## Funcionalidades

- Coleta de histórico via Yahoo Finance (`yfinance`).
- Indicadores RSI, MACD, Bandas de Bollinger, SMA e EMA.
- Validação básica de qualidade: colunas obrigatórias, datas duplicadas, preços nulos ou inválidos e volume mínimo de histórico.
- Projeção recursiva de curto prazo com regressão linear.
- Avaliação em conjunto temporal separado, com MAE e R².
- Testes automatizados e workflow de CI no GitHub Actions.

## Arquitetura

```text
app.py
src/
  ingestion/       # Extração dos dados de mercado
  transformation/  # Cálculo dos indicadores
  quality/         # Regras de validação
  forecasting/    # Treino, avaliação e projeção
tests/              # Testes automatizados
.github/workflows/  # Integração contínua
```

## Executar localmente

Requisitos: Python 3.10 ou superior.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Executar testes

```bash
pytest -q
```

## Fluxo de dados

1. O usuário seleciona o ativo e o intervalo.
2. O módulo de ingestão consulta o Yahoo Finance.
3. As validações verificam estrutura e consistência mínima.
4. O módulo de transformação calcula indicadores técnicos.
5. A interface exibe os dados ou chama o módulo de previsão.

## Limitações

- O Yahoo Finance é uma fonte externa e pode limitar, atrasar ou alterar respostas.
- A regressão linear é um exemplo didático, não um modelo robusto de investimento.
- O conjunto de teste respeita a ordem temporal; ainda assim, resultados históricos não garantem desempenho futuro.
- A previsão recursiva acumula erro a cada passo.
- Não há, nesta versão, persistência em S3, orquestração AWS ou consultas Athena. Esses componentes podem ser adicionados em uma evolução posterior, se implementados e testados.

## Aviso

Este projeto tem finalidade educacional e não constitui recomendação de investimento.
