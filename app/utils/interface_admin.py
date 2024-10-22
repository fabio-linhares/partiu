# Built-in libraries
import json

# Third-party libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from datetime import date

# Local modules
from api import get_sections_from_api, api_request_cached
from config.variaveis_globais import (
    streamlit_secret, 
    arquivo_de_palavras,

)
from utils.cadastro import render_add_question_form
from utils.database import get_user_data
from utils.frescuras import (
    exibir_grafico_precos,
    exibir_tabela_ofertas,
    gerar_nuvem_palavras
)
from utils.globals import create_global_variables
from utils.loadfile import save_uploaded_file
from utils.scraper import run_scraper




#################################################################################
############################       SECRETS.TOML       ###########################
#################################################################################

config_vars = create_global_variables(streamlit_secret)

#################################################################################
############################         VARIÁVEIS        ###########################
#################################################################################

dev_data = get_user_data(database_name=config_vars['database_user'], 
                         collection_name=config_vars['collections_dev'])

menu_dados = get_sections_from_api(config_vars['database_main'], 
                                   config_vars['collections_menu'])

if dev_data:
    support_mail_ = dev_data.get('email', config_vars['developer_email'])
    support_phone_ = dev_data.get('telefone', config_vars['developer_phone']) 

def interface_admin():

    section = option_menu("Menu", ["Visão Geral", "Análises", "Gerenciamento de Dados", 
                                "Gerenciamento de Usuários", "Operações Avançadas"],
                        icons=['house', 'bar-chart-line', 'database', 'people', 'gear'], 
                        menu_icon="cast", default_index=0, orientation="vertical")

    if section == "Visão Geral":
        render_overview_panel()
    elif section == "Análises":
        render_analysis_panel()
    elif section == "Gerenciamento de Dados":
        render_data_management_panel()
    elif section == "Gerenciamento de Usuários":
        render_user_management_panel()
    elif section == "Operações Avançadas":
        render_advanced_operations_panel()




def render_advanced_operations_panel():
    st.header("Operações Avançadas")
    option = st.radio(
        "Escolha uma opção:",
        ("Adicionar Nova Questão",)
    )

    if option == "Adicionar Nova Questão":
        render_add_question_form()


def render_analysis_panel():
    st.header("Análises")
    pacotes = get_pacotes_data()
    if pacotes:
        exibir_grafico_precos(pacotes)
        exibir_tabela_ofertas(pacotes)

        
        with st.expander("Exibir dados dos pacotes"):
            st.json(pacotes)

        json_string = json.dumps(pacotes)
        st.download_button(
            label="Clique para baixar os dados dos pacotes",
            data=json_string,
            file_name="dados_pacotes.json",
            mime="application/json"
        )
    else:
        st.info("Não há dados de pacotes disponíveis.")

def render_user_management_panel():
    st.header("Gerenciamento de Usuários")

    total_users = get_total_users()
    st.write(f"Total de usuários: {total_users}")
    
    users = get_user_details()
    
    user_data = {
        "Nome de Usuário": [user['username'] for user in users],
        "Email": [user['email'] for user in users],
        "Último Login": [user.get('last_login', 'N/A') for user in users]
    }
    df_users = pd.DataFrame(user_data)
    
    st.table(df_users.style.set_table_styles(
        [{'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('text-align', 'center')]},
         {'selector': 'tbody td', 'props': [('text-align', 'center')]}]
    ))

   
def render_data_management_panel():
    st.header("Gerenciamento de Dados")
    option = st.radio(
        "Escolha uma opção:",
        ("Adicionar Novo Pacote", "Carregar arquivo JSON existente", "Executar novo scraping")
    )

    if option == "Adicionar Novo Pacote":
        st.write("Funcionalidade de adicionar novo pacote ainda não implementada.")

    elif option == "Carregar arquivo JSON existente":
        uploaded_file = st.file_uploader("Escolha um arquivo JSON", type="json")
        if uploaded_file is not None:
            if save_uploaded_file(uploaded_file):
                st.success(f"Arquivo JSON salvo com sucesso em {arquivo_de_palavras}")
            with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                st.session_state.dados = json.load(file)
            st.success("Dados carregados com sucesso!")

    elif option == "Executar novo scraping":
        if st.button("Executar Scraper"):
            with st.spinner("Executando o scraper..."):
                run_scraper()
            st.success("Scraping concluído!")
            with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                st.session_state.dados = json.load(file)

    if 'dados' in st.session_state and st.session_state.dados is not None:
        pacotes = st.session_state.dados
        df_pacotes = pd.DataFrame(pacotes)

        st.subheader("Análise de Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Contagem de Pacotes por Cidade")
            contagem_cidades = df_pacotes['titulo'].value_counts().reset_index()
            contagem_cidades.columns = ['cidade', 'contagem']
            fig = px.bar(contagem_cidades, x='cidade', y='contagem', title="Contagem de Pacotes por Cidade")
            st.plotly_chart(fig)
        
        with col2:
            st.write("Distribuição de Durações")
            fig = px.histogram(df_pacotes, x='duracao', title="Distribuição de Durações")
            st.plotly_chart(fig)

        # Botão para baixar os dados
        json_string = json.dumps(st.session_state.dados)
        st.download_button(
            label="Baixar dados em JSON",
            data=json_string,
            file_name="dados_pacotes.json",
            mime="application/json"
        )

        with st.expander("Exibir dados brutos"):
            st.json(st.session_state.dados)



def get_total_users():
    try:
        result = api_request_cached("GET", "/count_users")
        return result.get('total_users', 0)
    except Exception as e:
        st.error(f"Erro ao obter total de usuários: {str(e)}")
        return 0

def get_total_pacotes():
    try:
        result = api_request_cached("GET", "/count_pacotes")
        return result.get('total_pacotes', 0)
    except Exception as e:
        st.error(f"Erro ao obter total de pacotes: {str(e)}")
        return 0

def get_pacotes_data(limit=100, skip=0):
    try:
        result = api_request_cached("GET", f"/read/{config_vars['collections_pacotes']}?limit={limit}&skip={skip}")
        return result.get('documents', [])
    except Exception as e:
        st.error(f"Erro ao obter dados dos pacotes: {str(e)}")
        return []

def get_user_details(limit=100, skip=0):
    try:
        result = api_request_cached("GET", f"/read/{config_vars['collections_users']}?limit={limit}&skip={skip}")
        return result.get('documents', [])
    except Exception as e:
        st.error(f"Erro ao obter detalhes dos usuários: {str(e)}")
        return []



def get_total_vendas():
    pass



def render_overview_panel():

    # núvem de palavras
    gerar_nuvem_palavras(get_pacotes_data())

    # Dados reais (implementado)
    total_users = get_total_users()
    total_pacotes = get_total_pacotes()
    total_vendas = get_total_vendas()

    # Dados simulados (serão implementados)
    pacotes_mais_vendidos = ["Pacote Europa", "Pacote América do Sul", "Pacote Ásia"]
    receita_total = 1250000  # Receita simulada
    taxa_crescimento_usuarios = "5%"  # Simulada
    taxa_conversao = "2.5%"  # Simulada
    feedback_medio = 4.3  # Simulada
    pacotes_rejeitados = ["Pacote África", "Pacote Caribe"]

    # Criando um DataFrame para exibir como tabela
    overview_data = {
        "Métrica": [
            "Total de Usuários", 
            "Total de Pacotes de Viagem", 
            "Total de Pacotes Vendidos", 
            "Receita Total (Simulada)", 
            "Taxa de Crescimento de Usuários (Simulada)", 
            "Taxa de Conversão (Simulada)", 
            "Feedback Médio dos Clientes (Simulada)"
        ],
        "Valor": [
            total_users, 
            total_pacotes, 
            total_vendas, 
            f"R$ {receita_total:,.2f}", 
            taxa_crescimento_usuarios, 
            taxa_conversao, 
            feedback_medio
        ]
    }
    df_overview = pd.DataFrame(overview_data)
    
    # Exibindo a tabela
    st.table(df_overview.style.set_table_styles(
        [{'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('text-align', 'center')]},
         {'selector': 'tbody td', 'props': [('text-align', 'center')]}]
    ))

    # Detalhes dos pacotes mais vendidos (simulado)
    st.subheader("Pacotes Mais Vendidos (Simulado)")
    st.write(", ".join(pacotes_mais_vendidos))

    # Pacotes com maior rejeição (cancelamentos simulados)
    st.subheader("Pacotes com Maior Rejeição (Simulado)")
    st.write(", ".join(pacotes_rejeitados))

    # Adicionando uma barra horizontal de separação
    st.markdown("---")




















if __name__ == "__main__":
    if 'dados' not in st.session_state:
        st.session_state.dados = None
    interface_admin()