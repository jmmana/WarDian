import logging
import os
import sys
import pandas as pd

from Scripts.config_environment import load_environment  # Importar la función de configuración del entorno
from Scripts.open_browser import open_browser
from Scripts.close_browser import close_browser
from Scripts.login_browser import login
from Scripts.datascraping_browser import scrape_work_items
from Scripts.processdata_browser import save_to_csv
from Scripts.processdata_browser import save_to_sqlite
from Scripts.config_log import logger

# Cargar las variables de entorno
env_vars = load_environment()

# Acceder a las variables de entorno desde el diccionario
db_file = env_vars['DB_FILE']
table_name = env_vars['TABLE_NAME']
login_url = env_vars['LOGIN_URL']
work_items_url = env_vars['WORK_ITEMS_URL']
process_base_url = env_vars['PROCESS_BASE_URL']
browser_name = env_vars['BROWSER_NAME']
username = env_vars['WEB_USERNAME']
password = env_vars['WEB_PASSWORD']




def main():
    """
    Función principal que inicia el script de automatización.
    """
    try:
        logger.info("Starting the automation script")
        
        driver = open_browser(login_url, browser_name)

        # Llamar a la función de login
        login(driver, username, password)

        # Llamar a la función de scraping
        df = scrape_work_items(driver, work_items_url)

        # Guardar los datos en un archivo CSV en el directorio Data
        output_directory = "Temp"
        save_to_csv(df, output_directory)

        # Guardar los datos en la base de datos SQLite
        save_to_sqlite(df, db_file, table_name)
        
        # Cerrar el navegador
        close_browser(driver)

        logger.info("Automation script completed successfully")
    except Exception as e:
        logger.error("An error occurred in the main script", exc_info=True)

if __name__ == "__main__":
    main()
