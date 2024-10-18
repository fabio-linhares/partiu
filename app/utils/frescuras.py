import streamlit as st  
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
from datetime import datetime

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

# Uso na interface Streamlit
# exibir_estatisticas(dados)

############################################################################################################    

def exibir_tabela_ofertas(dados):
    df = pd.DataFrame(dados)
    df['preco_atual'] = df['preco_atual'].astype(float)
    df['preco_atual'] = df['preco_atual'].apply(lambda x: f'R$ {x:.2f}')
    st.dataframe(df[['titulo', 'preco_atual', 'duracao', 'datas']])

# Uso na interface Streamlit
# st.header("Ofertas de Pacotes")
# exibir_tabela_ofertas(dados)

############################################################################################################


def exibir_grafico_precos(dados):
    df = pd.DataFrame(dados)
    df['preco_atual'] = df['preco_atual'].astype(float)
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('titulo', sort='-y'),
        y='preco_atual',
        tooltip=['titulo', 'preco_atual', 'duracao', 'datas']
    ).properties(
        width=800,
        height=500,
        title='Preços dos Pacotes de Viagem'
    )
    
    st.altair_chart(chart)

# Uso na interface Streamlit
# exibir_grafico_precos(dados)

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