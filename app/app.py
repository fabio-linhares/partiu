###############################################################################
# Script Name    : app/app.py
# Description    :
# Args           :
# Author         : Fábio Linhares (zerocopia)
# Email          : zerodevsystem@gmail.com
# GitHub         : https://github.com/zerodevsystem
# LinkedIn       : https://www.linkedin.com/in/fabio-linhares/
# Created        : 2024-10-11
# Last Modified  :
# Shell Version  : 5.2.37(1)-release
# OS Name        : Garuda Linux
# OS Type        : GNU/Linux
# OS Version     : 6.11.3-zen1-1-zen
###############################################################################

# Built-in libraries
import json

# Third-party libraries
import matplotlib.pyplot as plt
import streamlit as st

# Local modules
from utils.background import get_random_image
from utils.globals import create_global_variables
from utils.mongo2 import load_database_config
from api import api_request
from config.variaveis_globais import (
    streamlit_secret, 
    image_directory, 
    infnet_image, 
    mec_image, 
    arquivo_de_apresentacao, 
    arquivo_de_teste, 
    arquivo_de_rubrica
)

#################################################################################
############################            API           ###########################
#################################################################################


#################################################################################
############################         VARIÁVEIS        ###########################
#################################################################################

menu_dados = []


#################################################################################
############################       SECRETS.TOML       ###########################
#################################################################################

config_vars = create_global_variables(streamlit_secret)

if config_vars.get('environment_env') == 'dev':
    print("Variáveis carregadas do arquivo TOML:")
    for var_name, value in config_vars.items():
        if var_name != 'environment_env':
            print(f"{var_name} = {value}")

    uri = load_database_config(streamlit_secret)
    print("URI do banco de dados:", uri)



#################################################################################
############################         DATABASE         ###########################
#################################################################################




#################################################################################
############################           MENUS          ###########################
#################################################################################

st.sidebar.image(infnet_image, use_column_width=True)
st.sidebar.header("Seções do Menu")
st.sidebar.image(mec_image, use_column_width=True)

st.sidebar.markdown(
    """
    <div style="text-align: justify;">
        <strong>Instruções</strong>: <p>Após escolher uma das opções no menu acima, os dados correspondentes são exibidos na aba principal da página.</p>
    </div>
    """,
    unsafe_allow_html=True
)

#################################################################################
############################           TÍTULO         ###########################
#################################################################################


#################################################################################
############################          IMAGENS         ###########################
#################################################################################

random_image_path = get_random_image(image_directory)
capa_site = random_image_path
st.image(capa_site, use_column_width=True)

#################################################################################
############################           ABAS           ###########################
#################################################################################

# abas principais
main_tab1, main_tab2, main_tab3 = st.tabs(["O Projeto", "O Teste", "O App"])

with main_tab1:

    with open(arquivo_de_apresentacao, 'r', encoding='utf-8') as file:
        texto_em_markdown = file.read()
        st.markdown(texto_em_markdown)
             
with main_tab2:

    # abas secundárias
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Atividades", "Competências", "Respostas"])

    with sub_tab1:
        with open(arquivo_de_teste, 'r', encoding='utf-8') as file:
            texto_em_markdown = file.read()
            st.markdown(texto_em_markdown)

    with sub_tab2:
        with open(arquivo_de_rubrica, 'r', encoding='utf-8') as file:
            texto_em_markdown = file.read()
            st.markdown(texto_em_markdown)

#################################################################################
############################        RESPOSTAS         ###########################
#################################################################################

    with sub_tab3:
        pass
        

#################################################################################
############################           APP            ###########################
#################################################################################
with main_tab3:
    # Seleção de operação
    operation = st.selectbox("Select operation", ["Create", "Read", "Update", "Delete", "Get Main Collection"])

    if operation == "Create":
        collection = st.text_input("Collection name")
        data = st.text_area("Document data (JSON format)")
        if st.button("Create Document"):
            try:
                json_data = json.loads(data)
                result = api_request("POST", f"/create/{collection}", {"data": json_data})
                if result:
                    st.success(f"Document created with ID: {result['id']}")
            except json.JSONDecodeError:
                st.error("Invalid JSON format")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif operation == "Read":
        collection = st.text_input("Collection name")
        limit = st.number_input("Limit", min_value=1, value=10)
        if st.button("Read Documents"):
            try:
                result = api_request("GET", f"/read/{collection}?limit={limit}")
                if result:
                    st.json(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif operation == "Update":
        collection = st.text_input("Collection name")
        doc_id = st.text_input("Document ID")
        data = st.text_area("Updated data (JSON format)")
        if st.button("Update Document"):
            try:
                json_data = json.loads(data)
                result = api_request("PUT", f"/update/{collection}/{doc_id}", {"data": json_data})
                if result:
                    st.success("Document updated successfully")
            except json.JSONDecodeError:
                st.error("Invalid JSON format")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif operation == "Delete":
        collection = st.text_input("Collection name")
        doc_id = st.text_input("Document ID")
        if st.button("Delete Document"):
            try:
                result = api_request("DELETE", f"/delete/{collection}/{doc_id}")
                if result:
                    st.success("Document deleted successfully")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif operation == "Get Main Collection":
        if st.button("Get Main Collection"):
            try:
                result = api_request("GET", "/main_collection")
                if result:
                    st.json(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            
        
#################################################################################
############################           RODAPÉ         ###########################
#################################################################################

# st.markdown(
#     """
#     <div style="text-align: center;">
#         <p style="font-size: 12px;">Desenvolvido por {} | Contato: {}.</p>
#     </div>
#     """.format(dev_author, dev_mail),
#     unsafe_allow_html=True
# )
