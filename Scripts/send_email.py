import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import os

logger = logging.getLogger(__name__)

def send_email(subject, body, to_emails, attachment_path, smtp_server, smtp_port, smtp_user, smtp_password):
    """
    Envía un correo electrónico con un archivo adjunto.

    Args:
        subject (str): El asunto del correo electrónico.
        body (str): El cuerpo del correo electrónico.
        to_emails (list): Una lista de direcciones de correo electrónico de los destinatarios.
        attachment_path (str): La ruta al archivo adjunto.
        smtp_server (str): El servidor SMTP.
        smtp_port (int): El puerto SMTP.
        smtp_user (str): El usuario SMTP.
        smtp_password (str): La contraseña SMTP.
    """
    try:
        logger.debug(f"Enviando correo electrónico a {to_emails} con el archivo adjunto {attachment_path}")

        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject

        # Adjuntar el cuerpo del mensaje
        msg.attach(MIMEText(body, 'plain'))

        # Adjuntar el archivo
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
        msg.attach(part)

        # Enviar el correo
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, to_emails, text)
        server.quit()

        logger.info(f"Correo electrónico enviado a {to_emails} con el archivo adjunto {attachment_path} exitosamente")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_emails} with the attachment {attachment_path}", exc_info=True)
        return False
