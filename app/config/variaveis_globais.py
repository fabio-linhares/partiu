import os

streamlit_secret = os.path.join(os.path.dirname(__file__), '../../.streamlit/secrets.toml')

image_directory = os.path.join(os.path.dirname(__file__), '../../images/.backgound')
infnet_image = os.path.join(os.path.dirname(__file__), '../../images/infnet30.png')
mec_image = os.path.join(os.path.dirname(__file__), '../../images/mec.png')


arquivo_de_apresentacao = os.path.join(os.path.dirname(__file__), '../../data/interim/apresentacao.txt')
arquivo_de_teste = os.path.join(os.path.dirname(__file__), '../../data/interim/teste.txt')
arquivo_de_rubrica = os.path.join(os.path.dirname(__file__), '../../data/interim/rubricas.txt')

API_BASE_URL = "http://179.124.242.238:8000"