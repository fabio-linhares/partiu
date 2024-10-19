import streamlit as st
import re
import unicodedata
from datetime import datetime
from api import api_request
from utils.mail import enviar_email
from api import get_sections_from_api, api_request_cached
from utils.database import get_user_data

from utils.globals import create_global_variables
from jinja2 import Environment, FileSystemLoader
import os

from config.variaveis_globais import (
    streamlit_secret,
    template_email_cadastro
)

config_vars = create_global_variables(streamlit_secret)

#################################################################################
############################       SECRETS.TOML       ###########################
#################################################################################



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


def normalize_username(username):
    # acentos
    username = unicodedata.normalize('NFKD', username).encode('ASCII', 'ignore').decode('ASCII')
    # converte para minúsculas e remove caracteres especiais
    username = re.sub(r'[^a-z0-9]', '', username.lower())
    return username

def render_cadastro_form():
    st.markdown(f"##### Cadastre-se! É rápido e fácil.")

    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            "username": "",
            "email": "",
            "password": "",
            "confirm_password": "",
            "first_name": "",
            "last_name": "",
            "birth_date": datetime.now(),
            "phone": ""
        }

    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            raw_username = st.text_input("Nome de usuário", key="form_data.username")
            username = normalize_username(raw_username) 
            email = st.text_input("E-mail", key="form_data.email")
            password = st.text_input("Senha", type="password", key="form_data.password")
            confirm_password = st.text_input("Confirme a senha", type="password", key="form_data.confirm_password")
        with col2:
            first_name = st.text_input("Nome", key="form_data.first_name")
            last_name = st.text_input("Sobrenome", key="form_data.last_name")
            birth_date = st.date_input("Data de nascimento", key="form_data.birth_date")
            phone = st.text_input("Telefone", key="form_data.phone")
        
        submit_button = st.form_submit_button("Cadastrar")
        
        if submit_button:
            if password != confirm_password:
                st.error("As senhas não coincidem.")
            elif raw_username != username:
                st.error("Nome de usuário inválido. Use apenas letras minúsculas e números, sem acentos ou caracteres especiais.")
            else:
                user_data = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "created_at": datetime.now().isoformat(),
                    "last_login": datetime.now().isoformat(),
                    "is_active": True,
                    "roles": ["user"],
                    "profile": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "birth_date": birth_date.strftime("%Y-%m-%d"),
                        "phone": phone
                    },
                    "settings": {
                        "theme": "default",
                        "notifications": True
                    }
                }
                
                response = api_request("POST", "/register", data=user_data)
                
                if response.get("status") == "success":
                    st.success("Cadastro realizado com sucesso!")
                    
                    # Enviar email de confirmação
                    email_content = f"""
                    <h3>Cadastro realizado com sucesso!</h3>
                    <p>Obrigado por se cadastrar. Aqui estão os seus dados:</p>
                    <ul>
                        <li>Nome de usuário: {username}</li>
                        <li>E-mail: {email}</li>
                        <li>Nome: {first_name} {last_name}</li>
                        <li>Data de nascimento: {birth_date.strftime("%d/%m/%Y")}</li>
                        <li>Telefone: {phone}</li>
                    </ul>
                    <p>Por favor, guarde este e-mail para referência futura.</p>
                    """
                    enviar_email(
                        smtp_password=config_vars['apikey_sendgrid'],
                        from_email=config_vars['mail_sender'],
                        to_email=email,
                        subject="Confirmação de Cadastro",
                        html_content=email_content
                    )
                    
                    # Redefinir estado do formulário
                    for key in st.session_state.form_data.keys():
                        st.session_state.form_data[key] = "" if key != "birth_date" else datetime.now()
                else:
                    st.error(f"Erro ao cadastrar: {response.get('detail', 'Erro desconhecido')}")
    
    if st.button("Não quero me cadastrar!"):
        st.session_state.show_cadastro = False
        st.rerun()


def enviar_email_confirmacao_cadastro(user_data):
    env = Environment(loader=FileSystemLoader('path/to/templates'))
    template = env.get_template('confirmacao_cadastro.html')

    email_content = template.render(
        first_name=user_data['profile']['first_name'],
        last_name=user_data['profile']['last_name'],
        username=user_data['username'],
        email=user_data['email'],
        birth_date=user_data['profile']['birth_date'],
        phone=user_data['profile']['phone'],
        support_mail=support_mail_,
        support_phone=support_phone_
    )

    

    enviar_email(
        smtp_password=config_vars['apikey_sendgrid'],
        from_email=config_vars['mail_sender'],
        to_email=user_data['email'],
        subject="Confirmação de Cadastro",
        html_content=email_content
    )