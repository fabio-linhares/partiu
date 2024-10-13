from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from config.variaveis_globais import streamlit_secret
from utils.globals import create_global_variables
from utils.database import get_connection_string

config = create_global_variables(streamlit_secret)

def update_password_hash(client, username, password):
    db = client[config['database_user']]
    users_collection = db[config['collections_users']]
    hashed_password = generate_password_hash(password)
    result = users_collection.update_one({"username": username}, {"$set": {"password": hashed_password}})
    return result.modified_count > 0

if __name__ == "__main__":
    client = MongoClient(get_connection_string())

    username = input("Digite o nome de usuário: ")
    password = input("Digite a nova senha: ")

    if update_password_hash(client, username, password):
        print(f"Senha atualizada com sucesso para o usuário {username}")
    else:
        print(f"Não foi possível atualizar a senha para o usuário {username}")

    client.close()