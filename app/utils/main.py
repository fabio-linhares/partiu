###############################################################################
# Script Name    : app/main.py
# Description    : Inicializa o servidor FastAPI e fornece funções de utilidade
# Args           : None
# Author         : Fábio Linhares (zerocopia)
# Email          : zerodevsystem@gmail.com
# GitHub         : https://github.com/zerodevsystem
# LinkedIn       : https://www.linkedin.com/in/fabio-linhares/
# Created        : 2024-10-12
# Last Modified  : 2024-10-12
# Shell Version  : 5.2.37(1)-release
# OS Name        : Garuda Linux
# OS Type        : GNU/Linux
# OS Version     : 6.11.3-zen1-1-zen
###############################################################################

import logging
from api import app

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    
    # Configuração do Uvicorn
    uvicorn_config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(uvicorn_config)
    server.run()


