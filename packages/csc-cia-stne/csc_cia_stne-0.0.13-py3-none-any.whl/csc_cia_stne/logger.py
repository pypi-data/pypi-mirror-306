import os
import logging
import colorlog
from pythonjsonlogger import jsonlogger


# Strategy para formatação dos logs
class LogFormatterStrategy:
    """
    Interface para estratégia de formatação de logs.
    Define o método `format`, que deve ser implementado pelas subclasses.
    """

    def format(self, log_handler, date_format):
        """
        Aplica a formatação do log ao handler fornecido.

        Parâmetros:
            log_handler (logging.Handler): O handler que receberá a formatação.
            date_format (str): O formato da data para os logs.

        Retorna:
            None
        """
        raise NotImplementedError("O método format() deve ser implementado")


class ColorLogFormatter(LogFormatterStrategy):
    """
    Implementação da estratégia de formatação de logs coloridos para uso local.
    """

    def format(self, log_handler, date_format):
        """
        Aplica a formatação colorida ao handler de log.

        Parâmetros:
            log_handler (logging.Handler): O handler que receberá a formatação.
            date_format (str): O formato da data para os logs.

        Retorna:
            None
        """
        formatter = colorlog.ColoredFormatter(
            "%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
            datefmt=date_format,
            log_colors={
                "DEBUG": "reset",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        log_handler.setFormatter(formatter)


class JsonLogFormatter(LogFormatterStrategy):
    """
    Implementação da estratégia de formatação de logs em JSON, ideal para ambientes como Docker.
    """

    def format(self, log_handler, date_format):
        """
        Aplica a formatação JSON ao handler de log.

        Parâmetros:
            log_handler (logging.Handler): O handler que receberá a formatação.
            date_format (str): O formato da data para os logs.

        Retorna:
            None
        """
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt=date_format
        )
        log_handler.setFormatter(formatter)


# Factory para criar o logger
class LoggerFactory:
    """
    Classe de fábrica responsável por criar e configurar loggers.
    """

    @staticmethod
    def create_logger(name):
        """
        Cria e retorna um logger configurado com o nome especificado.

        Parâmetros:
            name (str): O nome do logger.

        Retorna:
            logging.Logger: O logger configurado.
        """
        try:
            if not os.path.exists("./tmp"):
                os.makedirs("./tmp")
        except OSError as e:
            print(f"Erro ao criar o diretório './tmp': {e}")
            raise

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        log_handler = logging.StreamHandler()
        date_format = "%d-%m-%Y %H:%M:%S"

        # Define a estratégia de formatação dependendo do ambiente
        if LoggerFactory.not_docker():
            formatter_strategy = ColorLogFormatter()

            # Configura o handler para salvar logs em arquivo
            file_handler = logging.FileHandler("tmp/log.txt")
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt=date_format,
                )
            )
            logger.addHandler(file_handler)
        else:
            formatter_strategy = JsonLogFormatter()
            print("Rodando em container, logs em JSON")

        # Aplica a estratégia de formatação
        formatter_strategy.format(log_handler, date_format)
        logger.addHandler(log_handler)

        return logger

    @staticmethod
    def not_docker():
        """
        Verifica se o código está sendo executado em um container Docker.

        Retorna:
            bool: False se estiver rodando em um container Docker, True se estiver rodando localmente.
        """
        if os.path.exists("/.dockerenv"):
            return False

        try:
            with open("/proc/1/cgroup", "rt") as file:
                for line in file:
                    if "docker" in line or "kubepods" in line:
                        return False
        except Exception:
            print("Logger sendo executado localmente.")

        return True


# Uso do logger
logger = LoggerFactory.create_logger(__name__)