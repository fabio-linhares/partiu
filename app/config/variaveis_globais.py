import os

streamlit_secret = os.path.join(os.path.dirname(__file__), '../../.streamlit/secrets.toml')

image_directory = os.path.join(os.path.dirname(__file__), '../../images/.backgound')
infnet_image = os.path.join(os.path.dirname(__file__), '../../images/infnet30.png')
mec_image = os.path.join(os.path.dirname(__file__), '../../images/mec.png')


arquivo_de_apresentacao = os.path.join(os.path.dirname(__file__), '../../data/interim/apresentacao.txt')
arquivo_de_teste = os.path.join(os.path.dirname(__file__), '../../data/interim/teste.txt')
arquivo_de_rubrica = os.path.join(os.path.dirname(__file__), '../../data/interim/rubricas.txt')
arquivo_de_palavras = os.path.join(os.path.dirname(__file__), '../../data/external/dados_completos.json')


# respostas
arquivo_de_resposta1 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/resposta1.txt')
arquivo_de_resposta2 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/resposta2.txt')
arquivo_de_resposta3 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/resposta3.txt')
arquivo_de_resposta4 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/resposta4.txt')


API_BASE_URL = "http://179.124.242.238:8000"
url_decolar = "https://www.decolar.com/pacotes/viagens-baratas/pacotes-prontos"

template_email = os.path.join(os.path.dirname(__file__), '../../data/templates/template_email.html')
