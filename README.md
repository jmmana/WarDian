
# Automatización de Login en ACME System 1

Esta sección describe cómo automatizamos el proceso de login en el sitio web de ACME System 1 utilizando Selenium en Python. A continuación, se muestra una imagen de la página de login y se explican los campos que llenaremos, los selectores que usaremos y cómo conseguimos estos selectores.

![image](https://github.com/user-attachments/assets/a602d63b-ffb9-4d76-a6df-c46b6e757aae)

## Campos a Llenar

1. **Email**: Campo de entrada para el correo electrónico del usuario.
2. **Password**: Campo de entrada para la contraseña del usuario.
3. **Login Button**: Botón para enviar el formulario de login.

## Selectores Utilizados

Para automatizar el proceso de login, utilizamos los siguientes selectores:

1. **Email Field**:
   - **Selector**: `#email`
   - **Descripción**: Este selector se utiliza para identificar el campo de entrada del correo electrónico.
   - **Código**:
     ```python
     email_field = driver.find_element(By.CSS_SELECTOR, "#email")
     email_field.send_keys("your_email@example.com")
     ```

2. **Password Field**:
   - **Selector**: `#password`
   - **Descripción**: Este selector se utiliza para identificar el campo de entrada de la contraseña.
   - **Código**:
     ```python
     password_field = driver.find_element(By.CSS_SELECTOR, "#password")
     password_field.send_keys("your_password")
     ```

3. **Login Button**:
   - **Selector**: `.btn-primary`
   - **Descripción**: Este selector se utiliza para identificar el botón de login.
   - **Código**:
     ```python
     login_button = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
     login_button.click()
     ```

## Cómo Conseguimos los Selectores

Para obtener los selectores de los elementos en la página de login, seguimos estos pasos:

1. **Abrir la página de login**: Navegamos a la URL de la página de login en un navegador web.
2. **Inspeccionar el elemento**: Hacemos clic derecho sobre el elemento que queremos automatizar (por ejemplo, el campo de email) y seleccionamos "Inspeccionar" en el menú contextual. Esto abrirá las herramientas de desarrollo del navegador.
3. **Copiar el selector**: En las herramientas de desarrollo, localizamos el elemento en el código HTML. Hacemos clic derecho sobre el código del elemento y seleccionamos "Copiar" > "Copiar selector" para obtener el selector CSS del elemento.
4. **Verificar el selector**: Pegamos el selector en nuestro script de automatización y verificamos que selecciona correctamente el elemento deseado.

## Ejemplo de Código Completo

A continuación se muestra un ejemplo de código completo para automatizar el login en la página de ACME System 1:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO)
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

        logger.info("Login successful")
    except Exception as e:
        logger.error("Failed to log in", exc_info=True)

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://acme-test.uipath.com/login")
    login(driver, "your_email@example.com", "your_password")
    driver.quit()


