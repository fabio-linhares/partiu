import streamlit as st
from api import api_request

def login_user(username, password):
    try:
        response = api_request("POST", "/login", data={"username": username, "password": password})
        return response
    except Exception as e:
        st.error(f"Erro ao fazer login: {e}")
        return None