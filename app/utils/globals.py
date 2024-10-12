import toml

def create_global_variables(file_path):
    """
    Carrega um arquivo TOML e cria variáveis globais a partir dele.
    
    Args:
    file_path (str): Caminho para o arquivo TOML.
    
    Returns:
    dict: Um dicionário contendo as variáveis globais criadas.
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