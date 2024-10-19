import requests
import json



url = "http://179.124.242.238:11434/api/generate"
payload = {
    "model": "llama3.2:1b",
    "prompt": "oi"}
       
# payload = {
#     "model": "llama3.2:1b",
#     "prompt": "Considere que dispomos destas opções de pacotes de viagens: Pacotes disponíveis: Maceió - Preço: R$ 2.004, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 01 fev até qui 06 fev Recife - Preço: R$ 1.869, Duração: 6 Dias / 5 Noites, Datas: A partir de qui 21 nov até ter 26 nov Mendoza - Preço: R$ 3.763, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 01 fev até qui 06 fev Cusco - Preço: R$ 3.146, Duração: 8 Dias / 7 Noites, Datas: A partir de sáb 04 jan até sáb 11 jan Belo Horizonte - Preço: R$ 982, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 01 fev até qui 06 fev San Andrés - Preço: R$ 5.509, Duração: 6 Dias / 5 Noites, Datas: A partir de qua 12 fev até seg 17 fev Florianópolis - Preço: R$ 1.912, Duração: 5 Dias / 4 Noites, Datas: A partir de sáb 04 jan até qua 08 jan Salvador Básico - Preço: R$ 4.487, Duração: 6 Dias / 5 Noites, Datas: A partir de dom 29 dez até sex 03 jan Penha com Ingresso Beto Carrero - Preço: R$ 1.921, Duração: 5 Dias / 4 Noites, Datas: A partir de qua 08 jan até dom 12 jan Florianópolis com ingresso Beto Carrero - Preço: R$ 1.862, Duração: 5 Dias / 4 Noites, Datas: A partir de seg 23 dez até sex 27 dez Maragogi - Preço: R$ 3.381, Duração: 5 Dias / 4 Noites, Datas: A partir de qui 06 fev até seg 10 fev Cancun - Preço: R$ 6.768, Duração: 8 Dias / 7 Noites, Datas: A partir de sáb 04 jan até sáb 11 jan Ushuaia Básico - Preço: R$ 3.223, Duração: 8 Dias / 7 Noites, Datas: A partir de ter 26 nov até ter 03 dez Natal - Preço: R$ 2.327, Duração: 6 Dias / 5 Noites, Datas: A partir de sex 14 fev até qua 19 fev Foz do Iguaçu - Preço: R$ 1.754, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 04 jan até qui 09 jan Porto de Galinhas - Preço: R$ 1.740, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 07 dez até qui 12 dez Fortaleza - Preço: R$ 2.518, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 02 nov até qui 07 nov Punta Cana - Preço: R$ 6.107, Duração: 8 Dias / 7 Noites, Datas: A partir de sáb 16 nov até sáb 23 nov Rio de Janeiro - Preço: R$ 2.471, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 01 mar até qui 06 mar Salvador - Preço: R$ 2.266, Duração: 6 Dias / 5 Noites, Datas: A partir de ter 14 jan até dom 19 jan Orlando - Preço: R$ 4.409, Duração: 12 Dias / 11 Noites, Datas: A partir de qua 04 dez até dom 15 dez Caldas Novas - Preço: R$ 1.905, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 01 fev até qui 06 fev Curitiba - Preço: R$ 869, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 07 dez até qui 12 dez Cartagena de Indias - Preço: R$ 4.917, Duração: 5 Dias / 4 Noites, Datas: A partir de sex 15 nov até ter 19 nov Morro de São Paulo - Preço: R$ 3.647, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 07 dez até qui 12 dez Buenos Aires - Preço: R$ 1.482, Duração: 4 Dias / 3 Noites, Datas: A partir de ter 10 dez até sex 13 dez Vitória Básico - Preço: R$ 1.319, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 07 dez até qui 12 dez Montevidéu - Preço: R$ 3.834, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 01 mar até qui 06 mar Paris - Preço: R$ 4.554, Duração: 9 Dias / 8 Noites, Datas: A partir de ter 18 fev até qua 26 fev Penha - Preço: R$ 1.435, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 01 mar até qui 06 mar Cancún - Preço: R$ 5.020, Duração: 8 Dias / 7 Noites, Datas: A partir de dom 09 mar até dom 16 mar Santiago - Preço: R$ 2.298, Duração: 6 Dias / 5 Noites, Datas: A partir de sáb 04 jan até qui 09 jan; Considere isto: tenho pouco dinheiro. e não gosto de praia; Considerando essas informações, utilize seu conhecimento para recomendar os 3 melhores pacotes ou destinos de viagem. Justifique sua escolha. Oferece resposta sucinta."
# }

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