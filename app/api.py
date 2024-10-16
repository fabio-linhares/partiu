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

from fastapi import FastAPI, Form, HTTPException
from pymongo import MongoClient

from pydantic import BaseModel
from utils.database import (create_document,
                            read_documents, 
                            update_document, 
                            delete_document, 
                            get_user_data,
                            get_connection_string)
from utils.globals import create_global_variables
from bson import ObjectId

import json
import requests
import logging
import random
import streamlit as st

from config.variaveis_globais import streamlit_secret, API_BASE_URL

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from utils.database import get_connection_string


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

config_vars = create_global_variables(streamlit_secret)




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Document(BaseModel):
    data: dict



#################################################################################
############################         FUNCTIONS        ###########################
#################################################################################

def api_request(method, endpoint, data=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, data=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API request error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            return {"status": "error", "detail": e.response.text}
        return {"status": "error", "detail": str(e)}
    
@st.cache_data(ttl=3600) # 1 hora
def api_request_cached(method, endpoint, data=None):
    return api_request(method, endpoint, data)
    

def get_sections_from_api(database, collection):
    try:
        result = api_request("GET", f"/get_sections/{database}/{collection}")
        if 'sections' in result:
            return result['sections']
        else:
            st.error(f"Resposta inesperada da API: {result}")
            return []
    except Exception as e:
        st.error(f"Erro ao buscar seções: {str(e)}")
        if hasattr(e, 'response'):
            st.error(f"Detalhes do erro: {e.response.text}")
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
        main_collection = config_vars['collections_main']
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
        connection_string = get_connection_string()
        logger.info(f"Connection string (without password): {connection_string.replace(config_vars['database_access_password'], '****')}")
        client = MongoClient(connection_string)
        db = client[database]
        coll = db[collection]
        logger.info(f"Connected to database and collection")
        sections = list(coll.find({}, {"section": 1, "questions": 1, "_id": 0}))
        logger.info(f"Found {len(sections)} sections")
        return {"sections": json.loads(json.dumps(sections, default=str))}
    except PyMongoError as e:
        logger.error(f"MongoDB error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if 'client' in locals():
            client.close()


@app.get("/random_title/{database}/{collection}")
async def get_random_title(database: str, collection: str):
    try:
        logger.info(f"Fetching random title from database: {database}, collection: {collection}")
        connection_string = get_connection_string()
        logger.info(f"Connection string (without password): {connection_string.replace(config_vars['database_access_password'], '****')}")
        client = MongoClient(connection_string)
        db = client[database]
        coll = db[collection]
        logger.info(f"Connected to database and collection")
        
        total_docs = coll.count_documents({})
        logger.info(f"Total documents in collection: {total_docs}")
        
        if total_docs == 0:
            logger.warning("No titles found in the collection")
            raise HTTPException(status_code=404, detail="No titles found in the collection")
        
        random_index = random.randint(0, total_docs - 1)
        random_title = coll.find().limit(1).skip(random_index).next()
        logger.info(f"Random title selected: {random_title['titulo']}")
        
        return {"titulo": random_title['titulo']}
    except PyMongoError as e:
        logger.error(f"MongoDB error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if 'client' in locals():
            client.close()


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    logger.info(f"Config vars: {config_vars}")
    try:
        connection_string = get_connection_string()
        client = MongoClient(connection_string)
        db = client[config_vars['database_main']] 
        users_collection = db[config_vars['collections_users']] 

        print(config_vars['collections_users'])



        user = users_collection.find_one({"username": username})
        if user:
            # Como a senha está vazia, vamos apenas verificar se o usuário existe
            if user['password'] == '':
                return {
                    "status": "success",
                    "user": {
                        "username": user['username'],
                        "email": user['email'],
                        "roles": user['roles'],
                        "profile": user['profile']
                    }
                }
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
        else:
            raise HTTPException(status_code=401, detail="User not found")
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'client' in locals():
            client.close()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)