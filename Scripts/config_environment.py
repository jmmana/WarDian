import logging
from dotenv import load_dotenv, find_dotenv
import os

def load_environment():
    # Configurar el logger
    logger = logging.getLogger(__name__)

    # Verificar si existe el archivo .env.local
    local_env_file = '.env.local'
    if os.path.exists(local_env_file):
        load_dotenv(local_env_file)
        logger.info("Loaded .env.local")
    else:
        # Cargar las variables de entorno desde el archivo .env
        env_file = '.env'
        load_dotenv(env_file)
        logger.info("Loaded .env")

    # Crear un diccionario con las variables de entorno
    env_vars = {
        'LOGIN_URL': os.getenv('LOGIN_URL'),
        'WORK_ITEMS_URL': os.getenv('WORK_ITEMS_URL'),
        'PROCESS_BASE_URL': os.getenv('PROCESS_BASE_URL'),
        'BROWSER_NAME': os.getenv('BROWSER_NAME'),
        'WEB_USERNAME': os.getenv('WEB_USERNAME'),
        'WEB_PASSWORD': os.getenv('WEB_PASSWORD'),
        'TO_EMAILS': os.getenv('TO_EMAILS').split(','),
        'SMTP_SERVER': os.getenv('SMTP_SERVER'),
        'SMTP_PORT': int(os.getenv('SMTP_PORT')),
        'SMTP_USER': os.getenv('SMTP_USER'),
        'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD'),
        'DB_FILE': os.getenv('DB_FILE'),
        'TABLE_NAME': os.getenv('TABLE_NAME')
    }

    return env_vars
