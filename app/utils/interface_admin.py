# Built-in libraries
import json

# Third-party libraries
import streamlit as st

# Local modules
from api import get_sections_from_api, api_request_cached
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

def interface_admin():
    st.sidebar.title("Painel Administrativo")
    section = st.sidebar.radio("Escolha uma seção:", ["Visão Geral", "Análises", "Gerenciamento de Dados", "Gerenciamento de Usuários"])
    
    if section == "Visão Geral":
        render_overview_panel()
    elif section == "Análises":
        render_analysis_panel()
    elif section == "Gerenciamento de Dados":
        render_data_management_panel()
    elif section == "Gerenciamento de Usuários":
        render_user_management_panel()

def render_overview_panel():
    st.header("Visão Geral")
    total_users = get_total_users()
    total_pacotes = get_total_pacotes()
    st.metric("Total de Usuários Cadastrados", total_users)
    st.metric("Total de Pacotes de Viagem", total_pacotes)

def render_analysis_panel():
    st.header("Análises")
    pacotes = get_pacotes_data()
    if pacotes:
        exibir_tabela_ofertas(pacotes)
        exibir_grafico_precos(pacotes)
        
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

def render_data_management_panel():
    st.header("Gerenciamento de Dados")
    option = st.radio(
        "Escolha uma opção:",
        ("Visualizar Pacotes", "Adicionar Novo Pacote")
    )

    if option == "Visualizar Pacotes":
        pacotes = get_pacotes_data()
        if pacotes:
            for pacote in pacotes:
                st.subheader(pacote['titulo'])
                st.write(f"Preço: R$ {pacote['preco_atual']}")
                st.write(f"Duração: {pacote['duracao']}")
                st.write(f"Datas: {pacote['datas']}")
        else:
            st.info("Não há pacotes disponíveis.")

    elif option == "Adicionar Novo Pacote":
        st.write("Funcionalidade de adicionar novo pacote ainda não implementada.")

def render_user_management_panel():
    st.header("Gerenciamento de Usuários")
    total_users = get_total_users()
    st.write(f"Total de usuários: {total_users}")
    
    users = get_user_details()
    for user in users:
        st.subheader(user['username'])
        st.write(f"Email: {user['email']}")
        st.write(f"Último Login: {user.get('last_login', 'N/A')}")
        if st.button(f"Redefinir Senha para {user['username']}"):
            st.success(f"Senha redefinida para {user['username']}")

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

if __name__ == "__main__":
    interface_admin()