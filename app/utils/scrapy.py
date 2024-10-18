from datetime import datetime, timedelta
import requests
import time


from config.variaveis_globais import (
    API_BASE_URL
)

def atualizar_pacotes():
    while True:
        st.session_state.pacotes = get_pacotes_viagem()
        time.sleep(300)  # Atualiza a cada 5 minutos

def get_pacotes_viagem():
    try:
        # só os pacotes mais recentes
        response = requests.get(f"{API_BASE_URL}/read/pacotes_viagem?sort=-data_extracao,-hora_extracao&limit=50")
        response.raise_for_status()
        pacotes = response.json()['documents']
        
        # tenta agrupar pacotes por título e seleciona o mais recente de cada
        pacotes_recentes = {}
        for pacote in pacotes:
            titulo = pacote['titulo']
            if titulo not in pacotes_recentes or (
                pacote['data_extracao'] + ' ' + pacote['hora_extracao'] >
                pacotes_recentes[titulo]['data_extracao'] + ' ' + pacotes_recentes[titulo]['hora_extracao']
            ):
                pacotes_recentes[titulo] = pacote
        
        return list(pacotes_recentes.values())
    except requests.RequestException as e:
        st.error(f"Erro ao buscar pacotes de viagem: {e}")
        return []