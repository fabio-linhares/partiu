import streamlit as st
import json
from utils.markdown import read_markdown_file
from utils.frescuras import gerar_nuvem_palavras


from config.variaveis_globais import (
    streamlit_secret, 
    arquivo_de_resposta1,
    arquivo_de_resposta2,
    arquivo_de_resposta3,
    arquivo_de_resposta4,
    arquivo_de_palavras,
    arquivo_de_respostatp3_1,
    arquivo_de_respostatp3_2,
    arquivo_de_respostatp3_3,
    arquivo_de_respostatp3_4,
    arquivo_de_respostatp3_5,
    template_email,
    OLLAMA_API_URL,
    GOOGLE_API_URL,
    GPT3_API_URL
)

def criar_exibidor_respostas(selected_section, menu_dados):

    def wrapper():
        exibir_respostas(selected_section, menu_dados)
    return wrapper

def exibir_respostas(selected_section, menu_dados):
    if selected_section:
        selected_questions = next((item['questions'] for item in menu_dados if item['section'] == selected_section), [])
        st.write(f"## {selected_section}")
        for question in selected_questions:
            st.write(question)

        if selected_section == "TP2 - Configuração do Ambiente de Desenvolvimento":
            texto_em_markdown = read_markdown_file(arquivo_de_resposta1)
            st.markdown(texto_em_markdown)

        elif selected_section == "TP2 - Implementação de Interface de Usuário Dinâmica":
            texto_em_markdown = read_markdown_file(arquivo_de_resposta2)
            st.markdown(texto_em_markdown)

        elif selected_section == "TP2 - Extração de Conteúdo da Web para Alimentar a Aplicação":
            texto_em_markdown = read_markdown_file(arquivo_de_resposta3)
            st.markdown(texto_em_markdown)
            
            with open(arquivo_de_palavras, 'r', encoding='utf-8') as file:
                dados = json.load(file)

            st.markdown(f"###### Nuvem de Palavras dos Pacotes de Viagem:")
            gerar_nuvem_palavras(dados)

            st.markdown(f"###### Últimos dados extraídos:")
            
            with st.expander("Exibir dados do arquivo JSON"):
                st.json(dados)  

        elif selected_section == "TP2 - Cache e Estado de Sessão":
            texto_em_markdown = read_markdown_file(arquivo_de_resposta4)
            st.markdown(texto_em_markdown)

        elif selected_section == "TP2 - Serviço de Upload e Download de Arquivos":
            st.markdown(f"###### Foi implementado no APP")

        elif selected_section == "TP2 - Finalização do Project Charter e Data Summary Report":
            pass

        elif selected_section == "TP3 - Criação de uma Aplicação com Múltiplas Páginas":
            texto_em_markdown = read_markdown_file(arquivo_de_respostatp3_1)
            st.markdown(texto_em_markdown)

        elif selected_section == "TP3 - Extração de Dados de Páginas Dinâmicas (Web Scraping)":
            texto_em_markdown = read_markdown_file(arquivo_de_respostatp3_2)
            st.markdown(texto_em_markdown)

        elif selected_section == "TP3 - Desenvolvimento de APIs com FastAPI":
            texto_em_markdown = read_markdown_file(arquivo_de_respostatp3_3)
            st.markdown(texto_em_markdown)

        elif selected_section == "TP3 - Preparação para Uso de Inteligência Artificial com LLMs":
            texto_em_markdown = read_markdown_file(arquivo_de_respostatp3_4)
            st.markdown(texto_em_markdown)

        elif selected_section == "TP3 - Revisão e Atualização da Documentação":
            # texto_em_markdown = read_markdown_file(arquivo_de_respostatp3_5)
            # st.markdown(texto_em_markdown)
            pass
    else:
        st.write("Por favor, selecione uma seção no menu lateral.")
