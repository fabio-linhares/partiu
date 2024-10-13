import streamlit as st
from api import api_request

def login_user(username, password):

    try:
        response = api_request("POST", "/login", data={"username": username, "password": password})
        
        if response and isinstance(response, dict):
            return response
        else:
            return {"status": "error", "detail": "Resposta inválida do servidor"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}