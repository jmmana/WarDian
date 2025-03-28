from selenium import webdriver
import logging

logger = logging.getLogger(__name__)

def open_browser(url, browser_name):
    """
    Abre una URL en un navegador específico y devuelve el controlador del navegador.

    Args:
        url (str): La URL a abrir.
        browser_name (str): El nombre del navegador (por ejemplo, 'chrome' o 'firefox').

    Returns:
        WebDriver: El controlador del navegador.
    """
    try:
        logger.info(f"Attempting to open URL: {url} in {browser_name}")
        
        # Seleccionar el navegador basado en el nombre proporcionado.
        if browser_name.lower() == 'chrome':
            driver = webdriver.Chrome()
        elif browser_name.lower() == 'firefox':
            driver = webdriver.Firefox()
        else:
            logger.error(f"Unsupported browser: {browser_name}")
            return None
  
        # Maximizar la ventana del navegador
        driver.maximize_window()
               
        # Abrir la URL en el navegador seleccionado.
        driver.get(url)
        logger.info(f"Successfully opened URL: {url} in {browser_name}")
        
        return driver
    except Exception as e:
        logger.error(f"Failed to open URL: {url} in {browser_name}", exc_info=True)
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        logger.error("Usage: python open_browser.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    browser_name = "chrome"  # Cambia a "firefox" u otros nombres de navegadores si es necesario
    open_browser(url, browser_name)
