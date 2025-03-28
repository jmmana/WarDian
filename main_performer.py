import logging
import os
import sys
import pandas as pd
import sqlite3
from datetime import datetime
from selenium import webdriver
from Scripts.open_browser import open_browser
from Scripts.close_browser import close_browser
from Scripts.login_browser import login
from Scripts.process_items import process_items
from Scripts.update_status import update_execution_status  # Importar la función
from Scripts.config_environment import load_environment  # Importar la función de configuración del entorno
from Scripts.config_log import logger

# Cargar las variables de entorno
env_vars = load_environment()

# Acceder a las variables de entorno desde el diccionario
login_url = env_vars['LOGIN_URL']
process_base_url = env_vars['PROCESS_BASE_URL']
browser_name = env_vars['BROWSER_NAME']
username = env_vars['WEB_USERNAME']
password = env_vars['WEB_PASSWORD']


def read_from_sqlite(db_file, table_name):
    """
    Lee los datos de una tabla en una base de datos SQLite y los devuelve como un DataFrame.

    Args:
        db_file (str): El archivo de la base de datos SQLite.
        table_name (str): El nombre de la tabla a leer.

    Returns:
        DataFrame: Los datos leídos de la tabla.
    """
    try:
        logger.debug(f"Conectando a la base de datos SQLite. Archivo: {db_file}, Tabla: {table_name}")
        conn = sqlite3.connect(db_file)
        query = f"SELECT * FROM {table_name} WHERE ExecutionStatus = 'Ready For Performer'"
        df = pd.read_sql_query(query, conn)
        conn.close()
        logger.debug(f"Datos leídos de la base de datos: {len(df)} filas")
        return df
    except Exception as e:
        logger.error(f"Failed to read data from SQLite database {db_file}", exc_info=True)
        sys.exit(1)

def main():
    """
    Función principal que inicia el script de automatización para el robot Performer.
    """
    try:
        logger.info("Starting the Performer automation script")
        
        driver = open_browser(login_url, browser_name)

        # Llamar a la función de login
        login(driver, username, password)

        # Leer los datos de la base de datos SQLite
        db_file = "Data/PythonAutomation.db"  # Especifica la ruta al archivo de la base de datos
        table_name = "ACME_Systems"  # Nombre de la tabla
        df = read_from_sqlite(db_file, table_name)

        # Procesar cada elemento de trabajo
        work_items = df.to_dict(orient="records")
        for item in work_items:
            try:
                process_items(driver, process_base_url, [item])
                update_execution_status(db_file, table_name, item['WIID'], 'Successful')
            except Exception as e:
                logger.error(f"Failed to process item WIID {item['WIID']}", exc_info=True)
                update_execution_status(db_file, table_name, item['WIID'], 'Failed')

        # Cerrar el navegador
        close_browser(driver)

        logger.info("Performer automation script completed successfully")
    except Exception as e:
        logger.error("An error occurred in the Performer automation script", exc_info=True)

if __name__ == "__main__":
    main()
