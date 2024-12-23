import os
from utils.globals import create_global_variables

#################################################################################
############################       SECRETS.TOML       ###########################
#################################################################################



streamlit_secret = os.path.join(os.path.dirname(__file__), '../../.streamlit/secrets.toml')

image_directory = os.path.join(os.path.dirname(__file__), '../../images/.backgound')
infnet_image = os.path.join(os.path.dirname(__file__), '../../images/infnet30.png')
mec_image = os.path.join(os.path.dirname(__file__), '../../images/mec.png')


arquivo_de_apresentacao = os.path.join(os.path.dirname(__file__), '../../data/interim/apresentacao.txt')
arquivo_de_teste_tp2 = os.path.join(os.path.dirname(__file__), '../../data/interim/teste_tp2.txt')
arquivo_de_rubrica_tp2 = os.path.join(os.path.dirname(__file__), '../../data/interim/rubricas_tp2.txt')

arquivo_de_teste_tp3= os.path.join(os.path.dirname(__file__), '../../data/interim/teste_tp3.txt')
arquivo_de_rubrica_tp3 = os.path.join(os.path.dirname(__file__), '../../data/interim/rubricas_tp3.txt')

arquivo_de_palavras = os.path.join(os.path.dirname(__file__), '../../data/external/dados_completos.json')


# respostas
arquivo_de_resposta1 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/resposta1.txt')
arquivo_de_resposta2 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/resposta2.txt')
arquivo_de_resposta3 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/resposta3.txt')
arquivo_de_resposta4 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/resposta4.txt')

arquivo_de_respostatp3_1 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/respostatp3_1.txt')
arquivo_de_respostatp3_2 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/respostatp3_2.txt')
arquivo_de_respostatp3_3 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/respostatp3_3.txt')
arquivo_de_respostatp3_4 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/respostatp3_4.txt')
arquivo_de_respostatp3_5 = os.path.join(os.path.dirname(__file__), '../../data/interim/answers/respostatp3_5.txt')

config_vars = create_global_variables(streamlit_secret)

API_BASE_URL = "http://179.124.242.238:8000"
OLLAMA_API_URL = "http://179.124.242.238:11434/api/generate"
GOOGLE_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={config_vars['apikey_gemini']}"
GPT3_API_URL = f"https://api.openai.com/v1/chat/completions"

url_decolar = "https://www.decolar.com/pacotes/viagens-baratas/pacotes-prontos"

template_email = os.path.join(os.path.dirname(__file__), '../../data/templates/template_email.html')

template_email_cadastro = os.path.join(os.path.dirname(__file__), '../../data/templates/template_email_cadastro.html')