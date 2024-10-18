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
# OS Name        : Arch Linux
# OS Type        : GNU/Linux
# OS Version     : 6.11.3-zen1-1-zen
###############################################################################

# Built-in libraries
import threading

# Third-party libraries
import streamlit as st

# Local modules
from api import get_sections_from_api
from config.variaveis_globais import (
    streamlit_secret,  
    infnet_image, 
    mec_image
)

from utils.cadastro import render_cadastro_form
from utils.database import get_user_data
from utils.globals import create_global_variables
from utils.mongo2 import load_database_config
from utils.scrapy import get_pacotes_viagem, atualizar_pacotes
from utils.security import login_user

from utils.title import get_random_title

# Inicialização de variáveis globais e configuração do Streamlit
config_vars = create_global_variables(streamlit_secret)

st.set_page_config(
    page_title=config_vars['app_title'], 
    page_icon=config_vars['app_icon'], 
    layout=config_vars['app_layout']
)

from utils.render import render_main_image, render_tabs

#################################################################################
############################       SECRETS.TOML       ###########################
#################################################################################

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



#################################################################################
############################           TÍTULO         ###########################
#################################################################################

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user' not in st.session_state:
    st.session_state.user = None

if 'used_titles' not in st.session_state:
    st.session_state.used_titles = []

try:
    random_title = get_random_title(config_vars['database_main'], config_vars['collections_title'])
    st.title(random_title)
except Exception as e:
    st.error(f"Erro ao buscar título aleatório: {str(e)}")
    st.title("Bem-vindo ao aplicativo")  



#################################################################################
############################          PACOTES         ###########################
#################################################################################

if 'pacotes' not in st.session_state:
    st.session_state.pacotes = get_pacotes_viagem()

if 'thread_atualizar_pacotes' not in st.session_state:
    st.session_state.thread_atualizar_pacotes = threading.Thread(target=atualizar_pacotes, daemon=True)
    st.session_state.thread_atualizar_pacotes.start()


#################################################################################
############################           MENUS          ###########################
#################################################################################

st.sidebar.image(infnet_image, use_column_width=True)
st.sidebar.header(config_vars['sections_sidemenu'])

if 'selected_section' not in st.session_state:
    st.session_state.selected_section = None

if menu_dados:
    sections = [item['section'] for item in menu_dados]
    selected_section = st.sidebar.selectbox(config_vars['sections_sidemenumsg'], 
                                            sections,    
                                            key='selected_section')
else:
    st.sidebar.warning("Nenhuma seção encontrada ou erro ao carregar dados.")
    selected_section = None

st.sidebar.image(mec_image, use_column_width=True)

st.sidebar.markdown(
    """
    <div style="text-align: justify;">
        <strong>{}</strong>: <p>{}</p>
    </div>
    """.format(config_vars['sections_sidemenuchamada'], config_vars['sections_sidemenuinstrucao']),
    unsafe_allow_html=True
)

#################################################################################
############################      LOGIN SIDEBAR       ###########################
#################################################################################

if 'show_cadastro' not in st.session_state:
    st.session_state.show_cadastro = False

st.sidebar.markdown("---")

if not st.session_state.get('logged_in', False):
    with st.sidebar.expander("Login / Cadastro"):
        username = st.text_input("Usuário", key="username_sidebar")
        password = st.text_input("Senha", type="password", key="password_sidebar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Login", key="login_button_sidebar", use_container_width=True):
                result = login_user(username, password)
                if result.get('status') == 'success':
                    st.session_state.logged_in = True
                    st.session_state.user = result.get('user', {})
                    st.session_state.user_email = result.get('user', {}).get('email', '') 
                    st.rerun()
                else:
                    st.error(f"Erro de login: {result.get('detail', 'Usuário ou senha incorretos')}")

        with col2:
            if st.button("Cadastro", key="register_button_sidebar", use_container_width=True):
                st.session_state.show_cadastro = True
                st.rerun()

else:
    st.sidebar.write(f"Bem-vindo, {st.session_state.user['profile']['first_name']}!")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.user_email = None
        st.rerun()
#################################################################################
############################     CONTEÚDO PRINCIPAL     #########################
#################################################################################

if st.session_state.show_cadastro:
    render_cadastro_form()
    pass
else:
    pass
    render_main_image()
    tabs_content = render_tabs(selected_section, menu_dados)
    tabs_content()
#################################################################################
############################           RODAPÉ         ###########################
#################################################################################

if dev_data:
    user_name = dev_data.get('nome', 'zerocopia')
    user_email = dev_data.get('email_aluno', 'zerodevsystem@gmail.com')

    st.markdown(
                """
                <div style="text-align: center;">
                    <p style="font-size: 12px;">Desenvolvido por {} | Contato: {}.</p>
                </div>
                """.format(user_name, user_email),
                unsafe_allow_html=True
)


else:
    st.error("Não foi possível recuperar os dados do usuário.")
