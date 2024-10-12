###############################################################################
# Script Name    : utils/globals.py
# Description    : Carrega configurações de um arquivo TOML e cria variáveis globais
# Args           : file_path (str): Caminho para o arquivo TOML
# Author         : Fábio Linhares (zerocopia)
# Email          : zerodevsystem@gmail.com
# GitHub         : https://github.com/zerodevsystem
# LinkedIn       : https://www.linkedin.com/in/fabio-linhares/
# Created        : 2024-10-11
# Last Modified  : 2024-10-12
# Shell Version  : 5.2.37(1)-release
# OS Name        : Garuda Linux
# OS Type        : GNU/Linux
# OS Version     : 6.11.3-zen1-1-zen
###############################################################################

import toml

def create_global_variables(file_path):
    """
    Carrega um arquivo TOML e cria variáveis globais a partir dele.
    
    Esta função lê um arquivo TOML especificado, processa seu conteúdo e cria
    variáveis globais baseadas nas seções e chaves do arquivo. As variáveis
    globais são nomeadas no formato "secao_chave".

    Args:
        file_path (str): Caminho para o arquivo TOML a ser carregado.

    Returns:
        dict: Um dicionário contendo as variáveis globais criadas, onde as
              chaves são os nomes das variáveis e os valores são seus
              respectivos conteúdos.

    Raises:
        FileNotFoundError: Se o arquivo TOML especificado não for encontrado.
        toml.TomlDecodeError: Se houver um erro na decodificação do arquivo TOML.

    Example:
        >>> config_vars = create_global_variables('config.toml')
        >>> print(config_vars)
        {'database_host': 'localhost', 'database_port': 5432, ...}
    """
    global_vars = {}
    
    try:
        config = toml.load(file_path)
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return global_vars
    except toml.TomlDecodeError:
        print(f"Erro ao decodificar o arquivo TOML: {file_path}")
        return global_vars
    
    for section, values in config.items():
        if isinstance(values, dict):
            for key, value in values.items():
                var_name = f"{section}_{key}"
                globals()[var_name] = value
                global_vars[var_name] = value
    
    return global_vars