# alertas.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT

def enviar_alerta(asunto, mensaje):
    """
    Envía un correo electrónico de alerta.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = asunto

        msg.attach(MIMEText(mensaje, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        server.quit()

        print("Alerta enviada correctamente.")
    except Exception as e:
        print(f"Error al enviar alerta: {e}")
