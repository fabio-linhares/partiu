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

def extrair_resposta_gemmini(resultado):
    """
    Extrai e concatena o texto da resposta de um dicionário JSON retornado pela API.

    Parâmetros:
    - resultado (dict): O dicionário JSON retornado pela API.

    Retorna:
    - str: O texto concatenado extraído do dicionário.
    """
    resposta_concatenada = ''

    # Verifica se a estrutura contém 'candidates' e navega até 'text'
    if 'candidates' in resultado:
        for candidate in resultado['candidates']:
            content = candidate.get('content', {})
            parts = content.get('parts', [])
            for part in parts:
                resposta_concatenada += part.get('text', '')

    return resposta_concatenada.strip()