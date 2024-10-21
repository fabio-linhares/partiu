import streamlit as st
from utils.interface_admin import interface_admin
from utils.security import login_user

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
                
            if st.session_state.get('logged_in', False) and 'roles' in st.session_state.user and 'admin' in st.session_state.user['roles']:

                # Inicialize o session_state se não estiver definido
                if 'dados' not in st.session_state:
                    st.session_state.dados = None  # ou uma lista vazia, se for mais apropriado []
                    
                interface_admin()