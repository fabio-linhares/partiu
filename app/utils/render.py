# Built-in libraries
import json
import threading
import time
from datetime import datetime, timedelta

# Third-party libraries
import matplotlib.pyplot as plt
import streamlit as st

import requests
from PIL import Image
import io

# Local modules
from api import api_request, get_sections_from_api, api_request_cached
from config.variaveis_globais import (
    streamlit_secret, 
    image_directory, 
    infnet_image, 
    mec_image, 
    arquivo_de_apresentacao, 
    arquivo_de_teste, 
    arquivo_de_rubrica,
    arquivo_de_resposta1,
    arquivo_de_resposta2,
    arquivo_de_resposta3,
    arquivo_de_resposta4,
    arquivo_de_palavras
)



from utils.abas import (criar_abas_principais, 
                        criar_abas_secundarias, 
                        adicionar_conteudo,
                        criar_exibidor_respostas,
                        exibir_respostas,
                        exibir_pacotes_viagem,
                        exibir_area_restrita,
                        exibir_api_teste,)

from utils.markdown import read_markdown_file
from utils.background import get_random_image, get_cached_random_image
from utils.cadastro import render_cadastro_form
from utils.globals import create_global_variables

from utils.database import get_user_data
from utils.loadfile import load_json_data, save_uploaded_file
from utils.mail import enviar_email
from utils.markdown import read_markdown_file
from utils.mongo2 import load_database_config
from utils.scrapy  import get_pacotes_viagem, atualizar_pacotes
from utils.scraper import run_scraper
from utils.security import login_user
from utils.title import get_random_title
from utils.frescuras import (gerar_nuvem_palavras,
                             contar_itens_config,
                             get_tab_names,
                             exibir_grafico_precos,
                             exibir_tabela_ofertas)



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
############################         VARIÁVEIS        ###########################
#################################################################################

dev_data = get_user_data(database_name=config_vars['database_user'], 
                                     collection_name=config_vars['collections_dev'])

menu_dados = get_sections_from_api(config_vars['database_main'], 
                                   config_vars['collections_menu'])

num_main_tabs = contar_itens_config(config_vars, 'main_tab')
num_sub_tabs = contar_itens_config(config_vars, 'sub_tab')
num_sub_tabs_test = contar_itens_config(config_vars, 'sub_tab_test')













def render_main_image():
    random_image_path = get_cached_random_image(image_directory)
    capa_site = random_image_path
    st.image(capa_site, use_column_width=True)

def render_tabs(selected_section, menu_dados):
    num_main_tabs = contar_itens_config(config_vars, 'main_tab') + 1
    num_sub_tabs = contar_itens_config(config_vars, 'sub_tab') + 1
    num_sub_tabs_test = contar_itens_config(config_vars, 'sub_tab_test') + 1

    # Criar abas principais
    main_tab_names = [config_vars[f'main_tab_{i}'] for i in range(1, num_main_tabs)] 

    def tab_contents():

        main_tabs = st.tabs(main_tab_names)

        for i, tab in enumerate(main_tabs):
            with tab:
                if main_tab_names[i] == config_vars['main_tab_2']:  # "O Projeto"
                    adicionar_conteudo(lambda: read_markdown_file(arquivo_de_apresentacao))
                
                elif main_tab_names[i] == config_vars['main_tab_3']:  # "O Teste"
                    sub_tab_names = [config_vars[f'sub_tab_test_{j}'] for j in range(1, num_sub_tabs_test)]
                    sub_tabs = st.tabs(sub_tab_names)
                    
                    for j, sub_tab in enumerate(sub_tabs):
                        with sub_tab:
                            if j == 0:
                                adicionar_conteudo(lambda: read_markdown_file(arquivo_de_teste))
                            elif j == 1:
                                adicionar_conteudo(lambda: read_markdown_file(arquivo_de_rubrica))
                            elif j == 2:
                                adicionar_conteudo(lambda: exibir_respostas(selected_section, menu_dados))
                
                elif main_tab_names[i] == config_vars['main_tab_1']:  # "O App"
                    sub_tab_names = [config_vars[f'sub_tab_{j}'] for j in range(1, num_sub_tabs)]
                    sub_tabs = st.tabs(sub_tab_names)
                    
                    for j, sub_tab in enumerate(sub_tabs):
                        with sub_tab:
                            if j == 0:
                                adicionar_conteudo(exibir_pacotes_viagem)
                            elif j == 1:
                                adicionar_conteudo(exibir_area_restrita)
                            elif j == 2:
                                adicionar_conteudo(exibir_api_teste)
    return tab_contents