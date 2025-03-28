# main.py
import subprocess
from Scripts.config_log import logger  ## Importa el logger configurado

def run_script(script_name):
    try:
        # Ejecuta el script y espera a que termine
        subprocess.run(['python', script_name], check=True)
        logger.info(f'{script_name} ejecutado correctamente.')
    except subprocess.CalledProcessError as e:
        logger.error(f'Error al ejecutar {script_name}: {e}')
        raise  # Vuelve a lanzar la excepción para detener la ejecución si hay un error

def main():
    scripts = [
        'main_dispatcher.py',
        'main_performer.py',
        'main_reporter.py'
    ]

    for script in scripts:
        run_script(script)

if __name__ == '__main__':
    main()
