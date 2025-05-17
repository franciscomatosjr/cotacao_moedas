import logging
import os
from functools import wraps

COLORS = {
    "DEBUG": "\033[94m",  # Azul Claro
    "INFO": "\033[92m",  # Verde
    "WARNING": "\033[93m",  # Amarelo
    "ERROR": "\033[91m",  # Vermelho
    "CRITICAL": "\033[95m",  # Magenta
    "RESET": "\033[0m",
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        """

        Colore o texto do log
        :param record:
        :return:
        """
        color = COLORS.get(record.levelname, COLORS["RESET"])
        record.msg = f"{color}{record.msg}{COLORS['RESET']}"
        return super().format(record)


# Configure o logger
logger = logging.getLogger()

# Remova os handlers existentes para evitar logs duplicados
for handler in logger.handlers:
    logger.removeHandler(handler)

log_name = os.getenv("PROJECT_NAME", "default_logger_name")
logger.setLevel(logging.INFO)  # Nível padrão

# Verifica e define o nível de logging a partir da variável de ambiente
env_level = os.getenv("LOGGER_LEVEL", "INFO").upper()
if env_level in ["DEBUG", "WARNING", "INFO", "ERROR", "CRITICAL"]:
    logger.setLevel(getattr(logging, env_level))
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, env_level))
else:
    print(f"Nível de logger desconhecido: {env_level}. Usando INFO como padrão.")

# logging_format = r"%(asctime)s - %(levelname)-7s %(threadName)-12s [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"
logging_format = r"%(asctime)s - [%(levelname)-7s] [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"
formatter = ColoredFormatter(logging_format)
ch.setFormatter(formatter)
logger.addHandler(ch)


# Decorator para logar a execução de funções
def log_and_call(logger=logger) -> None:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            logger.info(f"Início da execução: {func.__module__}.{func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Término da execução: {func.__module__}.{func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Erro durante a execução de {func.__module__}.{func.__name__}: {e}", exc_info=True)

        return wrapper

    return decorator
