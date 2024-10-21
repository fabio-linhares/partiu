import streamlit as st
from utils.markdown import read_markdown_file
from utils.respostas import exibir_respostas
from utils.pacotes import exibir_pacotes_viagem
from utils.adm import exibir_area_restrita
from utils.api_teste import exibir_api_teste
from config.variaveis_globais import (
    config_vars,
    arquivo_de_apresentacao,
    arquivo_de_teste_tp2,
    arquivo_de_teste_tp3,
    arquivo_de_rubrica_tp2,
    arquivo_de_rubrica_tp3
)

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

def tab_contents(main_tab_names, num_sub_tabs, num_sub_tabs_test, selected_section, menu_dados):
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
                            with st.expander("TP2"):
                                adicionar_conteudo(lambda: read_markdown_file(arquivo_de_teste_tp2))
                            with st.expander("TP3"):
                                adicionar_conteudo(lambda: read_markdown_file(arquivo_de_teste_tp3))
                        elif j == 1:
                            with st.expander("TP2"):
                                adicionar_conteudo(lambda: read_markdown_file(arquivo_de_rubrica_tp2))
                            with st.expander("TP3"):
                                adicionar_conteudo(lambda: read_markdown_file(arquivo_de_rubrica_tp3))
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