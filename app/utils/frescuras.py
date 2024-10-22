import streamlit as st  
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import altair as alt
from datetime import datetime
import locale

def convert_price_to_float(price_str):
    # Remove caracteres indesejados e converte para float
    try:
        return float(price_str.replace('R$', '').replace('.', '').replace(',', '.').strip())
    except ValueError:
        return None

def gerar_nuvem_palavras(viagens):

    texto = ' '.join([viagem['titulo'] + ' ' + (viagem.get('descricao') or '') for viagem in viagens])
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(texto)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    st.pyplot(plt)


def exibir_estatisticas(dados):
    df = pd.DataFrame(dados)
    
    # Convertendo preço_atual para float
    df['preco_atual'] = df['preco_atual'].astype(float)
    
    st.subheader("Estatísticas de Preços")
    st.write(df['preco_atual'].describe())
    
    st.subheader("Top 5 Destinos Mais Frequentes")
    st.write(df['titulo'].value_counts().head())
    
    st.subheader("Duração Média das Viagens")
    df['duracao_dias'] = df['duracao'].str.extract('(\d+)').astype(int)
    st.write(f"Média de dias: {df['duracao_dias'].mean():.2f}")
    
    st.subheader("Distribuição de Meses de Viagem")
    def extrair_mes(data_str):
        meses = {
            'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
            'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
        }
        for mes, num in meses.items():
            if mes in data_str.lower():
                return datetime(2024, num, 1).strftime('%B')
        return None

    df['mes_viagem'] = df['datas'].apply(extrair_mes)
    mes_counts = df['mes_viagem'].value_counts()
    st.write(mes_counts)

############################################################################################################    

def formatar_preco(preco):
    if isinstance(preco, str):
        preco = preco.replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        valor = float(preco)
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except ValueError:
        return preco


def exibir_tabela_ofertas(dados):
    # Definindo o locale para o formato brasileiro
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    df = pd.DataFrame(dados)

    # Função para formatar o preço corretamente
    def formatar_preco(preco):
        if isinstance(preco, str):
            # Remove o 'R$' se presente e substitui '.' por ''
            preco = preco.replace('R$', '').replace('.', '').strip()
            # Substitui ',' por '.' para converter para float
            preco = preco.replace(',', '.')
        try:
            valor = float(preco)
            return locale.currency(valor, grouping=True, symbol='R$')
        except ValueError:
            return preco  # Retorna o valor original se não puder ser convertido

    # Aplicando a formatação
    df['preco_atual'] = df['preco_atual'].apply(formatar_preco)

    # Exibindo a tabela
    st.dataframe(df[['titulo', 'preco_atual', 'duracao', 'datas']])




############################################################################################################

def exibir_grafico_precos(dados):
    df = pd.DataFrame(dados)
    
    # Função para limpar e converter o preço
    def limpar_preco(preco):
        if isinstance(preco, str):
            # Remove 'R$', pontos de milhar e substitui vírgula por ponto
            preco = preco.replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            return float(preco)
        except ValueError:
            return None  # Retorna None se não puder converter

    # Aplicar a limpeza e conversão
    df['preco_atual'] = df['preco_atual'].apply(limpar_preco)
    
    # Remover linhas com preços nulos ou zero
    df = df[df['preco_atual'].notna() & (df['preco_atual'] > 0)]
    
    # Agrupar por título e pegar o maior preço
    df_max_preco = df.loc[df.groupby('titulo')['preco_atual'].idxmax()]

    # Verificar se há dados para plotar
    if df_max_preco.empty:
        st.error("Não há dados válidos para exibir o gráfico.")
        return
    
    # Criar o gráfico com Plotly
    fig = px.bar(df_max_preco, x='titulo', y='preco_atual', 
                 title='Preços dos Pacotes de Viagem',
                 labels={'titulo': 'Destino', 'preco_atual': 'Preço (R$)'},
                 hover_data=['duracao', 'datas'])
    
    fig.update_layout(xaxis_title='Destino',
                      yaxis_title='Preço (R$)',
                      xaxis_tickangle=-45)
    
    # Exibir o gráfico
    st.plotly_chart(fig)

    
############################################################################################################


def get_tab_names(config_vars, prefix):
    tab_names = []
    i = 1
    while True:
        key = f'{prefix}_{i}'
        if key in config_vars:
            tab_names.append(config_vars[key])
            i += 1
        else:
            break
    return tab_names


def contar_itens_config(config_vars, radical):
    count = 0
    i = 1
    
    while True:
        key = f'{radical}_{i}'
        if key in config_vars:
            count += 1
            i += 1
        else:
            break  
    
    return count