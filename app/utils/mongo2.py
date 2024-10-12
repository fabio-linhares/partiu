
import toml

def load_database_config(file_path):
    config = toml.load(file_path)
    db_access = config['database_access']
    uri = f"{db_access['protocol']}://{db_access['user']}:{db_access['password']}@{db_access['host']}:{db_access['port']}/{db_access['database']}"
    return uri

