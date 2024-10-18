import streamlit as st
import re
import unicodedata
from datetime import datetime
from api import api_request
from utils.mail import enviar_email
from utils.globals import create_global_variables

from config.variaveis_globais import (
    streamlit_secret
)

config_vars = create_global_variables(streamlit_secret)


def normalize_username(username):
    # Remover acentos
    username = unicodedata.normalize('NFKD', username).encode('ASCII', 'ignore').decode('ASCII')
    # Converter para minúsculas e remover caracteres especiais
    username = re.sub(r'[^a-z0-9]', '', username.lower())
    return username

def render_cadastro_form():
    st.markdown(f"##### Cadastre-se! É rápido e fácil.")

    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            raw_username = st.text_input("Nome de usuário", key="username")
            username = normalize_username(raw_username)  # Normalizar o nome de usuário
            email = st.text_input("E-mail", key="email")
            password = st.text_input("Senha", type="password", key="password")
            confirm_password = st.text_input("Confirme a senha", type="password", key="confirm_password")
        with col2:
            first_name = st.text_input("Nome", key="first_name")
            last_name = st.text_input("Sobrenome", key="last_name")
            birth_date = st.date_input("Data de nascimento", key="birth_date")
            phone = st.text_input("Telefone", key="phone")
        
        submit_button = st.form_submit_button("Cadastrar")
        
        if submit_button:
            if password != confirm_password:
                st.error("As senhas não coincidem.")
            elif raw_username != username:
                st.error("Nome de usuário inválido. Use apenas letras minúsculas e números, sem acentos ou caracteres especiais.")
            else:
                # Preparar dados para enviar à API
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
                
                # Fazer a solicitação à API para criar o usuário
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
                    st.experimental_rerun()
                else:
                    st.error(f"Erro ao cadastrar: {response.get('detail', 'Erro desconhecido')}")
    
    if st.button("Não quero me cadastrar!"):
        st.session_state.show_cadastro = False
        st.rerun()