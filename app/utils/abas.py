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

# def render_tabs(selected_section, menu_dados):
#     main_tabs, main_tab_names = criar_abas_principais(config_vars)
    
#     def tabs_content():
#         for i, tab in enumerate(main_tabs):
#             with tab:
#                 if i == 0:  # Primeira aba principal
#                     sub_tabs, sub_tab_names = criar_abas_secundarias(config_vars, tab)
#                     for j, sub_tab in enumerate(sub_tabs):
#                         with sub_tab:
#                             if j == 0:
#                                 adicionar_conteudo(lambda: exibir_respostas(selected_section, menu_dados))
#                             elif j == 1:
#                                 adicionar_conteudo(exibir_pacotes_viagem)
#                             elif j == 2:
#                                 adicionar_conteudo(exibir_area_restrita)
#                 elif i == 1:  # Segunda aba principal
#                     adicionar_conteudo(exibir_api_teste)
    
#     return tabs_content

#################################################################################
############################        RESPOSTAS         ###########################
#################################################################################

# def criar_exibidor_respostas(selected_section, menu_dados):
#     def wrapper():
#         exibir_respostas(selected_section, menu_dados)
#     return wrapper

# Funções para exibir conteúdo específico
# def exibir_respostas(selected_section, menu_dados):
#     if selected_section:
#         selected_questions = next((item['questions'] for item in menu_dados if item['section'] == selected_section), [])
#         st.write(f"## {selected_section}")
#         for question in selected_questions:
#             st.write(question)

#         if selected_section == "TP2 - Configuração do Ambiente de Desenvolvimento":
#             texto_em_markdown = read_markdown_file(arquivo_de_resposta1)
#             st.markdown(texto_em_markdown)

#         elif selected_section == "TP2 - Implementação de Interface de Usuário Dinâmica":
#             texto_em_markdown = read_markdown_file(arquivo_de_resposta2)
#             st.markdown(texto_em_markdown)

#         elif selected_section == "TP2 - Extração de Conteúdo da Web para Alimentar a Aplicação":
#             texto_em_markdown = read_markdown_file(arquivo_de_resposta3)
#             st.markdown(texto_em_markdown)
            
#             with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
#                 dados = json.load(file)

#             st.markdown(f"###### Nuvem de Palavras dos Pacotes de Viagem:")
#             gerar_nuvem_palavras(dados)

#             st.markdown(f"###### Últimos dados extraídos:")
            
#             with st.expander("Exibir dados do arquivo JSON"):
#                 st.json(dados)  

#         elif selected_section == "TP2 - Cache e Estado de Sessão":
#             texto_em_markdown = read_markdown_file(arquivo_de_resposta4)
#             st.markdown(texto_em_markdown)

#         elif selected_section == "TP2 - Serviço de Upload e Download de Arquivos":
#             st.markdown(f"###### Foi implementado no APP")

#         elif selected_section == "TP2 - Finalização do Project Charter e Data Summary Report":
#             pass

#     else:
#         st.write("Por favor, selecione uma seção no menu lateral.")


##################################################################################################
############################        PACOTES DE VIAGEM         ####################################
##################################################################################################

# def render_search_expander():
#     if not st.session_state.get('logged_in', False):
#         st.info("Faça login para utilizar nosso assistente especial para fugas.", icon="ℹ️")
#     else:
#         with st.expander("Precisa de ajuda para fugir?"):
#             search_query = st.text_input("Diga-me por que está aqui e eu te ajudarei a escolher o melhor destino!")
#             if st.button("Buscar"):
#                 process_search_query(search_query)

# utiliza a API do Google e do GPT, alternando entre elas.
# def process_search_query_2(search_query):
#     global use_google_api  

#     if search_query:
#         try:
#             pacotes_texto = "\n".join([
#                 f"{pacote['titulo']} - Preço: R$ {pacote['preco_atual']}, Duração: {pacote['duracao']}, Datas: {pacote['datas']}"
#                 for pacote in st.session_state.pacotes[:1000]
#             ])
#             contexto = f"Pacotes disponíveis:\n{pacotes_texto}"
#             prompt = f"""Considere que dispomos destas opções de pacotes de viagens: {contexto}; Considere isto: {search_query}; Considerando essas informações, utilize seu conhecimento para recomendar os 3 melhores pacotes ou destinos de viagem. Justifique sua escolha. Apresente algum conhecimento que possa aumentar o interesse pela sua recomandação. Não seja repetitivo ou prolixo. Seja sucinto."""

#             headers = {'Content-Type': 'application/json'}

#             if use_google_api:
#                 print("Usando a API do Google")
#                 payload = {
#                     "contents": [{"parts": [{"text": prompt}]}]
#                 }
#                 response = requests.post(GOOGLE_API_URL, json=payload, headers=headers)

#                 if response.status_code == 200:
#                     resultado = response.json()
#                     resposta_concatenada = extrair_resposta_gemmini(resultado)
#                     st.write(resposta_concatenada)
#                 else:
#                     st.error(f"Erro na API Google: {response.status_code} - {response.text}")

#             else:
#                 # Chamada à API do GPT
#                 payload = {
#                     #"model": "gpt-3.5-turbo",  # Modelo apropriado
#                     "model_type": "text-davinci-002",
#                     "messages": [{"role": "user", "content": prompt}]
#                 }
#                 headers['Authorization'] = f"Bearer {config_vars['apikey_chatgpt']}"
#                 response = requests.post(GPT3_API_URL, json=payload, headers=headers)

#                 if response.status_code == 200:
#                     resultado = response.json()
#                     resposta_concatenada = extrair_resposta_gpt(resultado)
#                     st.write(resposta_concatenada)
#                 elif response.status_code == 429:
#                     st.error("Erro 429: Limite de uso da API GPT excedido. Verifique seu plano e detalhes de faturamento.")
#                 else:
#                     st.error(f"Erro na API GPT: {response.status_code} - {response.text}")

#             use_google_api = not use_google_api

#         except Exception as e:
#             st.error(f"Ocorreu um erro inesperado: {str(e)}")
#             st.error(f"Tipo do erro: {type(e).__name__}")
#             import traceback
#             st.error(f"Traceback: {traceback.format_exc()}")
#     else:
#         st.warning("Por favor, insira uma consulta antes de buscar.")

# def process_search_query(search_query):
#     if search_query:
#         try:
#             pacotes_texto = "\n".join([
#                 f"{pacote['titulo']} - Preço: R$ {pacote['preco_atual']}, Duração: {pacote['duracao']}, Datas: {pacote['datas']}"
#                 for pacote in st.session_state.pacotes[:1000]
#             ])
#             contexto = f"Pacotes disponíveis:\n{pacotes_texto}"
#             prompt = f"""Considere que dispomos destas opções de pacotes de viagens: {contexto}; Considere isto: {search_query}; Considerando essas informações, utilize seu conhecimento para recomendar os 3 melhores pacotes ou destinos de viagem. Justifique sua escolha. Apresente algum conhecimento que possa aumentar o interesse pela sua recomandação. Não seja repetitivo ou prolixo. Seja sucinto."""

#             payload = {
#                 "contents": [{"parts": [{"text": prompt}]}]
#             }
#             headers = {'Content-Type': 'application/json'}
#             response = requests.post(GOOGLE_API_URL, json=payload, headers=headers)

#             if response.status_code == 200:
#                 resultado = response.json()
#                 resposta_concatenada = extrair_resposta_gemmini(resultado)
#                 st.write(resposta_concatenada)
#             else:
#                 st.error(f"Erro na API: {response.status_code} - {response.text}")
#         except Exception as e:
#             st.error(f"Ocorreu um erro inesperado: {str(e)}")
#             st.error(f"Tipo do erro: {type(e).__name__}")
#             import traceback
#             st.error(f"Traceback: {traceback.format_exc()}")
#     else:
#         st.warning("Por favor, insira uma consulta antes de buscar.")

# def render_package_card(pacote, index):
#     with st.container():
#         try:
#             response = requests.get(f"https:{pacote['imagem']}")
#             img = Image.open(io.BytesIO(response.content))
#             st.image(img, use_column_width=True)
#         except:
#             st.image("https://via.placeholder.com/300x200?text=Imagem+não+disponível", use_column_width=True)
        
#         st.subheader(pacote['titulo'])
#         st.write(f"Preço: R$ {pacote['preco_atual']}")
#         st.write(f"Duração: {pacote['duracao']}")
#         st.write(f"Datas: {pacote['datas']}")
        
#         if pacote.get('economia'):
#             st.write(f"Economia: {pacote['economia']}")

#         data_hora = datetime.strptime(f"{pacote['data_extracao']} {pacote['hora_extracao']}", "%Y-%m-%d %H:%M:%S")
#         data_hora_formatada = data_hora.strftime("%d/%m/%Y às %H:%M:%S")
#         st.write(f"Última atualização: {data_hora_formatada}")

#         render_select_button(pacote, index)

# def render_select_button(pacote, index):
#     if st.session_state.get('logged_in', False):
#         user_email = st.session_state.get('user_email', '')
#         if st.button("Selecionar", key=f"select_{index}"):
#             if user_email:
#                 user_data = st.session_state.get('user', {})
#                 if user_data:
#                     process_package_selection(pacote, user_data, user_email)
#                 else:
#                     st.error("Dados do usuário não encontrados. Por favor, faça login novamente.")
#             else:
#                 st.error("E-mail do usuário não encontrado. Por favor, faça login novamente.")
#     else:
#         st.info("Faça login para selecionar este pacote", icon="ℹ️")

# def process_package_selection(pacote, user_data, user_email):
#     email_content = criar_conteudo_email(pacote, user_data)
#     mail_subject = f"Confirmação de Reserva - {pacote['titulo']}"

#     if config_vars['apikey_sendgrid']:
#         with st.spinner("Efetuando a reserva..."):
#             resultado = enviar_email(
#                 config_vars['apikey_sendgrid'],
#                 config_vars['mail_sender'],
#                 user_email,
#                 mail_subject,
#                 email_content
#             )
            
#             if resultado["status"] == "success":
#                 st.success("Um e-mail de confirmação foi enviado para você.", icon="✅")
#             else:
#                 st.error(f"Erro ao enviar email: {resultado['message']}")
#     else:
#         st.error("Chave API do SendGrid não encontrada. Verifique o arquivo de configuração.")

#     st.info("Nota: O email enviado pode cair na caixa de spam. Verifique lá se não o encontrar na caixa de entrada.")

# def exibir_pacotes_viagem():
#     st.markdown("#### Pacotes de Viagem")
#     st.write("Aqui você encontra os pacotes de viagem mais recentes que 'raspamos' da 'decolar.com'. Xiuuu! kkkkkk")

#     render_search_expander()

#     cols = st.columns(3)
#     for i, pacote in enumerate(st.session_state.pacotes):
#         with cols[i % 3]:
#             render_package_card(pacote, i)



# def criar_conteudo_email(pacote, user_data):

#     env = Environment(loader=FileSystemLoader(os.path.dirname(template_email)))
#     template = env.get_template(os.path.basename(template_email))

#     # recupera os dados
#     data_extracao = datetime.strptime(pacote['data_extracao'], "%Y-%m-%d").strftime("%d/%m/%Y")
#     profile = user_data.get('profile', {})
#     first_name = profile.get('first_name', 'Cliente')
#     last_name = profile.get('last_name', '')
#     email = user_data.get('email', 'Não fornecido')
#     phone = profile.get('phone', 'Não fornecido')
#     birth_date = profile.get('birth_date')
#     data_nascimento = datetime.strptime(birth_date, "%Y-%m-%d").strftime("%d/%m/%Y") if birth_date else 'Não fornecido'
#     settings = user_data.get('settings', {})
#     notifications = 'Ativadas' if settings.get('notifications', False) else 'Desativadas'

#     # URL absoluta
#     imagem_url = f"https:{pacote['imagem']}" if not pacote['imagem'].startswith('http') else pacote['imagem']

#     return template.render(
#         first_name=first_name,
#         last_name=last_name,
#         destino=pacote['titulo'],
#         preco_atual=pacote['preco_atual'],
#         preco_original=pacote.get('preco_original', 'Não especificado'),
#         economia=pacote.get('economia', 'Não especificado'),
#         duracao=pacote['duracao'],
#         datas=pacote['datas'],
#         cidade_saida=pacote.get('cidade_saida', 'Indisponível'),
#         servicos_incluidos=pacote.get('servicos_incluidos', 'Não especificado'),
#         imagem=imagem_url,
#         data_extracao=data_extracao,
#         hora_extracao=pacote['hora_extracao'],
#         email=email,
#         phone=phone,
#         data_nascimento=data_nascimento,
#         notifications=notifications,
#         support_mail=support_mail_,
#         support_phone=support_phone_
#     )


# def exibir_area_restrita():
#     if not st.session_state.logged_in:
#         st.title("Login")
        
#         username = st.text_input("Usuário")
#         password = st.text_input("Senha", type="password")

#         if st.button("Login", key="login_button"):
#             result = login_user(username, password)
#             if result.get('status') == 'success':
#                 st.session_state.logged_in = True
#                 st.session_state.user = result.get('user', {})
#                 st.rerun()
#             else:
#                 st.error(f"Erro de login: {result.get('detail', 'Usuário ou senha incorretos')}")
#     else:
#         if st.session_state.user and 'roles' in st.session_state.user and 'admin' in st.session_state.user['roles']:
#             st.write("Área administrativa")
#             st.write(f"Bem-vindo, {st.session_state.user['profile']['first_name']}")
#             if st.button("Logout", key="logout_admin"):
#                 st.session_state.logged_in = False
#                 st.session_state.user = None
#                 st.rerun()

#################################################################################
########################     OPERAÇÕES ADMINISTRATIVAS     ######################
#################################################################################
            #
            # if st.session_state.get('logged_in', False) and 'roles' in st.session_state.user and 'admin' in st.session_state.user['roles']:

            #     # Inicialize o session_state se não estiver definido
            #     if 'dados' not in st.session_state:
            #         st.session_state.dados = None  # ou uma lista vazia, se for mais apropriado []
                    
            #     interface_admin()
                
            #     if 'dados' not in st.session_state:
            #         st.session_state.dados = None

            #     option = st.radio(
            #         "Escolha uma opção:",
            #         ("Carregar arquivo JSON existente", "Executar novo scraping", "Adicionar Nova Questão")
            #     )

            #     if option == "Carregar arquivo JSON existente":
            #         uploaded_file = st.file_uploader("Escolha um arquivo JSON", type="json")
            #         if uploaded_file is not None:

            #             if save_uploaded_file(uploaded_file):
            #                 st.success(f"Arquivo JSON salvo com sucesso em {arquivo_de_palavras}")

            #             with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
            #                 st.session_state.dados = json.load(file)

            #     elif option == "Executar novo scraping":
            #         if st.button("Executar Scraper"):
            #             with st.spinner("Executando o scraper..."):
            #                 run_scraper()
            #             st.success("Scraping concluído!")

            #             with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
            #                 st.session_state.dados = json.load(file)

            #     elif option == "Adicionar Nova Questão":
            #         render_add_question_form()

            #     if st.session_state.dados is not None:
            #         st.markdown("##### Tabela de Ofertas:")
            #         exibir_tabela_ofertas(st.session_state.dados)

            #         st.markdown("##### Gráfico de Preços:")
            #         exibir_grafico_precos(st.session_state.dados)

            #         with st.expander("Exibir dados do arquivo JSON"):
            #             st.json(st.session_state.dados)

            #         # Botão de download
            #         with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
            #             json_string = file.read()
                    
            #         st.download_button(
            #             label="Clique para baixar o JSON",
            #             data=json_string,
            #             file_name="dados_scraping.json",
            #             mime="application/json"
            #         )

            #     else:
            #         st.info("Carregue um arquivo JSON ou execute o scraper para visualizar os dados.")

            # else:
            #     st.warning("Você não tem permissão para acessar esta área")

#################################################################################
########################            TESTE DE API           ######################
#################################################################################

# def exibir_api_teste():
#     operation = st.selectbox("Select operation", ["Create", "Read", "Update", "Delete", "Get Main Collection"])

#     if operation == "Create":
#         collection = st.text_input("Collection name")
#         data = st.text_area("Document data (JSON format)")
#         if st.button("Create Document"):
#             try:
#                 json_data = json.loads(data)
#                 result = api_request_cached("POST", f"/create/{collection}", {"data": json_data})
#                 if result:
#                     st.success(f"Document created with ID: {result['id']}")
#             except json.JSONDecodeError:
#                 st.error("Invalid JSON format")
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")

#     elif operation == "Read":
#         collection = st.text_input("Collection name")
#         limit = st.number_input("Limit", min_value=1, value=10)
#         if st.button("Read Documents"):
#             try:
#                 result = api_request_cached("GET", f"/read/{collection}?limit={limit}")
#                 if result:
#                     st.json(result)
#                 else:
#                     st.warning("No documents found or empty result.")
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")
#                 if hasattr(e, 'response'):
#                     st.error(f"Response content: {e.response.content}")

#     elif operation == "Update":
#         collection = st.text_input("Collection name")
#         doc_id = st.text_input("Document ID")
#         data = st.text_area("Updated data (JSON format)")
#         if st.button("Update Document"):
#             try:
#                 json_data = json.loads(data)
#                 result = api_request_cached("PUT", f"/update/{collection}/{doc_id}", {"data": json_data})
#                 if result:
#                     st.success("Document updated successfully")
#             except json.JSONDecodeError:
#                 st.error("Invalid JSON format")
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")

#     elif operation == "Delete":
#         collection = st.text_input("Collection name")
#         doc_id = st.text_input("Document ID")
#         if st.button("Delete Document"):
#             try:
#                 result = api_request_cached("DELETE", f"/delete/{collection}/{doc_id}")
#                 if result:
#                     st.success("Document deleted successfully")
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")

#     elif operation == "Get Main Collection":
#         if st.button("Get Main Collection"):
#             try:
#                 result = api_request_cached("GET", "/main_collection")
#                 if result:
#                     st.json(result)
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")


# def render_tabs(selected_section, menu_dados):
#     main_tabs, main_tab_names = criar_abas_principais(config_vars)
    
#     def tabs_content():
#         for i, tab in enumerate(main_tabs):
#             with tab:
#                 if i == 0:  # Primeira aba principal
#                     sub_tabs, sub_tab_names = criar_abas_secundarias(config_vars, tab)
#                     for j, sub_tab in enumerate(sub_tabs):
#                         with sub_tab:
#                             if j == 0:
#                                 adicionar_conteudo(lambda: exibir_respostas(selected_section, menu_dados))
#                             elif j == 1:
#                                 adicionar_conteudo(exibir_pacotes_viagem)
#                             elif j == 2:
#                                 adicionar_conteudo(exibir_area_restrita)
#                 elif i == 1:  # Segunda aba principal
#                     adicionar_conteudo(exibir_api_teste)
    
#     return tabs_content

# if __name__ == "__main__":
#     exibir_pacotes_viagem()