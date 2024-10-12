
import streamlit as st

from api import api_request
from utils.globals import create_global_variables
from config.variaveis_globais import streamlit_secret

config_vars = create_global_variables(streamlit_secret)

if 'used_titles' not in st.session_state:
    st.session_state.used_titles = []
    
def get_random_title(database, collection):
    try:
        result = api_request("GET", f"/random_title/{database}/{collection}")
        if 'titulo' in result:
            new_title = result['titulo']
            
            if len(st.session_state.used_titles) >= 10:
                st.session_state.used_titles = []
            
            while new_title in st.session_state.used_titles:
                result = api_request("GET", f"/random_title/{database}/{collection}")
                new_title = result['titulo']
            
            st.session_state.used_titles.append(new_title)
            return new_title
        else:
            st.error(f"Resposta inesperada da API: {result}")
            return config_vars['app_title']
    except Exception as e:
        st.error(f"Erro ao buscar título aleatório: {str(e)}")
        if hasattr(e, 'response'):
            st.error(f"Detalhes do erro: {e.response.text}")
        return config_vars['app_title']
