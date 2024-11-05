from pydantic_settings import BaseSettings
from pydantic import ValidationError
from rich.traceback import install
from dotenv import load_dotenv
from .functions import titulo
# Instala formatações de exception da biblioteca Rich
install()

# Carrega .env
load_dotenv()

# Classe para armazenar configurações
class Settings(BaseSettings):
    # Ambiente de Execução
    ambiente_de_execucao: str = "local"
    log_level: str = "DEBUG"
    
    # Titulo
    project_name: str
    project_version: str
    project_dev_name: str
    project_dev_mail: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'  # Defina a codificação se necessário

# Carrega as configurações do arquivo .env ou retorna exception com os campos obrigatórios que não foram preenchidos
def load_settings():
    try:
        settings = Settings()
        return settings

    except ValidationError as e:
        # Extrair os detalhes da exceção
        errors = e.errors()
        missing_vars = [error['loc'][0] for error in errors if error['type'] == 'missing']
        
        # Criar uma mensagem personalizada
        if missing_vars:
            missing_vars_str = ', '.join(missing_vars)
            raise ValueError(
                f"As seguintes variáveis obrigatórias estão ausentes no arquivo .env ou nas variáveis de ambiente da máquina: {missing_vars_str}\n"
                "Outras variáveis, não obrigatórias: 'ambiente_de_execução' ('local' ou 'karavela') e 'log_level' ('DEBUG', 'INFO', etc)"
            )
        else:
            titulo()
            
settings = load_settings()
