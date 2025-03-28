from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

def process_items(driver, base_url, work_items):
    """
    Procesa cada elemento de trabajo abriendo una nueva pestaña y navegando a la URL específica del elemento.

    Args:
        driver (WebDriver): El controlador del navegador.
        base_url (str): La URL base para procesar los elementos de trabajo.
        work_items (list): Una lista de diccionarios con los datos de los elementos de trabajo.
    """
    try:
        logger.info("Starting to process work items")

        for item in work_items:
            if item["Type"] == "WI5":
                wiid = item["WIID"]
                item_url = f"{base_url}/{wiid}"
                logger.info(f"Processing work item: {wiid}")

                # Abrir una nueva pestaña
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])

                # Navegar a la URL del elemento de trabajo
                driver.get(item_url)

                # Esperar hasta que el campo de comentario esté presente
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "newComment"))
                )

                # Llenar el campo de comentario
                comment_field = driver.find_element(By.ID, "newComment")
                comment_field.send_keys("Datos Procesados por Automatizacion con Python")

                # Seleccionar la opción "Closed" del combobox
                dropdown_button = driver.find_element(By.XPATH, "//button[@data-id='newStatus']")
                dropdown_button.click()
                closed_option = driver.find_element(By.XPATH, "//span[text()='Completed']")
                closed_option.click()

                # Hacer clic en el botón "Update Work Item"
                update_button = driver.find_element(By.ID, "buttonUpdate")
                update_button.click()

                # Cerrar la pestaña
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        logger.info("Processing of work items completed successfully")
    except Exception as e:
        logger.error("Failed to process work items", exc_info=True)

if __name__ == "__main__":
    import sys
    from selenium import webdriver
    import pandas as pd

    if len(sys.argv) != 3:
        logger.error("Usage: python process_items.py <base_url> <input_file>")
        sys.exit(1)

    base_url = sys.argv[1]
    input_file = sys.argv[2]

    df = pd.read_csv(input_file)
    work_items = df.to_dict(orient="records")

    driver = webdriver.Chrome()
    driver.maximize_window()

    process_items(driver, base_url, work_items)

    driver.quit()
