# Built-in libraries
import json

# Third-party libraries
import streamlit as st

# Local modules
from api import get_sections_from_api
from config.variaveis_globais import (
    streamlit_secret, 
    arquivo_de_resposta1,
    arquivo_de_resposta2,
    arquivo_de_resposta3,
    arquivo_de_resposta4,
    arquivo_de_palavras,
    template_email,
    OLLAMA_API_URL,
    GOOGLE_API_URL,
    GPT3_API_URL
)
from utils.cadastro import render_add_question_form
from utils.database import get_user_data
from utils.frescuras import (
    exibir_grafico_precos,
    exibir_tabela_ofertas
)
from utils.globals import create_global_variables
from utils.loadfile import save_uploaded_file
from utils.scraper import run_scraper

import streamlit as st
import requests
from PIL import Image
import io
from datetime import datetime
from pymongo import MongoClient
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

use_google_api = True

def interface_admin():
    st.sidebar.title("Painel Administrativo")
    section = st.sidebar.radio("Escolha uma seção:", ["Faculdade", "Aplicativo"])
    
    if section == "Faculdade":
        st.header("Gerenciamento de Questões")
        # Usar expander para organizar as opções
        with st.expander("Opções de Questões"):
            option = st.radio(
                "Escolha uma opção:",
                ("Adicionar Nova Questão",)
            )

            if option == "Adicionar Nova Questão":
                render_add_question_form()

    elif section == "Aplicativo":
        st.header("Dados do Aplicativo")
        
        # Organizar as funcionalidades em abas para um layout mais limpo
        tabs = st.tabs(["Visão Geral", "Análises", "Gerenciamento de Dados"])
        
        with tabs[0]:
            st.subheader("Visão Geral")
            num_users = get_total_users()
            num_pacotes = get_total_pacotes()
            st.metric("Total de Usuários Cadastrados", num_users)
            st.metric("Total de Pacotes Cadastrados", num_pacotes)

        with tabs[1]:
            st.subheader("Análises")
            if st.session_state.dados is not None:
                exibir_tabela_ofertas(st.session_state.dados)
                exibir_grafico_precos(st.session_state.dados)
                
                with st.expander("Exibir dados do arquivo JSON"):
                    st.json(st.session_state.dados)

                json_string = json.dumps(st.session_state.dados)
                st.download_button(
                    label="Clique para baixar o JSON",
                    data=json_string,
                    file_name="dados_scraping.json",
                    mime="application/json"
                )
            else:
                st.info("Carregue um arquivo JSON ou execute o scraper para visualizar os dados.")

        with tabs[2]:
            st.subheader("Gerenciamento de Dados")
            option = st.radio(
                "Escolha uma opção:",
                ("Carregar arquivo JSON existente", "Executar novo scraping")
            )

            if option == "Carregar arquivo JSON existente":
                uploaded_file = st.file_uploader("Escolha um arquivo JSON", type="json")
                if uploaded_file is not None:
                    if save_uploaded_file(uploaded_file):
                        st.success(f"Arquivo JSON salvo com sucesso em {arquivo_de_palavras}")

                    with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                        st.session_state.dados = json.load(file)

            elif option == "Executar novo scraping":
                if st.button("Executar Scraper"):
                    with st.spinner("Executando o scraper..."):
                        run_scraper()
                    st.success("Scraping concluído!")

                    with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                        st.session_state.dados = json.load(file)

def get_total_users():
    # Função hipotética para buscar o número total de usuários do banco de dados
    return 150  # Exemplo de retorno

def get_total_pacotes():
    # Função hipotética para buscar o número total de pacotes do banco de dados
    return 75  # Exemplo de retorno

# # Verifique se o usuário está logado e é administrador
# if st.session_state.get('logged_in', False) and 'roles' in st.session_state.user and 'admin' in st.session_state.user['roles']:
#     interface_admin()
# else:
#     st.warning("Você não tem permissão para acessar esta área")

def render_analysis_panel():
    st.header("Análises")
    if st.session_state.dados is not None:
        exibir_tabela_ofertas(st.session_state.dados)
        exibir_grafico_precos(st.session_state.dados)
        
        with st.expander("Exibir dados do arquivo JSON"):
            st.json(st.session_state.dados)

        json_string = json.dumps(st.session_state.dados)
        st.download_button(
            label="Clique para baixar o JSON",
            data=json_string,
            file_name="dados_scraping.json",
            mime="application/json"
        )
    else:
        st.info("Carregue um arquivo JSON ou execute o scraper para visualizar os dados.")


def render_data_management_panel():
    st.header("Gerenciamento de Dados")
    option = st.radio(
        "Escolha uma opção:",
        ("Carregar arquivo JSON existente", "Executar novo scraping")
    )

    if option == "Carregar arquivo JSON existente":
        uploaded_file = st.file_uploader("Escolha um arquivo JSON", type="json")
        if uploaded_file is not None:
            if save_uploaded_file(uploaded_file):
                st.success(f"Arquivo JSON salvo com sucesso em {arquivo_de_palavras}")

            with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                st.session_state.dados = json.load(file)

    elif option == "Executar novo scraping":
        if st.button("Executar Scraper"):
            with st.spinner("Executando o scraper..."):
                run_scraper()
            st.success("Scraping concluído!")

            with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                st.session_state.dados = json.load(file)


def render_user_management_panel():
    st.header("Gerenciamento de Usuários")
    users = get_all_users()  # Função para buscar todos os usuários
    for user in users:
        st.subheader(user['username'])
        st.write(f"Email: {user['email']}")
        st.write(f"Último Login: {user['last_login']}")
        if st.button(f"Redefinir Senha para {user['username']}"):
            set_user_password(user['username'], "nova_senha")  # Exemplo de redefinição
            st.success(f"Senha redefinida para {user['username']}")


def render_overview_panel():
    st.header("Visão Geral")
    st.metric("Total de Usuários Cadastrados", get_total_users())
    st.metric("Total de Pacotes de Viagem", get_total_pacotes())
    #st.metric("Pacotes Vendidos Este Mês", get_pacotes_vendidos_mes())  # Exemplo de função
    #st.metric("Novos Usuários Este Mês", get_novos_usuarios_mes())  # Exemplo de função


if __name__ == "__main__":
    interface_admin()