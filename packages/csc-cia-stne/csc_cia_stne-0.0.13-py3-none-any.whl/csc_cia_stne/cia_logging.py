import logging
from rich.logging import RichHandler
from rich.theme import Theme
from rich.console import Console
import re
from pythonjsonlogger import jsonlogger
from rich.traceback import install

def logger(env:str = "local", log_level:str = "DEBUG"):
    
    def get_log_level(log_level):
        if log_level.upper().strip() == "DEBUG":

            log_config_level = logging.DEBUG

        elif log_level.upper().strip() == "INFO":

            log_config_level = logging.INFO

        elif log_level.upper().strip() == "WARNING":

            log_config_level = logging.WARNING

        elif log_level.upper().strip() == "ERROR":

            log_config_level = logging.ERROR
        
        elif log_level.upper().strip() == "CRITICAL":

            log_config_level = logging.CRITICAL

        else:

            log_config_level = logging.INFO  # ou outro nível padrão
        
        return log_config_level

    def add_log_level(level_name, level_num, method_name=None):
        """
        Adiciona um log level

        Parâmetros:
            level_name (str): Nome do level
            level_num (int): Número do level
        """
        if not method_name:
        
            method_name = level_name.lower()

        if hasattr(logging, level_name):
        
            raise AttributeError('{} already defined in logging module'.format(level_name))
        
        if hasattr(logging, method_name):
        
            raise AttributeError('{} already defined in logging module'.format(method_name))
        
        if hasattr(logging.getLoggerClass(), method_name):
        
            raise AttributeError('{} already defined in logger class'.format(method_name))

        def log_for_level(self, message, *args, **kwargs):
            
            if self.isEnabledFor(level_num):

                self._log(level_num, message, args, **kwargs)
                
        def log_to_root(message, *args, **kwargs):
            
            logging.log(level_num, message, *args, **kwargs)

        logging.addLevelName(level_num, level_name)
        setattr(logging, level_name, level_num)
        setattr(logging.getLoggerClass(), method_name, log_for_level)
        setattr(logging, method_name, log_to_root)

    add_log_level("SUCCESS",21)

    if env.upper().strip() != "KARAVELA":
        
        install()

        # Definindo o tema customizado
        custom_theme = Theme({
            # python -m rich.color - cores
            # python -m rich.default_styles - item + cor padrão
            "logging.level.debug": "bold bright_cyan",
            "logging.level.info": "bold bright_white",
            "logging.level.warning": "bold orange1",
            "logging.level.error": "bold red blink",
            "logging.level.critical": "bold white on red blink",
            "logging.level.success": "bold bright_green",
            "log.time":"bold white",
            "log.message":"bold gray70",
            "repr.str":"dark_olive_green3",
            "inspect.value.border":"blue",
        })

        console = Console(theme=custom_theme)

        class CustomRichHandler(RichHandler):
            def __init__(self, *args, rich_tracebacks=True, show_time=True, show_level=True, show_path=True, console=console, **kwargs):
                super().__init__(rich_tracebacks=rich_tracebacks, show_time=show_time, show_level=show_level, show_path=show_path, console=console, *args, **kwargs)
                self.show_time = show_time

            def format(self, record: logging.LogRecord) -> str:
                
                def remover_prefixo_log(mensagem):
                    # Expressão regular que encontra o padrão 'log_level:nivel: '
                    padrao = r'^(ERROR|WARNING|INFO|DEBUG|SUCCESS|CRITICAL):[^:]*:'
                    
                    # Substitui o padrão encontrado por uma string vazia
                    return re.sub(padrao, '', mensagem).strip()
                
                msg = f"| {record.getMessage()}"

                return(str(msg))
            
        # Configurando o logging com o CustomRichHandler
        logging.basicConfig(
            level=get_log_level(log_level),
            handlers=[CustomRichHandler()],
            datefmt="%d/%m/%Y %H:%M:%S |",
        )

        return logging.getLogger()
    
    else:

        def setup_json_logger():
            logger = logging.getLogger()
            logger.setLevel(get_log_level(log_level))

            # Remove handlers anteriores, se houver
            if logger.hasHandlers():
                logger.handlers.clear()

            log_handler = logging.StreamHandler()
            formatter = jsonlogger.JsonFormatter(
                fmt='%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d %(exc_info)s %(stack_info)s %(funcName)s %(module)s',
                json_ensure_ascii=False
            )
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)

            return logger

        # Chama a função para configurar o logger
        return setup_json_logger()