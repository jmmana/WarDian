# Scripts/config_log.py
import logging
import os
import sys
from datetime import datetime

# Configuración del logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Logs')
os.makedirs(log_dir, exist_ok=True)

# Obtener la fecha actual y formatearla
current_date = datetime.now().strftime('%Y-%m-%d')
log_file = os.path.join(log_dir, f'automation_{current_date}.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)-45s - %(levelname)-8s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
