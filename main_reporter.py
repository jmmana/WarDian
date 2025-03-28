import logging
import os
import sys
import pandas as pd
import sqlite3
from datetime import datetime
from Scripts.processdata_browser import update_execution_status  # Importar la función
from Scripts.send_email import send_email  # Importar la función
from Scripts.config_environment import load_environment  # Importar la función de configuración del entorno
from Scripts.config_log import logger

# Cargar las variables de entorno
env_vars = load_environment()

# Acceder a las variables de entorno desde el diccionario
db_file = env_vars['DB_FILE']
table_name = env_vars['TABLE_NAME']
to_emails = env_vars['TO_EMAILS']
smtp_server = env_vars['SMTP_SERVER']
smtp_port = env_vars['SMTP_PORT']
smtp_user = env_vars['SMTP_USER']
smtp_password = env_vars['SMTP_PASSWORD']

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
        query = f"SELECT * FROM {table_name} WHERE ExecutionStatus NOT LIKE '% - Reported'"
        df = pd.read_sql_query(query, conn)
        conn.close()
        logger.debug(f"Datos leídos de la base de datos: {len(df)} filas")
        return df
    except Exception as e:
        logger.error(f"Failed to read data from SQLite database {db_file}", exc_info=True)
        sys.exit(1)

def main():
    """
    Función principal que inicia el script de automatización para el robot Reporter.
    """
    try:
        logger.info("Starting the Reporter automation script")
        
        # Leer los datos de la base de datos SQLite
        df = read_from_sqlite(db_file, table_name)

        # Crear un archivo CSV con los datos leídos
        output_directory = "Temp"
        os.makedirs(output_directory, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"Report_{timestamp}.csv"
        csv_filepath = os.path.join(output_directory, csv_filename)
        df.to_csv(csv_filepath, index=False)
        logger.info(f"CSV creado en {csv_filepath}")

        # Enviar el archivo CSV por correo
        subject = "Reporte de Ejecución"
        body = "Adjunto encontrará el reporte de ejecución."

        if send_email(subject, body, to_emails, csv_filepath, smtp_server, smtp_port, smtp_user, smtp_password):
            # Actualizar el estado de ejecución de los registros a "Reported"
            for wiid in df['WIID']:
                update_execution_status(db_file, table_name, wiid, f"{df.loc[df['WIID'] == wiid, 'ExecutionStatus'].values[0]} - Reported")

        logger.info("Reporter automation script completed successfully")
    except Exception as e:
        logger.error("An error occurred in the Reporter automation script", exc_info=True)

if __name__ == "__main__":
    main()
