import smtplib
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api import get_sections_from_api
from utils.database import get_user_data
from utils.globals import create_global_variables
from config.variaveis_globais import (
    streamlit_secret, 
    template_email,

)
#################################################################################
############################       SECRETS.TOML       ###########################
#################################################################################

config_vars = create_global_variables(streamlit_secret)


#################################################################################
############################         VARIÁVEIS        ###########################
#################################################################################

dev_data = get_user_data(database_name=config_vars['database_user'], 
                                     collection_name=config_vars['collections_dev'])

menu_dados = get_sections_from_api(config_vars['database_main'], 
                                   config_vars['collections_menu'])

if dev_data:
    support_mail_ = dev_data.get('email', config_vars['developer_email'])
    support_phone_ = dev_data.get('telefone', config_vars['developer_phone']) 

use_google_api = True

def enviar_email(smtp_password, from_email, to_email, subject, html_content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email

    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        with smtplib.SMTP("smtp.sendgrid.net", 587) as server:
            server.starttls()
            server.login("apikey", smtp_password)
            server.sendmail(from_email, to_email, message.as_string())
        return {"status": "success", "message": "Email enviado com sucesso!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

def criar_conteudo_email(pacote, user_data):

    env = Environment(loader=FileSystemLoader(os.path.dirname(template_email)))
    template = env.get_template(os.path.basename(template_email))

    # recupera os dados
    data_extracao = datetime.strptime(pacote['data_extracao'], "%Y-%m-%d").strftime("%d/%m/%Y")
    profile = user_data.get('profile', {})
    first_name = profile.get('first_name', 'Cliente')
    last_name = profile.get('last_name', '')
    email = user_data.get('email', 'Não fornecido')
    phone = profile.get('phone', 'Não fornecido')
    birth_date = profile.get('birth_date')
    data_nascimento = datetime.strptime(birth_date, "%Y-%m-%d").strftime("%d/%m/%Y") if birth_date else 'Não fornecido'
    settings = user_data.get('settings', {})
    notifications = 'Ativadas' if settings.get('notifications', False) else 'Desativadas'

    # URL absoluta
    imagem_url = f"https:{pacote['imagem']}" if not pacote['imagem'].startswith('http') else pacote['imagem']

    return template.render(
        first_name=first_name,
        last_name=last_name,
        destino=pacote['titulo'],
        preco_atual=pacote['preco_atual'],
        preco_original=pacote.get('preco_original', 'Não especificado'),
        economia=pacote.get('economia', 'Não especificado'),
        duracao=pacote['duracao'],
        datas=pacote['datas'],
        cidade_saida=pacote.get('cidade_saida', 'Indisponível'),
        servicos_incluidos=pacote.get('servicos_incluidos', 'Não especificado'),
        imagem=imagem_url,
        data_extracao=data_extracao,
        hora_extracao=pacote['hora_extracao'],
        email=email,
        phone=phone,
        data_nascimento=data_nascimento,
        notifications=notifications,
        support_mail=support_mail_,
        support_phone=support_phone_
    )