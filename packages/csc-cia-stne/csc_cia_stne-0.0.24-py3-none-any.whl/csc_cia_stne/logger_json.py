import logging
from pythonjsonlogger import jsonlogger

def setup_json_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

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

    # Capturando logs da biblioteca FastAPI/Uvicorn
    #uvicorn_logger = logging.getLogger("uvicorn")
    #uvicorn_logger.handlers = logger.handlers
    #uvicorn_logger.setLevel(logging.INFO)

    #uvicorn_error_logger = logging.getLogger("uvicorn.error")
    #uvicorn_error_logger.handlers = logger.handlers
    #uvicorn_error_logger.setLevel(logging.INFO)

    #uvicorn_access_logger = logging.getLogger("uvicorn.access")
    #uvicorn_access_logger.handlers = logger.handlers
    #uvicorn_access_logger.setLevel(logging.INFO)

    return logger

# Chama a função para configurar o logger
logger = setup_json_logger()