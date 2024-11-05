import os
from datetime import datetime
from rich import print
from rich.panel import Panel
from rich.style import Style
import logging
from pydantic import BaseModel
from pydantic import ValidationError, field_validator

# Classe para validar - titulo
class TituloSettings(BaseModel):
    
    # Titulo
    project_name: str
    project_version: str
    project_dev_name: str
    project_dev_mail: str
    # Validador para garantir que nenhum campo seja uma string vazia

    @field_validator('project_name', 'project_version', 'project_dev_name', 'project_dev_mail')
    def check_non_empty_string(cls, value, info):
        if not isinstance(value, str) or not value.strip():
            
            raise ValueError(f"O parâmetro '{info.field_name}' deve ser uma string não vazia.")
        
        return value


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

def titulo(project_name:str,project_version:str,project_dev_name:str,project_dev_mail:str):

    try:
        settings = TituloSettings(project_name=project_name,project_version=project_version,project_dev_name=project_dev_name,project_dev_mail=project_dev_mail)
        #return settings

    except ValidationError as e:
        # Extrair os detalhes da exceção
        errors = e.errors()
        missing_vars = [error['loc'][0] for error in errors if error['type'] == 'missing']
        
        # Criar uma mensagem personalizada
        if missing_vars:
            missing_vars_str = ', '.join(missing_vars)
            raise ValueError(
                f"As seguintes variáveis obrigatórias estão ausentes no arquivo .env ou nas variáveis de ambiente da máquina, impossibi: {missing_vars_str}"
            )


    if os.getenv('ambiente_de_execucao') is None or os.getenv('ambiente_de_execucao') != "karavela":

        estilo_box = Style(bold=True)
        print(
            Panel(
                f"""
                    [bold chartreuse3]CIA [bold white]| [bold chartreuse3]Centro de Inteligência e Automação [bold white]([bold chartreuse3]cia@stone.com.br[bold white])[bold green]\n
                    Projeto[bold white]: [bold green]{project_name}\n
                    Versão[bold white]: [bold green]{project_version}\n
                    Dev[bold white]: [bold green]{project_dev_name} [bold white]([bold green]{project_dev_mail}[bold white])[bold green]\n
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
        logging.info(f"Projeto: {project_name}")
        logging.info(f"\tVersão: {project_version} (Última modificação: {last_modified()})")
        logging.info("\tTime: CIA <cia@stone.com.br>")
        logging.info(f"\tDesenvolvedor: {project_dev_name} <{project_dev_mail}>")
        logging.info("-")

