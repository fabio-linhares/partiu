###############################################################################
# Script Name    : app/api.py
# Description    : API FastAPI para operações CRUD no MongoDB
# Args           : Vários, dependendo da rota (veja docstrings)
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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.database import (create_document,
                            read_documents, 
                            update_document, 
                            delete_document, 
                            get_user_data)
from utils.globals import create_global_variables
from bson import ObjectId

import json
import requests
import logging
import streamlit as st

from config.variaveis_globais import streamlit_secret, API_BASE_URL

app = FastAPI()

config = create_global_variables(streamlit_secret)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Document(BaseModel):
    data: dict


#################################################################################
############################         FUNCTIONS        ###########################
#################################################################################

def api_request(method, endpoint, data=None):
    """
    Realiza uma requisição à API.

    Args:
        method (str): Método HTTP (GET, POST, PUT, DELETE).
        endpoint (str): Endpoint da API.
        data (dict, optional): Dados para enviar na requisição. Padrão é None.

    Returns:
        dict: Resposta da API em formato JSON.

    Raises:
        Exception: Se ocorrer um erro durante a requisição.
    """
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API request error: {e}")
        raise Exception(f"Error: {e}")
    

def get_sections_from_api(database, collection):
    try:
        result = api_request("GET", f"/get_sections/{database}/{collection}")
        return result['sections']
    except Exception as e:
        st.error(f"Erro ao buscar seções: {str(e)}")
        return []



#################################################################################
############################           ROTAS          ###########################
#################################################################################

@app.post("/create/{collection}")
async def create(collection: str, document: Document):
    """
    Cria um novo documento na coleção especificada.

    Args:
        collection (str): Nome da coleção.
        document (Document): Dados do documento a ser criado.

    Returns:
        dict: ID do documento criado.

    Raises:
        HTTPException: Se ocorrer um erro durante a criação do documento.
    """
    try:
        result = create_document(collection, document.data)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Error creating document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/read/{collection}")
async def read(collection: str, limit: int = 10):
    """
    Lê documentos da coleção especificada.

    Args:
        collection (str): Nome da coleção.
        limit (int, optional): Número máximo de documentos a retornar. Padrão é 10.

    Returns:
        dict: Documentos lidos da coleção.

    Raises:
        HTTPException: Se ocorrer um erro durante a leitura dos documentos.
    """
    try:
        logger.info(f"Received request to read from collection: {collection}")
        documents = read_documents(collection, limit=limit)
        logger.info(f"Successfully read {len(documents)} documents")
        return {"documents": json.loads(json.dumps(documents, default=str))}
    except PyMongoError as e:
        logger.error(f"MongoDB error reading documents: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error reading documents: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    


@app.put("/update/{collection}/{id}")
async def update(collection: str, id: str, document: Document):
    """
    Atualiza um documento específico na coleção.

    Args:
        collection (str): Nome da coleção.
        id (str): ID do documento a ser atualizado.
        document (Document): Novos dados do documento.

    Returns:
        dict: Status da atualização.

    Raises:
        HTTPException: Se o documento não for encontrado ou ocorrer um erro durante a atualização.
    """
    try:
        result = update_document(collection, {"_id": ObjectId(id)}, document.data)
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"status": "updated"}
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/{collection}/{id}")
async def delete(collection: str, id: str):
    """
    Exclui um documento específico da coleção.

    Args:
        collection (str): Nome da coleção.
        id (str): ID do documento a ser excluído.

    Returns:
        dict: Status da exclusão.

    Raises:
        HTTPException: Se o documento não for encontrado ou ocorrer um erro durante a exclusão.
    """
    try:
        result = delete_document(collection, {"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"status": "deleted"}
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/main_collection")
async def get_main_collection():
    """
    Recupera todos os documentos da coleção principal.

    Returns:
        dict: Documentos da coleção principal.

    Raises:
        HTTPException: Se ocorrer um erro ao recuperar os documentos.
    """
    try:
        main_collection = config['collections_main']
        documents = read_documents(main_collection)
        return {"documents": json.loads(json.dumps(documents, default=str))}
    except Exception as e:
        logger.error(f"Error getting main collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))
   
@app.get("/user_data")
async def read_user_data():
    """
    Recupera os dados do usuário.

    Returns:
        dict: Dados do usuário.
    """
    try:
        user_data = get_user_data()
        return {"user_data": json.loads(json.dumps(user_data, default=str))}
    except Exception as e:
        logger.error(f"Error getting user data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/get_sections/{database}/{collection}")
async def get_sections(database: str, collection: str):
    try:
        logger.info(f"Fetching sections from database: {database}, collection: {collection}")
        db = get_database(database)
        coll = db[collection]
        sections = list(coll.find({}, {"section": 1, "questions": 1}))
        return {"sections": json.loads(json.dumps(sections, default=str))}
    except Exception as e:
        logger.error(f"Error fetching sections: {e}")
        raise HTTPException(status_code=500, detail=str(e))