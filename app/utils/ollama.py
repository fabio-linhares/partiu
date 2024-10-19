import requests
import json
from config.variaveis_globais import OLLAMA_API_URL

def get_llama3_response(prompt):
    payload = {
        "model": "llama3.2:1b",
        "prompt": prompt
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(OLLAMA_API_URL, data=json.dumps(payload), headers=headers, stream=True)
    
    if response.status_code == 200:
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_response = json.loads(line)
                    full_response += json_response.get('response', '')
                except json.JSONDecodeError:
                    print(f"Erro ao decodificar JSON: {line}")
        return full_response
    else:
        return f"Erro ao conectar com a API Ollama. Status code: {response.status_code}"