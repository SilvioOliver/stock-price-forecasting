# Projeto 8 - Inteligência Financeira - Prevendo Preços de Ativos em Tempo Real
# Para executar a plicação digite no terminal: streamlit run app.py

# Importando os pacotes que serão utilizados
import datetime
import pandas as pd
import streamlit as st
import yfinance as yf
from datetime import date
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD, EMAIndicator, SMAIndicator
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# Título principal
st.title('Inteligência Financeira - Prevendo Preços de Ativos em Tempo Real')

# Adicionando o conteúdo da barra lateral
st.sidebar.header("Bem-Vindo(a)")
st.sidebar.info('Método TCD')
st.sidebar.info('Projeto 8')

# Adicionando um espaço em branco para ajustar o tamanho da barra lateral
st.sidebar.markdown("&#8203;" * 100)

# Módulo de seleção de página


def tcd_seleciona_pagina():

    # Cria um menu lateral com opções de seleção
    option = st.sidebar.selectbox('Selecione o Que Deseja Fazer', [
                                  'Visualizar Gráficos', 'Visualizar Tabela de Dados', 'Fazer Previsões'])

    # Verifica se a opção selecionada é 'Visualizar Gráficos' e chama a função correspondente
    if option == 'Visualizar Gráficos':
        tcd_indicadores_tecnicos()

    # Verifica se a opção selecionada é 'Visualizar Tabela de Dados' e chama a função correspondente
    elif option == 'Visualizar Tabela de Dados':
        tcd_imprime_tabela()

    # Se nenhuma das opções acima for selecionada, assume que a opção é 'Fazer Previsões' e chama a função correspondente
    else:
        tcd_previsoes()

# Decorador que permite o cache de recursos no Streamlit para melhorar a performance da aplicação


@st.cache_resource
# Módulo de download de dados de ativos financeiros
def tcd_download_dados(ticker, start_date, end_date):

    ativo = yf.Ticker(ticker)
    df_tcd = ativo.history(start=start_date, end=end_date)

    # Retorna o DataFrame com os dados baixados
    return df_tcd


# Caixa de seleção lateral
option = st.sidebar.selectbox("Selecione a Empresa", [
                              "Apple", "Google", "Microsoft", "Tesla", "Netflix", "Meta"])

# Converte a seleção para maiúsculo
option = option.upper()

# Imprime a opção
print(option)

# Caixa de seleção lateral para o número de pontos de dados (valor padrão de 365, ou seja, 1 ano)
num_pontos_dados = st.sidebar.number_input(
    'Número de Registros Para Treinar o Modelo', value=365)

# Registra a data atual
today = datetime.date.today()

# Obtém a data com a diferença entre a data atual e o número de pontos de dados selecionados
data_padrao = today - datetime.timedelta(days=num_pontos_dados)

# Input para data de início
start_date = st.sidebar.date_input(
    'Selecione Uma Data Inicial', value=data_padrao)

# Input para data de fim
end_date = st.sidebar.date_input('Selecione Uma Data Final', today)


# Bloco condicional para obter o código da empresa selecionada, data de início e data de fim
if option == "APPLE":
    st.sidebar.success('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (
        start_date, end_date))
    stock = "AAPL"
elif option == "GOOGLE":
    st.sidebar.success('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (
        start_date, end_date))
    stock = "GOOG"
elif option == "MICROSOFT":
    st.sidebar.success('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (
        start_date, end_date))
    stock = "MSFT"
elif option == "TESLA":
    st.sidebar.success('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (
        start_date, end_date))
    stock = "TSLA"
elif option == "NETFLIX":
    st.sidebar.success('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (
        start_date, end_date))
    stock = "NFLX"
elif option == "META":
    st.sidebar.success('Data Inicial da Coleta de Dados: `%s`\n\nData Final da Coleta de Dados: `%s`' % (
        start_date, end_date))
    stock = "META"

# Download dos dados
df_tcd_dados = tcd_download_dados(stock, start_date, end_date)


# Define a função para exibir indicadores técnicos no Streamlit
def tcd_indicadores_tecnicos():

    # Cria um cabeçalho na página
    st.header('Indicadores Técnicos')

    # Cria um widget de seleção para escolher um indicador técnico
    option = st.radio('Selecione Um Indicador Técnico Para Visualizar', ['Preço de Fechamento',
                                                                         'Bandas Bollinger',
                                                                         'Moving Average Convergence Divergence',
                                                                         'Relative Strength Indicator',
                                                                         'Simple Moving Average',
                                                                         'Exponential Moving Average'])

    # Calcula as Bandas de Bollinger para o preço de fechamento
    indicador_bb = BollingerBands(df_tcd_dados.Close)

    # Prepara o DataFrame para os dados das Bandas de Bollinger
    df_bb = df_tcd_dados

    # Adiciona a banda superior de Bollinger ao DataFrame
    df_bb['bb_maximo'] = indicador_bb.bollinger_hband()

    # Adiciona a banda inferior de Bollinger ao DataFrame
    df_bb['bb_minimo'] = indicador_bb.bollinger_lband()

    # Seleciona apenas as colunas relevantes para exibição
    df_bb = df_bb[['Close', 'bb_maximo', 'bb_minimo']]

    # Calcula o objeto MACD para o preço de fechamento
    macd_object = MACD(df_tcd_dados['Close'])

    # Calcula o indicador RSI para o preço de fechamento
    rsi = RSIIndicator(df_tcd_dados.Close).rsi()

    # Calcula a Média Móvel Simples (SMA) para o preço de fechamento
    sma = SMAIndicator(df_tcd_dados.Close, window=14).sma_indicator()

    # Calcula a Média Móvel Exponencial (EMA) para o preço de fechamento
    ema = EMAIndicator(df_tcd_dados.Close).ema_indicator()

    # Condicional para verificar qual indicador foi escolhido e exibir os dados correspondentes
    if option == 'Preço de Fechamento':
        st.write('Preço de Fechamento')
        st.line_chart(df_tcd_dados.Close)

    elif option == 'Bandas Bollinger':
        st.write('Bandas Bollinger')
        st.line_chart(df_bb)

    elif option == 'Moving Average Convergence Divergence':
        st.write('Moving Average Convergence Divergence')

        # Se necessário, instale: !pip install PyQt5
        import matplotlib.pyplot as plt

        # Extrai o MACD, o Sinal e a Diferença
        df_tcd_dados['MACD'] = macd_object.macd()
        df_tcd_dados['Signal_Line'] = macd_object.macd_signal()
        df_tcd_dados['MACD_Diff'] = macd_object.macd_diff()

        # Plot
        plt.figure(figsize=(14, 7))

        # Plot do Preço de Fechamento
        plt.subplot(2, 1, 1)
        plt.plot(df_tcd_dados['Close'], label='Preço Fechamento')
        plt.legend()

        # Plot do MACD
        plt.subplot(2, 1, 2)
        plt.plot(df_tcd_dados['MACD'], label='MACD', color='blue')
        plt.plot(df_tcd_dados['Signal_Line'], label='Sinal', color='magenta')
        plt.bar(df_tcd_dados.index,
                df_tcd_dados['MACD_Diff'], label='Histograma', color='black', alpha=0.8)
        plt.legend()
        st.pyplot(plt)

    elif option == 'Relative Strength Indicator':
        st.write('Relative Strength Indicator')
        st.line_chart(rsi)

    elif option == 'Simple Moving Average':
        st.write('Simple Moving Average')
        st.line_chart(sma)

    else:
        st.write('Exponential Moving Average')
        st.line_chart(ema)

# Função para mostrar os 20 últimos registros da tabela de dados


def tcd_imprime_tabela():
    st.header('Tabela de Dados')
    st.dataframe(df_tcd_dados.tail(20))

# Função para previsão


def tcd_previsoes():

    # Recebe o número de dias para a previsão
    num = st.number_input(
        'Fazer a Previsão de Quantos Dias?', value=1, min_value=1)
    num = int(num)

    # Verifica se o botão 'Previsão' foi pressionado e se num é maior que 0
    if st.button('Previsão') and num > 0:
        tcd_gerando_previsoes(num)
    elif num <= 0:
        st.error('Por favor, insira um número de dias maior que 0 para a previsão.')

# Módulo para fazer previsões a partir dos dados


def tcd_gerando_previsoes(num):

    # Extrai o preço de fechamento
    df = df_tcd_dados[['Close']].copy()

    # A nova coluna 'target' conterá os valores da coluna 'Close' deslocados (shift) para cima por num posições.
    df['target'] = df.Close.shift(-num)

    # Separa as variáveis de entrada e saída (variaveis preditoras e variavel alvo)
    x = df.drop(['target'], axis=1).values
    y = df.target.values[:-num]

    # Divide os dados em treino e teste antes da padronização
    x_treino, x_teste, y_treino, y_teste = train_test_split(
        x[:-num], y, test_size=.2, random_state=42)

    # Inicializa e ajusta o StandardScaler com os dados de treino
    padronizador = StandardScaler()
    x_treino_padronizado = padronizador.fit_transform(x_treino)

    # Aplica a transformação aos dados de teste
    x_teste_padronizado = padronizador.transform(x_teste)

    # Treina o modelo com os dados de treino padronizados
    modelo_tcd = LinearRegression().fit(x_treino_padronizado, y_treino)

    # Faz previsões com os dados de teste padronizados
    previsoes = modelo_tcd.predict(x_teste_padronizado)

    # Avalia a acurácia do modelo
    st.text(f'Previsão com Acurácia de: {r2_score(y_teste, previsoes)}')

    # Prepara e faz previsões para os próximos 'num' dias
    # Obs: A padronização de 'x_forecast' deve ser feita com o mesmo padronizador
    x_forecast = df.drop(['target'], axis=1).values[-num:]
    x_forecast_padronizado = padronizador.transform(x_forecast)
    forecast_previsto = modelo_tcd.predict(x_forecast_padronizado)

    # Exibe as previsões para os próximos 'num' dias
    day = 1
    for i in forecast_previsto:
        st.text(f'Previsão do Preço de Fechamento no Dia {day} é: {i}')
        day += 1


# Adiciona um rodapé simples ao final do aplicativo
st.caption('Silvio Oliver - Método')

# Bloco principal do programa Python
if __name__ == '__main__':
    tcd_seleciona_pagina()
