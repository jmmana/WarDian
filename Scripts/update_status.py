import logging
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)

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
