# Built-in libraries
from datetime import datetime

# Third-party libraries
import streamlit as st

# Local modules
from api import get_sections_from_api
from config.variaveis_globais import streamlit_secret
from utils.database import get_user_data
from utils.globals import create_global_variables


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

#################################################################################
############################            ABAS          ###########################
#################################################################################

def criar_abas_principais(config_vars):
    main_tab_names = [config_vars[f'main_tab_{i}'] for i in range(1, len(config_vars) + 1) if f'main_tab_{i}' in config_vars]
    main_tabs = st.tabs(main_tab_names)
    return main_tabs, main_tab_names

def criar_abas_secundarias(config_vars, aba_principal):
    sub_tab_names = [config_vars[f'sub_tab_{i}'] for i in range(1, len(config_vars) + 1) if f'sub_tab_{i}' in config_vars]
    with aba_principal:
        sub_tabs = st.tabs(sub_tab_names)
    return sub_tabs, sub_tab_names

def adicionar_conteudo(conteudo, *args, **kwargs):
    try:
        if isinstance(conteudo, str):
            st.markdown(conteudo)
        elif callable(conteudo):
            result = conteudo(*args, **kwargs)
            if result is not None:
                st.write(result)
        else:
            st.write(conteudo)
    except Exception as e:
        st.error(f"Erro ao adicionar conteúdo: {str(e)}")
        print(f"Erro ao adicionar conteúdo: {str(e)}")  