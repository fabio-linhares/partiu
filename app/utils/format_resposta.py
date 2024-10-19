import json

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
