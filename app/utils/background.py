import os
import random

def get_random_image(directory):
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not image_files:
        raise ValueError(f"Nenhuma imagem encontrada no diretório {directory}")
    return os.path.join(directory, random.choice(image_files))
