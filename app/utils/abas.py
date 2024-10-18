# Built-in libraries
import json
import io
import os
from datetime import datetime

# Third-party libraries
import streamlit as st
import requests
from PIL import Image

from jinja2 import Environment, FileSystemLoader

# Local modules
from api import get_sections_from_api, api_request_cached
from config.variaveis_globais import (
    streamlit_secret, 
    arquivo_de_resposta1,
    arquivo_de_resposta2,
    arquivo_de_resposta3,
    arquivo_de_resposta4,
    arquivo_de_palavras,
    template_email
)
from utils.database import get_user_data
from utils.frescuras import (
    gerar_nuvem_palavras,
    get_tab_names,
    exibir_grafico_precos,
    exibir_tabela_ofertas
)
from utils.globals import create_global_variables
from utils.loadfile import save_uploaded_file
from utils.mail import enviar_email
from utils.markdown import read_markdown_file
from utils.mongo2 import load_database_config
from utils.scraper import run_scraper
from utils.security import login_user

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



#################################################################################
############################        RESPOSTAS         ###########################
#################################################################################

def criar_exibidor_respostas(selected_section, menu_dados):
    def wrapper():
        exibir_respostas(selected_section, menu_dados)
    return wrapper

# Funções para exibir conteúdo específico
def exibir_respostas(selected_section, menu_dados):
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

        elif selected_section == "Serviço de Upload e Download de Arquivos":
            st.markdown(f"###### Foi implementado no APP")

        elif selected_section == "Finalização do Project Charter e Data Summary Report":
            pass

    else:
        st.write("Por favor, selecione uma seção no menu lateral.")

# def exibir_pacotes_viagem():


#     st.markdown(f"#### Pacotes de Viagem")
#     st.write("Aqui você encontra os pacotes de viagem mais recentes que 'raspamos' da 'decolar.com'. Xiuuu! kkkkkk")

#     cols = st.columns(3)
                
#     for i, pacote in enumerate(st.session_state.pacotes):
#         with cols[i % 3]:
#             with st.container():
#                 try:
#                     response = requests.get(f"https:{pacote['imagem']}")
#                     img = Image.open(io.BytesIO(response.content))
#                     st.image(img, use_column_width=True)
#                 except:
#                     st.image("https://via.placeholder.com/300x200?text=Imagem+não+disponível", use_column_width=True)
                
#                 st.subheader(pacote['titulo'])
#                 st.write(f"Preço: R$ {pacote['preco_atual']}")
#                 st.write(f"Duração: {pacote['duracao']}")
#                 st.write(f"Datas: {pacote['datas']}")
                
#                 if pacote.get('economia'):
#                     st.write(f"Economia: {pacote['economia']}")

#                 data_hora = datetime.strptime(f"{pacote['data_extracao']} {pacote['hora_extracao']}", "%Y-%m-%d %H:%M:%S")
#                 data_hora_formatada = data_hora.strftime("%d/%m/%Y às %H:%M:%S")

#                 st.write(f"Última atualização: {data_hora_formatada}")
#                 if st.session_state.get('logged_in', False):
#                     user_email = st.session_state.get('user_email', '')
#                     if st.button("Selecionar", key=f"select_{i}"):

# #################################################################################
# ############################           EMAIL          ###########################
# #################################################################################

#                         if user_email:
#                             mail_subject = f"{config_vars['mail_subjectp1']} {pacote['titulo']} {config_vars['mail_subjectp2']}"

#                             if config_vars['apikey_sendgrid']:
#                                 with st.spinner("Efetuando a reserva..."):
#                                     resultado = enviar_email(config_vars['apikey_sendgrid'], config_vars['mail_sender'], user_email, mail_subject, config_vars['mail_content1'])
                                    
#                                     if resultado["status"] == "success":
#                                         st.info("Um e-mail de confirmação foi enviado para você.", icon="ℹ️")
#                                     else:
#                                         st.error(f"Erro ao enviar email: {resultado['message']}")
#                             else:
#                                 st.error("Senha SMTP do SendGrid não encontrada. Verifique o arquivo de configuração.")

#                             st.write("""
#                             Nota: O email enviado pode cair na caixa de spam. Verifique lá se não o encontrar na caixa de entrada.
#                             """)
#                         else:
#                             st.error("E-mail do usuário não encontrado. Por favor, faça login novamente.")
#                 else:
#                     st.info("Faça login para selecionar este pacote", icon="ℹ️")



from datetime import datetime
import streamlit as st
import requests
from PIL import Image
import io
from utils.mail import enviar_email
from utils.database import get_user_data

def exibir_pacotes_viagem():
    st.markdown("#### Pacotes de Viagem")
    st.write("Aqui você encontra os pacotes de viagem mais recentes que 'raspamos' da 'decolar.com'. Xiuuu! kkkkkk")

    cols = st.columns(3)
                
    for i, pacote in enumerate(st.session_state.pacotes):
        with cols[i % 3]:
            with st.container():
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

                data_hora = datetime.strptime(f"{pacote['data_extracao']} {pacote['hora_extracao']}", "%Y-%m-%d %H:%M:%S")
                data_hora_formatada = data_hora.strftime("%d/%m/%Y às %H:%M:%S")

                st.write(f"Última atualização: {data_hora_formatada}")
                if st.session_state.get('logged_in', False):
                    user_email = st.session_state.get('user_email', '')
                    if st.button("Selecionar", key=f"select_{i}"):
                        if user_email:
                            # pega os dados do usuário
                            user_data = st.session_state.get('user', {})
                            if user_data:
                                email_content = criar_conteudo_email(pacote, user_data)
                                
                                mail_subject = f"Confirmação de Reserva - {pacote['titulo']}"

                                if config_vars['apikey_sendgrid']:
                                    with st.spinner("Efetuando a reserva..."):
                                        resultado = enviar_email(
                                            config_vars['apikey_sendgrid'],
                                            config_vars['mail_sender'],
                                            user_email,
                                            f"Confirmação de Reserva - {pacote['titulo']}",
                                            email_content  # conteúdo HTML
                                        )
                                        
                                        if resultado["status"] == "success":
                                            st.success("Um e-mail de confirmação foi enviado para você.", icon="✅")
                                        else:
                                            st.error(f"Erro ao enviar email: {resultado['message']}")
                                else:
                                    st.error("Chave API do SendGrid não encontrada. Verifique o arquivo de configuração.")

                                st.info("Nota: O email enviado pode cair na caixa de spam. Verifique lá se não o encontrar na caixa de entrada.")
                            else:
                                st.error("Dados do usuário não encontrados. Por favor, faça login novamente.")
                        else:
                            st.error("E-mail do usuário não encontrado. Por favor, faça login novamente.")
                else:
                    st.info("Faça login para selecionar este pacote", icon="ℹ️")

def criar_conteudo_email(pacote, user_data):
    # Configurar o ambiente do Jinja2
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_email)))
    template = env.get_template(os.path.basename(template_email))

    # Configurar os dados
    data_extracao = datetime.strptime(pacote['data_extracao'], "%Y-%m-%d").strftime("%d/%m/%Y")
    profile = user_data.get('profile', {})
    first_name = profile.get('first_name', 'Cliente')
    last_name = profile.get('last_name', '')
    email = user_data.get('email', 'Não fornecido')
    phone = profile.get('phone', 'Não fornecido')
    birth_date = profile.get('birth_date')
    data_nascimento = datetime.strptime(birth_date, "%Y-%m-%d").strftime("%d/%m/%Y") if birth_date else 'Não fornecido'
    settings = user_data.get('settings', {})
    notifications = 'Ativadas' if settings.get('notifications', False) else 'Desativadas'

    # Assegurar que a URL da imagem é absoluta
    imagem_url = f"https:{pacote['imagem']}" if not pacote['imagem'].startswith('http') else pacote['imagem']

    # Renderizar o template com os dados
    return template.render(
        first_name=first_name,
        last_name=last_name,
        destino=pacote['titulo'],
        preco_atual=pacote['preco_atual'],
        preco_original=pacote.get('preco_original', 'Não especificado'),
        economia=pacote.get('economia', 'Não especificado'),
        duracao=pacote['duracao'],
        datas=pacote['datas'],
        cidade_saida=pacote.get('cidade_saida', 'Indisponível'),
        servicos_incluidos=pacote.get('servicos_incluidos', 'Não especificado'),
        imagem=imagem_url,
        data_extracao=data_extracao,
        hora_extracao=pacote['hora_extracao'],
        email=email,
        phone=phone,
        data_nascimento=data_nascimento,
        notifications=notifications
    )


def exibir_area_restrita():
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


def exibir_api_teste():
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