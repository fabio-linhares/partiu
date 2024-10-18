# Third-party libraries
import streamlit as st
import bcrypt
from utils.database import update_document, get_collection



# Local modules
from config.variaveis_globais import (
    streamlit_secret, 
    image_directory,  
    arquivo_de_apresentacao, 
    arquivo_de_teste, 
    arquivo_de_rubrica
)


from utils.abas import (adicionar_conteudo,
                        exibir_respostas,
                        exibir_pacotes_viagem,
                        exibir_area_restrita,
                        exibir_api_teste,)

from utils.markdown import read_markdown_file
from utils.background import get_cached_random_image
from utils.globals import create_global_variables

from utils.frescuras import (contar_itens_config)



#################################################################################
############################       SECRETS.TOML       ###########################
#################################################################################
config_vars = create_global_variables(streamlit_secret)


def render_main_image():
    random_image_path = get_cached_random_image(image_directory)
    capa_site = random_image_path
    st.image(capa_site, use_column_width=True)

def render_tabs(selected_section, menu_dados):
    num_main_tabs = contar_itens_config(config_vars, 'main_tab') + 1
    num_sub_tabs = contar_itens_config(config_vars, 'sub_tab') + 1
    num_sub_tabs_test = contar_itens_config(config_vars, 'sub_tab_test') + 1

    # Criar abas principais
    main_tab_names = [config_vars[f'main_tab_{i}'] for i in range(1, num_main_tabs)] 

    def tab_contents():

        main_tabs = st.tabs(main_tab_names)

        for i, tab in enumerate(main_tabs):
            with tab:
                if main_tab_names[i] == config_vars['main_tab_2']:  # "O Projeto"
                    adicionar_conteudo(lambda: read_markdown_file(arquivo_de_apresentacao))
                
                elif main_tab_names[i] == config_vars['main_tab_3']:  # "O Teste"
                    sub_tab_names = [config_vars[f'sub_tab_test_{j}'] for j in range(1, num_sub_tabs_test)]
                    sub_tabs = st.tabs(sub_tab_names)
                    
                    for j, sub_tab in enumerate(sub_tabs):
                        with sub_tab:
                            if j == 0:
                                adicionar_conteudo(lambda: read_markdown_file(arquivo_de_teste))
                            elif j == 1:
                                adicionar_conteudo(lambda: read_markdown_file(arquivo_de_rubrica))
                            elif j == 2:
                                adicionar_conteudo(lambda: exibir_respostas(selected_section, menu_dados))
                
                elif main_tab_names[i] == config_vars['main_tab_1']:  # "O App"
                    sub_tab_names = [config_vars[f'sub_tab_{j}'] for j in range(1, num_sub_tabs)]
                    sub_tabs = st.tabs(sub_tab_names)
                    
                    for j, sub_tab in enumerate(sub_tabs):
                        with sub_tab:
                            if j == 0:
                                adicionar_conteudo(exibir_pacotes_viagem)
                            elif j == 1:
                                adicionar_conteudo(exibir_area_restrita)
                            elif j == 2:
                                adicionar_conteudo(exibir_api_teste)
    return tab_contents

def render_alterar_senha_form():
    st.markdown("##### Alterar Senha")

    with st.form("alterar_senha_form"):
        senha_atual = st.text_input("Senha Atual", type="password")
        nova_senha = st.text_input("Nova Senha", type="password")
        confirmar_nova_senha = st.text_input("Confirme a Nova Senha", type="password")
        
        submit_button = st.form_submit_button("Alterar Senha")
        
        if submit_button:
            if nova_senha != confirmar_nova_senha:
                st.error("As senhas não coincidem.")
            else:
                # Verificar a senha atual
                user = st.session_state.user
                collection = get_collection('tp_users')
                user_record = collection.find_one({'username': user['username']})

                if user_record and bcrypt.checkpw(senha_atual.encode('utf-8'), user_record['password'].encode('utf-8')):
                    # Atualizar com a nova senha
                    hashed_password = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
                    update_document(
                        collection_name='tp_users',
                        query={'username': user['username']},
                        update={'password': hashed_password.decode('utf-8')}
                    )
                    st.success("Senha alterada com sucesso!")
                else:
                    st.error("Senha atual incorreta.")