###############################################################################
# Script Name    : database.py
# Description    : Funções para operações CRUD no MongoDB
# Args           : Vários, dependendo da função (veja docstrings)
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
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from utils.globals import create_global_variables
from config.variaveis_globais import streamlit_secret

config = create_global_variables(streamlit_secret)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection_string():
    """
    Gera a string de conexão para o MongoDB.

    Returns:
        str: String de conexão para o MongoDB.
    """
    return (f"{config['database_access_protocol']}://{config['database_access_user']}:"
            f"{config['database_access_password']}@{config['database_access_host']}:"
            f"{config['database_access_port']}/{config['database_access_database']}")

def get_database():
    """
    Estabelece conexão com o banco de dados MongoDB.

    Returns:
        pymongo.database.Database: Objeto de banco de dados MongoDB.

    Raises:
        PyMongoError: Se houver falha na conexão com o banco de dados.
    """
    try:
        client = MongoClient(get_connection_string())
        return client[config['database_main']]
    except PyMongoError as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

def get_collection(collection_name):
    """
    Obtém uma coleção específica do banco de dados.

    Args:
        collection_name (str): Nome da coleção.

    Returns:
        pymongo.collection.Collection: Objeto de coleção MongoDB.
    """
    db = get_database()
    return db[collection_name]

def create_document(collection_name, document):
    """
    Cria um novo documento em uma coleção específica.

    Args:
        collection_name (str): Nome da coleção.
        document (dict): Documento a ser inserido.

    Returns:
        pymongo.results.InsertOneResult: Resultado da operação de inserção.

    Raises:
        PyMongoError: Se houver falha na criação do documento.
    """
    try:
        collection = get_collection(collection_name)
        return collection.insert_one(document)
    except PyMongoError as e:
        logger.error(f"Failed to create document in {collection_name}: {e}")
        raise

def read_documents(collection_name, query=None, limit=None):
    """
    Lê documentos de uma coleção específica.

    Args:
        collection_name (str): Nome da coleção.
        query (dict, optional): Filtro de consulta. Defaults to None.
        limit (int, optional): Número máximo de documentos a retornar. Defaults to None.

    Returns:
        list: Lista de documentos encontrados.

    Raises:
        PyMongoError: Se houver falha na leitura dos documentos.
    """
    try:
        collection = get_collection(collection_name)
        return list(collection.find(query, limit=limit))
    except PyMongoError as e:
        logger.error(f"Failed to read documents from {collection_name}: {e}")
        raise

def update_document(collection_name, query, update):
    """
    Atualiza um documento em uma coleção específica.

    Args:
        collection_name (str): Nome da coleção.
        query (dict): Filtro para encontrar o documento a ser atualizado.
        update (dict): Atualizações a serem aplicadas ao documento.

    Returns:
        pymongo.results.UpdateResult: Resultado da operação de atualização.

    Raises:
        PyMongoError: Se houver falha na atualização do documento.
    """
    try:
        collection = get_collection(collection_name)
        return collection.update_one(query, {'$set': update})
    except PyMongoError as e:
        logger.error(f"Failed to update document in {collection_name}: {e}")
        raise

def delete_document(collection_name, query):
    """
    Exclui um documento de uma coleção específica.

    Args:
        collection_name (str): Nome da coleção.
        query (dict): Filtro para encontrar o documento a ser excluído.

    Returns:
        pymongo.results.DeleteResult: Resultado da operação de exclusão.

    Raises:
        PyMongoError: Se houver falha na exclusão do documento.
    """
    try:
        collection = get_collection(collection_name)
        return collection.delete_one(query)
    except PyMongoError as e:
        logger.error(f"Failed to delete document from {collection_name}: {e}")
        raise

def get_user_data():
    """
    Recupera dados do usuário da coleção específica.

    Returns:
        dict: Dados do usuário.
    """
    db = get_database()
    collection = db[config['collections_dev']]
    user_data = collection.find_one({})  # queremos o primeiro documento
    return user_data