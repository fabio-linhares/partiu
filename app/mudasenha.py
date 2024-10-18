import bcrypt
from utils.database import update_document

def set_user_password(username, plain_password):
    # Hash a senha
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    # Atualizar o documento do usuário no banco de dados
    update_document(
        collection_name='tp_users',
        query={'username': username},
        update={'password': hashed_password.decode('utf-8')}
    )

# Exemplo de uso
set_user_password('infnet', 'infnet')