import os
import base64
import mimetypes
from datetime import datetime
from rich import print
from rich.panel import Panel
from rich.style import Style
import json
import shutil
import logging

# Retorna data de modificação
def last_modified()->datetime:
    """
    Retorna a data da última atualização do script

    """
    current_file = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_file)
    base_dir = os.path.dirname(os.path.dirname(current_file))

    newest_date = None

    for root, _, files in os.walk(base_dir):
        
        for file in files:
        
            if file.endswith('.py'):
        
                file_path = os.path.join(root, file)
                file_modification_date = os.path.getmtime(file_path)
                
                if newest_date is None or file_modification_date > newest_date:
        
                    newest_date = file_modification_date

    # Converter o timestamp para um objeto datetime
    last_modified_date = datetime.fromtimestamp(newest_date)
    last_modified_date = last_modified_date.strftime("%Y%m%d")
    
    return last_modified_date

def titulo():
    
    if os.getenv('ambiente_de_execucao') is None or os.getenv('ambiente_de_execucao') != "karavela":

        estilo_box = Style(bold=True)
        print(
            Panel(
                f"""
                    [bold chartreuse3]CIA [bold white]| [bold chartreuse3]Centro de Inteligência e Automação [bold white]([bold chartreuse3]cia@stone.com.br[bold white])[bold green]\n
                    Projeto[bold white]: [bold green]{os.getenv('project_name')}\n
                    Versão[bold white]: [bold green]{os.getenv('project_version')}\n
                    Dev[bold white]: [bold green]{os.getenv('project_dev_name')} [bold white]([bold green]{os.getenv('project_dev_mail')}[bold white])[bold green]\n
                    Última atualização[bold white]: [bold green]{last_modified()}
                """, 
                title="Stone", 
                subtitle="CSC-CIA", 
                style=estilo_box, 
                border_style="bold chartreuse3"
            )   
        )

    else:

        logging.info("CSC | CIA - Centro de Inteligência e Automação")
        logging.info(f"Projeto: {os.getenv('project_name')}")
        logging.info(f"\tVersão: {os.getenv('project_version')} (Última modificação: {last_modified()})")
        logging.info("\tTime: CIA <cia@stone.com.br>")
        logging.info(f"\tDesenvolvedor: {os.getenv('project_dev_name')} <{os.getenv('project_dev_mail')}>")
        logging.info("-")

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

