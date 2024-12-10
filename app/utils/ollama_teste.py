import requests
import json



url = "http://179.124.242.238:11434/api/generate"
payload = {
    "model": "llama3.2:1b",
    "prompt": "oi"}
       

def extrair_resposta(texto):
    linhas = texto.strip().split('\n')
    resposta_concatenada = ''
    for linha in linhas:
        try:
            dados = json.loads(linha)
            resposta_concatenada += dados.get('response', '')
        except json.JSONDecodeError:
            continue  # Ignora linhas que não são JSON válido
    return resposta_concatenada.strip()


headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=payload, headers=headers)
#print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")


resposta_concatenada = extrair_resposta(response.text)
print(resposta_concatenada)