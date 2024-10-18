import streamlit as st


def render_cadastro_form():
    st.markdown(f"##### Cadastre-se! É rápido e fácil.")

    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Nome de usuário")
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            confirm_password = st.text_input("Confirme a senha", type="password")
        with col2:
            first_name = st.text_input("Nome")
            last_name = st.text_input("Sobrenome")
            birth_date = st.date_input("Data de nascimento")
            phone = st.text_input("Telefone")
        
        submit_button = st.form_submit_button("Cadastrar")
        
        if submit_button:
            if password != confirm_password:
                st.error("As senhas não coincidem.")
            else:
                # Aqui você chamaria a API para registrar o usuário
                # Por enquanto, apenas mostraremos uma mensagem de sucesso
                st.success("Cadastro realizado com sucesso!")
                st.session_state.show_cadastro = False
    
    if st.button("Não quero me cadastrar!"):
        st.session_state.show_cadastro = False
        st.rerun()
