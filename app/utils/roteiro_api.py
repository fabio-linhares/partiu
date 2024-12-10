       
from openai import OpenAI
import os

# OBS: Abaixo mantenho a chave de API para o modelo 'nvidia/llama-3.1-nemotron-70b-instruct' da Nvidia, 
# ambora pudesse armazená-lo no arquivo 'secrets.toml', porque precisa
# fazer login no site da Nvidia toda vez que vou utilizá-la. Logo, não faz nenhum 'sentido' protegê-la!

def gerar_roteiro_viagem(destino, duracao):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
       api_key="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"

    )

    prompt = f"""
    Crie um roteiro de viagem empolgante para {destino} com duração de {duracao}. O roteiro deve:
    1. Focar em experiências únicas e atrações principais, sem mencionar informações básicas como chegada ou check-in.
    2. Incluir dicas de restaurantes locais e experiências gastronômicas.
    3. Sugerir atividades para diferentes perfis de viajantes (aventureiros, famílias, casais).
    4. Ser conciso, informativo e formatado em HTML para fácil leitura em e-mail.
    5. Não repetir informações como nome do destino, duração da viagem ou datas específicas.
    6. Utilizar emojis relevantes para tornar o roteiro mais atrativo visualmente.

    Formato desejado:
    <h2>Roteiro Personalizado para sua Aventura</h2>
    <ul>
        <li><strong>Dia 1:</strong> [Atividades do dia]</li>
        <li><strong>Dia 2:</strong> [Atividades do dia]</li>
        ...
    </ul>
    <h3>Dicas Especiais:</h3>
    <ul>
        <li>[Dica 1]</li>
        <li>[Dica 2]</li>
        ...
    </ul>
    """

    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            top_p=1,
            max_tokens=1024
        )

        roteiro = completion.choices[0].message.content
        return roteiro
    except Exception as e:
        print(f"Erro ao gerar roteiro: {str(e)}")
        return "<p>Desculpe, não foi possível gerar um roteiro personalizado neste momento. Entre em contato com nosso suporte para obter assistência adicional.</p>"