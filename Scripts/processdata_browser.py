import pandas as pd
import logging
import os
import sqlite3
from datetime import datetime


logger = logging.getLogger(__name__)

def save_to_csv(df, directory):
    """
    Guarda un DataFrame en un archivo CSV en el directorio especificado.

    Args:
        df (DataFrame): El DataFrame a guardar.
        directory (str): El directorio donde se guardará el archivo CSV.
    """
    try:
        logger.debug(f"Guardando DataFrame en CSV. Directorio: {directory}")
        # Crear el directorio si no existe
        os.makedirs(directory, exist_ok=True)

        # Generar el nombre del archivo con la fecha y hora actuales
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Example_{timestamp}.csv"
        filepath = os.path.join(directory, filename)

        # Guardar el DataFrame en un archivo CSV
        df.to_csv(filepath, index=False)
        logger.info(f"Data saved to {filepath} successfully")
    except Exception as e:
        logger.error(f"Failed to save data to {filepath}", exc_info=True)

def save_to_sqlite(df, db_file, table_name):
    """
    Guarda un DataFrame en una base de datos SQLite, evitando duplicados.

    Args:
        df (DataFrame): El DataFrame a guardar.
        db_file (str): El archivo de la base de datos SQLite.
        table_name (str): El nombre de la tabla donde se guardarán los datos.
    """
    try:
        logger.debug(f"Conectando a la base de datos SQLite. Archivo: {db_file}, Tabla: {table_name}")
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Crear la tabla si no existe, incluyendo las columnas adicionales
        columns = ", ".join([f"{col} TEXT" for col in df.columns])
        additional_columns = "CreatedDate TEXT, ChangeDate TEXT, ErrorReason TEXT, ExecutionStatus TEXT"
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns}, {additional_columns})"
        logger.debug(f"Creando tabla con la consulta: {create_table_query}")
        cursor.execute(create_table_query)

        # Insertar los datos del DataFrame en la tabla, evitando duplicados
        for index, row in df.iterrows():
            wiid = row['WIID']  # Asumiendo que 'WIID' es el nombre de la columna
            cursor.execute(f"SELECT 1 FROM {table_name} WHERE WIID = ?", (wiid,))
            if cursor.fetchone() is None:
                placeholders = ", ".join(["?"] * len(row))
                insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}, CreatedDate, ChangeDate, ErrorReason, ExecutionStatus) VALUES ({placeholders}, ?, ?, ?, ?)"
                logger.debug(f"Insertando fila con la consulta: {insert_query}, Valores: {tuple(row) + (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '', 'Ready For Performer')}")
                cursor.execute(insert_query, tuple(row) + (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '', 'Ready For Performer'))
            else:
                logger.debug(f"El registro con WIID {wiid} ya existe en la tabla {table_name}")

        # Confirmar los cambios
        conn.commit()
        logger.info(f"Data saved to SQLite database {db_file} successfully")
    except Exception as e:
        logger.error(f"Failed to save data to SQLite database {db_file}", exc_info=True)
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

def update_execution_status(db_file, table_name, wiid, status):
    """
    Actualiza el estado de ejecución de un registro en la base de datos SQLite.

    Args:
        db_file (str): El archivo de la base de datos SQLite.
        table_name (str): El nombre de la tabla a actualizar.
        wiid (str): El identificador único del registro.
        status (str): El nuevo estado de ejecución.
    """
    try:
        logger.debug(f"Actualizando estado de ejecución en la base de datos SQLite. Archivo: {db_file}, Tabla: {table_name}, WIID: {wiid}, Estado: {status}")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        update_query = f"UPDATE {table_name} SET ExecutionStatus = ?, ChangeDate = ? WHERE WIID = ?"
        cursor.execute(update_query, (status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wiid))
        conn.commit()
        conn.close()
        logger.debug(f"Estado de ejecución actualizado para WIID {wiid} a {status}")
    except Exception as e:
        logger.error(f"Failed to update execution status for WIID {wiid} in SQLite database {db_file}", exc_info=True)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logger.error("Usage: python processdata_browser.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_directory = "Data"
    db_file = "Data/PythonAutomation.db"  # Especifica la ruta al archivo de la base de datos
    table_name = "ACME_Systems"  # Nombre de la tabla

    logger.debug(f"Archivo de entrada: {input_file}")
    logger.debug(f"Directorio de salida: {output_directory}")
    logger.debug(f"Archivo de base de datos: {db_file}")
    logger.debug(f"Nombre de la tabla: {table_name}")

    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(input_file)
    logger.debug(f"DataFrame cargado con {len(df)} filas y {len(df.columns)} columnas")

    # Guardar los datos en un archivo CSV
    save_to_csv(df, output_directory)

    # Guardar los datos en la base de datos SQLite
    save_to_sqlite(df, db_file, table_name)
