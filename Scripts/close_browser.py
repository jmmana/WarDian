import logging

logger = logging.getLogger(__name__)

def close_browser(driver):
    """
    Cierra el navegador especificado.

    Args:
        driver (WebDriver): El controlador del navegador a cerrar.
    """
    try:
        logger.info("Attempting to close the browser")
        driver.quit()
        logger.info("Successfully closed the browser")
    except Exception as e:
        logger.error("Failed to close the browser", exc_info=True)

if __name__ == "__main__":
    logger.error("This script should not be run directly")
