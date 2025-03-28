from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

def login(driver, username, password):
    """
    Realiza el proceso de login en la página web.

    Args:
        driver (WebDriver): El controlador del navegador.
        username (str): El nombre de usuario para el login.
        password (str): La contraseña para el login.
    """
    try:
        logger.info("Attempting to log in")

        # Localizar los elementos de la página de login
        email_field = driver.find_element(By.CSS_SELECTOR, "#email")
        password_field = driver.find_element(By.CSS_SELECTOR, "#password")
        login_button = driver.find_element(By.CSS_SELECTOR, ".btn-primary")

        # Ingresar el nombre de usuario y la contraseña
        email_field.send_keys(username)
        password_field.send_keys(password)

        # Hacer clic en el botón de login
        login_button.click()

        logger.info("Login button clicked, waiting for login to complete")

        # Esperar hasta que el elemento de logout sea visible o hasta que pasen 10 segundos
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='bs-example-navbar-collapse-1']/ul/li[3]/a"))
        )

        logger.info("Login successful")
    except Exception as e:
        logger.error("Failed to log in", exc_info=True)
        raise
