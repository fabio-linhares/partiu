from datetime import datetime, timedelta
import requests
import time
import streamlit as st


from config.variaveis_globais import (
    API_BASE_URL
)

def atualizar_pacotes():
    while True:
        st.session_state.pacotes = get_pacotes_viagem()
        time.sleep(300)  # 5 minutos

def get_pacotes_viagem():
    try:
        response = requests.get(f"{API_BASE_URL}/read/pacotes_viagem")
        response.raise_for_status()
        pacotes = response.json()['documents']
        
        # ordena pela data e hora de extração mais recente
        pacotes_ordenados = sorted(
            pacotes,
            key=lambda x: datetime.strptime(f"{x['data_extracao']} {x['hora_extracao']}", "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )
        
        # Agrupa por título e seleciona o mais recente de cada
        pacotes_recentes = {}
        for pacote in pacotes_ordenados:
            titulo = pacote['titulo']
            if titulo not in pacotes_recentes:
                pacotes_recentes[titulo] = pacote
        
        return list(pacotes_recentes.values())
    except requests.RequestException as e:
        st.error(f"Erro ao buscar pacotes de viagem: {e}")
        return []