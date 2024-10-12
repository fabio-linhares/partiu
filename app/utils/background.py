###############################################################################
# Script Name    : utils/background.py
# Description    : Seleciona uma imagem aleatória de um diretório especificado
# Args           : directory (str): Caminho para o diretório contendo as imagens
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

import os
import random
import streamlit as st

def get_random_image(directory):
    """
    Seleciona uma imagem aleatória de um diretório especificado.

    Esta função percorre o diretório fornecido, identifica todos os arquivos
    de imagem (com extensões .png, .jpg, .jpeg, ou .gif) e retorna o caminho
    completo para uma imagem aleatória selecionada.

    Args:
        directory (str): O caminho para o diretório contendo as imagens.

    Returns:
        str: O caminho completo para a imagem aleatória selecionada.

    Raises:
        ValueError: Se nenhuma imagem for encontrada no diretório especificado.

    Example:
        >>> random_image = get_random_image("/path/to/image/directory")
        >>> print(random_image)
        /path/to/image/directory/random_image.jpg
    """
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not image_files:
        raise ValueError(f"Nenhuma imagem encontrada no diretório {directory}")
    return os.path.join(directory, random.choice(image_files))

@st.cache_data
def get_cached_random_image(image_directory):
    return get_random_image(image_directory)