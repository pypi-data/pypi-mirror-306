import os
import shutil

def recriar_pasta(caminho_pasta):

    try:

        # Se a pasta já existir, remove-a
        if os.path.exists(caminho_pasta) and os.path.isdir(caminho_pasta):
            shutil.rmtree(caminho_pasta)  # Deleta a pasta e todo o conteúdo

        # Cria a pasta novamente
        os.makedirs(caminho_pasta)
        return True, None

    except Exception as e:

        return False, e

