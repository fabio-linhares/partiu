from utils.database import update_document, get_collection
import bcrypt

def login_user(username, password):
    try:
        collection = get_collection('tp_users')
        user = collection.find_one({'username': username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return {"status": "success", "user": user}
        else:
            return {"status": "error", "detail": "Credenciais inválidas"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def set_user_password(username, plain_password):

    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    update_document(
        collection_name='tp_users',
        query={'username': username},
        update={'password': hashed_password.decode('utf-8')}
    )