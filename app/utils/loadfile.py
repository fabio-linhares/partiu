import json
import os

from config.variaveis_globais import (
    arquivo_de_palavras
)

def load_json_data(file):
    return json.load(file)

def save_uploaded_file(uploadedfile):
    with open(arquivo_de_palavras, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return True