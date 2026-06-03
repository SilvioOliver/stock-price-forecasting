# 📈 Projeto 8 — Inteligência Financeira
### Prevendo Preços de Ativos em Tempo Real

> **Silvio Oliver**

---

## 📌 Visão Geral

Aplicação interativa construída com **Streamlit** que permite ao usuário:

- Selecionar ações de grandes empresas (Apple, Google, Microsoft, Tesla, Netflix, Meta)
- Definir o período histórico de análise
- Visualizar **indicadores técnicos** em gráficos interativos
- Gerar **previsões de preço** via Regressão Linear com Machine Learning

---

## 🗂️ Estrutura do Projeto

```
Projeto8_InteligenciaFinanceira/
│
├── app.py                          # Aplicação Streamlit (interface web)
├── InteligenciaFinanceira_v2.ipynb # Notebook com análise e desenvolvimento
├── README.md                       # Este arquivo
└── requirements.txt                # Dependências do projeto
```

---

## ⚙️ Instalação e Execução

### 1. Pré-requisitos

- Python 3.8 ou superior
- pip atualizado

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install streamlit yfinance ta scikit-learn pandas matplotlib
```

### 3. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`.

---

## 🔧 Dependências

| Pacote | Versão mínima | Finalidade |
|--------|--------------|------------|
| `streamlit` | 1.28+ | Framework da aplicação web interativa |
| `yfinance` | 0.2+ | Download de dados históricos via Yahoo Finance |
| `ta` | 0.10+ | Cálculo de indicadores técnicos financeiros |
| `scikit-learn` | 1.3+ | Pipeline de Machine Learning |
| `pandas` | 2.0+ | Manipulação e análise de dados |
| `matplotlib` | 3.7+ | Visualizações estáticas |

---

## 📊 Funcionalidades

### 🔍 Visualizar Gráficos — Indicadores Técnicos

| Indicador | Descrição |
|-----------|-----------|
| **Preço de Fechamento** | Histórico do preço de fechamento do ativo |
| **Bandas de Bollinger** | Volatilidade — identifica sobrecompra/sobrevenda |
| **MACD** | Tendência — cruzamento de médias móveis exponenciais |
| **RSI** | Força relativa — zonas de 30 (sobrevenda) e 70 (sobrecompra) |
| **SMA** | Média Móvel Simples de 14 períodos |
| **EMA** | Média Móvel Exponencial — mais reativa a mudanças recentes |

### 📋 Visualizar Tabela de Dados

Exibe os **20 últimos registros** do ativo selecionado com todas as colunas disponíveis.

### 🤖 Fazer Previsões

- Insira o número de dias para a previsão
- O modelo treina uma **Regressão Linear** com padronização (StandardScaler)
- Exibe o **R²** (acurácia) e os preços previstos dia a dia

---

## 🧠 Como o Modelo de Previsão Funciona

```
Dados históricos (Close)
        │
        ▼
Shift temporal → cria variável-alvo (preço N dias à frente)
        │
        ▼
Train/Test Split (80% treino / 20% teste)
        │
        ▼
StandardScaler (fit apenas no treino → evita data leakage)
        │
        ▼
LinearRegression.fit(x_treino, y_treino)
        │
        ▼
Métricas: R² e MAE no conjunto de teste
        │
        ▼
Previsão dos próximos N dias com os últimos dados disponíveis
```

> ⚠️ **Aviso:** Este modelo é para fins educacionais. Regressão Linear não captura
> padrões não-lineares de séries temporais financeiras. Não constitui recomendação
> de investimento.

---

## 📁 Empresas e Tickers Disponíveis

| Empresa | Ticker |
|---------|--------|
| Apple | `AAPL` |
| Google | `GOOG` |
| Microsoft | `MSFT` |
| Tesla | `TSLA` |
| Netflix | `NFLX` |
| Meta | `META` |

Para adicionar novos ativos, edite o bloco de seleção em `app.py` e adicione o ticker
correspondente. Todos os tickers disponíveis podem ser consultados em:
[Yahoo Finance — Most Active](https://finance.yahoo.com/markets/stocks/most-active/)

---

## 🐛 Problemas Conhecidos e Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| `ValueError: No data returned` | Ticker inválido ou mercado fechado | Verifique o ticker no Yahoo Finance |
| Gráfico MACD não renderiza | `matplotlib` não instalado | `pip install matplotlib` |
| `SettingWithCopyWarning` | Modificação de slice sem `.copy()` | Use sempre `df.copy()` |
| Previsão com R² muito baixo | Poucos dados de treino | Aumente o número de registros na sidebar |

---

## 🚀 Evoluções Futuras

- [ ] Substituir Regressão Linear por **LSTM** (Keras/TensorFlow) para melhor captura de dependências temporais
- [ ] Adicionar modelo **Prophet** (Meta) para previsões de séries temporais
- [ ] Incorporar mais features: Volume, indicadores combinados, **sentiment** de notícias
- [ ] Expandir o universo de ativos: BDRs, criptomoedas, índices (IBOVESPA, S&P 500)
- [ ] Criar sistema de **alertas automáticos** quando RSI > 70 ou < 30
- [ ] Adicionar suporte a **múltiplos idiomas** (PT/EN)

---

## 📚 Referências

- [Documentação yfinance](https://ranaroussi.github.io/yfinance/)
- [Documentação ta (Technical Analysis Library)](https://technical-analysis-library-in-python.readthedocs.io/)
- [Documentação Streamlit](https://docs.streamlit.io/)
- [Documentação scikit-learn](https://scikit-learn.org/stable/)
- [Yahoo Finance — Tickers](https://finance.yahoo.com/markets/stocks/most-active/)

---

*Nerd dos Dados — Método TCD | Projeto 8*
