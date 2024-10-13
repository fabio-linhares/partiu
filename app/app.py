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
from utils.background import get_random_image, get_cached_random_image
from utils.globals import create_global_variables
from utils.database import get_user_data
from utils.loadfile import load_json_data, save_uploaded_file
from utils.markdown import read_markdown_file
from utils.mongo2 import load_database_config
from utils.scrapy  import get_pacotes_viagem
from utils.scraper import run_scraper
from utils.security import login_user
from utils.title import get_random_title
from utils.frescuras import (gerar_nuvem_palavras,
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

#config_vars['collections_dev']

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

st.set_page_config(page_title=config_vars['app_title'], page_icon=config_vars['app_icon'], layout=config_vars['app_layout'])

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

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()  

#################################################################################
############################          IMAGENS         ###########################
#################################################################################

random_image_path = get_cached_random_image(image_directory)
capa_site = random_image_path
st.image(capa_site, use_column_width=True)
#################################################################################
############################           ABAS           ###########################
#################################################################################

# abas principais
main_tab1, main_tab2, main_tab3 = st.tabs(["O Projeto", "O Teste", "O App"])

with main_tab1:
    texto_em_markdown = read_markdown_file(arquivo_de_apresentacao)
    st.markdown(texto_em_markdown)
            
with main_tab2:

    # abas secundárias
    sub_tab_a1, sub_tab_a2, sub_tab_a3 = st.tabs(["Atividades", "Competências", "Respostas"])

    with sub_tab_a1:

        texto_em_markdown = read_markdown_file(arquivo_de_teste)
        st.markdown(texto_em_markdown)

    with sub_tab_a2:

        texto_em_markdown = read_markdown_file(arquivo_de_rubrica)
        st.markdown(texto_em_markdown)

#################################################################################
############################        RESPOSTAS         ###########################
#################################################################################

    with sub_tab_a3:
        if selected_section:
            selected_questions = next((item['questions'] for item in menu_dados if item['section'] == selected_section), [])
            st.write(f"## {selected_section}")
            for question in selected_questions:
                st.write(question)

            if selected_section == "Configuração do Ambiente de Desenvolvimento":

                texto_em_markdown = read_markdown_file(arquivo_de_resposta1)
                st.markdown(texto_em_markdown)

            elif selected_section == "Implementação de Interface de Usuário Dinâmica":

                texto_em_markdown = read_markdown_file(arquivo_de_resposta2)
                st.markdown(texto_em_markdown)

            elif selected_section == "Extração de Conteúdo da Web para Alimentar a Aplicação":

                texto_em_markdown = read_markdown_file(arquivo_de_resposta3)
                st.markdown(texto_em_markdown)
                
                with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                    dados = json.load(file)

                st.markdown(f"###### Nuvem de Palavras dos Pacotes de Viagem:")
                gerar_nuvem_palavras(dados)

                st.markdown(f"###### Últimos dados extraídos:")
                
                with st.expander("Exibir dados do arquivo JSON"):
                    st.json(dados)  

            elif selected_section == "Cache e Estado de Sessão":

                texto_em_markdown = read_markdown_file(arquivo_de_resposta4)
                st.markdown(texto_em_markdown)

        else:
            st.write("Por favor, selecione uma seção no menu lateral.")
            

#################################################################################
############################           APP            ###########################
#################################################################################
with main_tab3:
    # abas secundárias
    sub_tab_b1, sub_tab_b2, sub_tab_b3 = st.tabs(["Home", "Área Restrita", "API Teste"])

    with sub_tab_b1:
        st.title("Pacotes de Viagem Disponíveis")

        # Área de login/logout
        col1, col2 = st.columns([3, 1])
        with col2:
            if not st.session_state.get('logged_in', False):
                with st.expander("Login"):
                    username = st.text_input("Usuário", key="username_home")
                    password = st.text_input("Senha", type="password", key="password_home")
                    if st.button("Login", key="login_button_home"):
                        result = login_user(username, password)
                        if result.get('status') == 'success':
                            st.session_state.logged_in = True
                            st.session_state.user = result.get('user', {})
                            st.rerun()
                        else:
                            st.error(f"Erro de login: {result.get('detail', 'Usuário ou senha incorretos')}")
            else:
                st.write(f"Bem-vindo, {st.session_state.user['profile']['first_name']}!")
                if st.button("Logout", key="logout_home"):
                    st.session_state.logged_in = False
                    st.session_state.user = None
                    st.rerun()

        with col1:
            pacotes = get_pacotes_viagem()
            
            # Criar um layout de grade para os cards
            cols = st.columns(3)  # Você pode ajustar o número de colunas conforme necessário
            
            for i, pacote in enumerate(pacotes):
                with cols[i % 3]:
                    # Criar um card para cada pacote
                    with st.container():
                        # Tentar carregar a imagem
                        try:
                            response = requests.get(f"https:{pacote['imagem']}")
                            img = Image.open(io.BytesIO(response.content))
                            st.image(img, use_column_width=True)
                        except:
                            st.image("https://via.placeholder.com/300x200?text=Imagem+não+disponível", use_column_width=True)
                        
                        st.subheader(pacote['titulo'])
                        st.write(f"Preço: R$ {pacote['preco_atual']}")
                        st.write(f"Duração: {pacote['duracao']}")
                        st.write(f"Datas: {pacote['datas']}")
                        
                        if pacote.get('economia'):
                            st.write(f"Economia: {pacote['economia']}")
                        
                        # Mostrar o botão apenas se o usuário estiver logado
                        if st.session_state.get('logged_in', False):
                            if st.button("Selecionar", key=f"select_{i}"):
                                st.success(f"Ótimo! Você selecionou o pacote de viagens {pacote['titulo']}!")
                        else:
                            st.info("Faça login para selecionar este pacote", icon="ℹ️")

    with sub_tab_b2:
        if not st.session_state.logged_in:
            st.title("Login")
            
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")

            if st.button("Login", key="login_button"):
                result = login_user(username, password)
                if result.get('status') == 'success':
                    st.session_state.logged_in = True
                    st.session_state.user = result.get('user', {})
                    st.rerun()
                else:
                    st.error(f"Erro de login: {result.get('detail', 'Usuário ou senha incorretos')}")
        else:
            if st.session_state.user and 'roles' in st.session_state.user and 'admin' in st.session_state.user['roles']:
                st.write("Área administrativa")
                st.write(f"Bem-vindo, {st.session_state.user['profile']['first_name']}")
                if st.button("Logout", key="logout_admin"):
                    st.session_state.logged_in = False
                    st.session_state.user = None
                    st.rerun()

#################################################################################
########################     OPERAÇÕES ADMINISTRATIVAS     ######################
#################################################################################
                #
                if 'dados' not in st.session_state:
                    st.session_state.dados = None

                option = st.radio(
                    "Escolha uma opção:",
                    ("Carregar arquivo JSON existente", "Executar novo scraping")
                )

                if option == "Carregar arquivo JSON existente":
                    uploaded_file = st.file_uploader("Escolha um arquivo JSON", type="json")
                    if uploaded_file is not None:
                        # Salva o arquivo uploadado no local desejado
                        if save_uploaded_file(uploaded_file):
                            st.success(f"Arquivo JSON salvo com sucesso em {arquivo_de_palavras}")
                        # Carrega os dados do arquivo salvo
                        with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                            st.session_state.dados = json.load(file)

                if option == "Executar novo scraping":
                    if st.button("Executar Scraper"):
                        with st.spinner("Executando o scraper..."):
                            run_scraper()
                        st.success("Scraping concluído!")
                        # Carregando os dados do arquivo gerado pelo scraper
                        with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                            st.session_state.dados = json.load(file)

                # Exibição dos dados
                if st.session_state.dados is not None:
                    st.markdown("##### Tabela de Ofertas:")
                    exibir_tabela_ofertas(st.session_state.dados)

                    st.markdown("##### Gráfico de Preços:")
                    exibir_grafico_precos(st.session_state.dados)

                    with st.expander("Exibir dados do arquivo JSON"):
                        st.json(st.session_state.dados)

                    # Botão de download
                    with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                        json_string = file.read()
                    
                    st.download_button(
                        label="Clique para baixar o JSON",
                        data=json_string,
                        file_name="dados_scraping.json",
                        mime="application/json"
                    )

                else:
                    st.info("Carregue um arquivo JSON ou execute o scraper para visualizar os dados.")




            else:
                st.warning("Você não tem permissão para acessar esta área")

    with sub_tab_b3:
        
        operation = st.selectbox("Select operation", ["Create", "Read", "Update", "Delete", "Get Main Collection"])

        if operation == "Create":
            collection = st.text_input("Collection name")
            data = st.text_area("Document data (JSON format)")
            if st.button("Create Document"):
                try:
                    json_data = json.loads(data)
                    result = api_request_cached("POST", f"/create/{collection}", {"data": json_data})
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
                    result = api_request_cached("GET", f"/read/{collection}?limit={limit}")
                    if result:
                        st.json(result)
                    else:
                        st.warning("No documents found or empty result.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    if hasattr(e, 'response'):
                        st.error(f"Response content: {e.response.content}")

        elif operation == "Update":
            collection = st.text_input("Collection name")
            doc_id = st.text_input("Document ID")
            data = st.text_area("Updated data (JSON format)")
            if st.button("Update Document"):
                try:
                    json_data = json.loads(data)
                    result = api_request_cached("PUT", f"/update/{collection}/{doc_id}", {"data": json_data})
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
                    result = api_request_cached("DELETE", f"/delete/{collection}/{doc_id}")
                    if result:
                        st.success("Document deleted successfully")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

        elif operation == "Get Main Collection":
            if st.button("Get Main Collection"):
                try:
                    result = api_request_cached("GET", "/main_collection")
                    if result:
                        st.json(result)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


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
