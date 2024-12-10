import bcrypt
from utils.database import update_document

def set_user_password(username, plain_password):
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    update_document(
        collection_name='tp_users',
        query={'username': username},
        update={'password': hashed_password.decode('utf-8')}
    )


#set_user_password('infnet', 'infnet')