import streamlit as st
import requests
from PIL import Image
import io
from datetime import datetime
from utils.mail import enviar_email, criar_conteudo_email
from utils.format_resposta import extrair_resposta_gemmini
from utils.globals import create_global_variables
from utils.format_resposta import (extrair_resposta_gemmini, 
                                   extrair_resposta_gpt)

from config.variaveis_globais import (
    streamlit_secret, 
    GOOGLE_API_URL,
    GPT3_API_URL
)
#################################################################################
############################       SECRETS.TOML       ###########################
#################################################################################

config_vars = create_global_variables(streamlit_secret)

def render_search_expander():
    if not st.session_state.get('logged_in', False):
        st.info("Faça login para utilizar nosso assistente especial para fugas.", icon="ℹ️")
    else:
        with st.expander("Precisa de ajuda para fugir?"):
            search_query = st.text_input("Diga-me por que está aqui e eu te ajudarei a escolher o melhor destino!")
            if st.button("Buscar"):
                process_search_query(search_query)


def process_search_query(search_query):
    if search_query:
        try:
            pacotes_texto = "\n".join([
                f"{pacote['titulo']} - Preço: R$ {pacote['preco_atual']}, Duração: {pacote['duracao']}, Datas: {pacote['datas']}"
                for pacote in st.session_state.pacotes[:1000]
            ])
            contexto = f"Pacotes disponíveis:\n{pacotes_texto}"
            prompt = f"""Considere que dispomos destas opções de pacotes de viagens: {contexto}; Considere isto: {search_query}; Considerando essas informações, utilize seu conhecimento para recomendar os 3 melhores pacotes ou destinos de viagem. Justifique sua escolha. Apresente algum conhecimento que possa aumentar o interesse pela sua recomandação. Não seja repetitivo ou prolixo. Seja sucinto."""

            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(GOOGLE_API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                resultado = response.json()
                resposta_concatenada = extrair_resposta_gemmini(resultado)
                st.write(resposta_concatenada)
            else:
                st.error(f"Erro na API: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {str(e)}")
            st.error(f"Tipo do erro: {type(e).__name__}")
            import traceback
            st.error(f"Traceback: {traceback.format_exc()}")
    else:
        st.warning("Por favor, insira uma consulta antes de buscar.")


def render_package_card(pacote, index):
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

        render_select_button(pacote, index)

def render_select_button(pacote, index):
    if st.session_state.get('logged_in', False):
        user_email = st.session_state.get('user_email', '')
        if st.button("Selecionar", key=f"select_{index}"):
            if user_email:
                user_data = st.session_state.get('user', {})
                if user_data:
                    process_package_selection(pacote, user_data, user_email)
                else:
                    st.error("Dados do usuário não encontrados. Por favor, faça login novamente.")
            else:
                st.error("E-mail do usuário não encontrado. Por favor, faça login novamente.")
    else:
        st.info("Faça login para selecionar este pacote", icon="ℹ️")

def process_package_selection(pacote, user_data, user_email):
    email_content = criar_conteudo_email(pacote, user_data)
    mail_subject = f"Confirmação de Reserva - {pacote['titulo']}"

    if config_vars['apikey_sendgrid']:
        with st.spinner("Efetuando a reserva..."):
            resultado = enviar_email(
                config_vars['apikey_sendgrid'],
                config_vars['mail_sender'],
                user_email,
                mail_subject,
                email_content
            )
            
            if resultado["status"] == "success":
                st.success("Um e-mail de confirmação foi enviado para você.", icon="✅")
            else:
                st.error(f"Erro ao enviar email: {resultado['message']}")
    else:
        st.error("Chave API do SendGrid não encontrada. Verifique o arquivo de configuração.")

    st.info("Nota: O email enviado pode cair na caixa de spam. Verifique lá se não o encontrar na caixa de entrada.")

def exibir_pacotes_viagem():
    st.markdown("#### Pacotes de Viagem")
    st.write("Aqui você encontra os pacotes de viagem mais recentes que 'raspamos' da 'decolar.com'. Xiuuu! kkkkkk")

    render_search_expander()

    cols = st.columns(3)
    for i, pacote in enumerate(st.session_state.pacotes):
        with cols[i % 3]:
            render_package_card(pacote, i)

#gpt
def process_search_query_2(search_query):
    global use_google_api  

    if search_query:
        try:
            pacotes_texto = "\n".join([
                f"{pacote['titulo']} - Preço: R$ {pacote['preco_atual']}, Duração: {pacote['duracao']}, Datas: {pacote['datas']}"
                for pacote in st.session_state.pacotes[:1000]
            ])
            contexto = f"Pacotes disponíveis:\n{pacotes_texto}"
            prompt = f"""Considere que dispomos destas opções de pacotes de viagens: {contexto}; Considere isto: {search_query}; Considerando essas informações, utilize seu conhecimento para recomendar os 3 melhores pacotes ou destinos de viagem. Justifique sua escolha. Apresente algum conhecimento que possa aumentar o interesse pela sua recomandação. Não seja repetitivo ou prolixo. Seja sucinto."""

            headers = {'Content-Type': 'application/json'}

            if use_google_api:
                print("Usando a API do Google")
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                response = requests.post(GOOGLE_API_URL, json=payload, headers=headers)

                if response.status_code == 200:
                    resultado = response.json()
                    resposta_concatenada = extrair_resposta_gemmini(resultado)
                    st.write(resposta_concatenada)
                else:
                    st.error(f"Erro na API Google: {response.status_code} - {response.text}")

            else:
                # Chamada à API do GPT
                payload = {
                    #"model": "gpt-3.5-turbo",  # Modelo apropriado
                    "model_type": "text-davinci-002",
                    "messages": [{"role": "user", "content": prompt}]
                }
                headers['Authorization'] = f"Bearer {config_vars['apikey_chatgpt']}"
                response = requests.post(GPT3_API_URL, json=payload, headers=headers)

                if response.status_code == 200:
                    resultado = response.json()
                    resposta_concatenada = extrair_resposta_gpt(resultado)
                    st.write(resposta_concatenada)
                elif response.status_code == 429:
                    st.error("Erro 429: Limite de uso da API GPT excedido. Verifique seu plano e detalhes de faturamento.")
                else:
                    st.error(f"Erro na API GPT: {response.status_code} - {response.text}")

            use_google_api = not use_google_api

        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {str(e)}")
            st.error(f"Tipo do erro: {type(e).__name__}")
            import traceback
            st.error(f"Traceback: {traceback.format_exc()}")
    else:
        st.warning("Por favor, insira uma consulta antes de buscar.")

