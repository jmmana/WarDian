from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def scrape_work_items(driver, url):
    """
    Realiza el scraping de los elementos de trabajo en la página web, incluyendo la paginación.

    Args:
        driver (WebDriver): El controlador del navegador.
        url (str): La URL de la página de trabajo.

    Returns:
        DataFrame: Un DataFrame de pandas con los datos de los elementos de trabajo.
    """
    try:
        logger.info(f"Navigating to URL: {url}")
        driver.get(url)
        
        logger.info("Starting to scrape work items")

        all_data = []

        while True:
            # Esperar hasta que la tabla de resultados esté presente
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".table"))
            )
            table = driver.find_element(By.CSS_SELECTOR, ".table")

            # Extraer las filas de la tabla
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Omitir la fila de encabezado

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                work_item = {
                    "Actions": columns[0].text,
                    "WIID": columns[1].text,
                    "Description": columns[2].text,
                    "Type": columns[3].text,
                    "Status": columns[4].text,
                    "Date": columns[5].text
                }
                all_data.append(work_item)

            # Intentar encontrar el botón de "Next" para la paginación
            try:
                next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next »']")
                next_button.click()
                WebDriverWait(driver, 10).until(EC.staleness_of(table))  # Esperar a que la tabla se actualice
            except Exception as e:
                logger.info("No more pages to scrape")
                break

        df = pd.DataFrame(all_data)
        logger.info("Scraping completed successfully")
        return df
    except Exception as e:
        logger.error("Failed to scrape work items", exc_info=True)
        return pd.DataFrame()

if __name__ == "__main__":
    import sys
    from selenium import webdriver

    if len(sys.argv) != 2:
        logger.error("Usage: python datascraping_browser.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    browser_name = "chrome"  # Cambia a "firefox" u otros nombres de navegadores si es necesario

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    df = scrape_work_items(driver, url)
    print(df)

    driver.quit()
