import requests
import time
from tqdm import tqdm
from dotenv import load_dotenv
import os

# Cargar variables desde el archivo .env
load_dotenv()

# URL del producto desde el archivo .env
URL = os.getenv("URL")

# Configuración de Telegram desde el archivo .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_telegram(mensaje):
    """Envía un mensaje a Telegram y espera hasta que se confirme el envío."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": mensaje}  # Usamos params para enviar el mensaje
    try:
        response = requests.post(url, data=params)  # Usamos POST con data
        response.raise_for_status()  # Lanza una excepción si el código de estado no es 200
        print("📩 Mensaje enviado a Telegram")
        return True  # Confirmamos que el mensaje se envió correctamente
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al enviar mensaje a Telegram: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Respuesta del servidor: {e.response.text}")
        return False  # Indicamos que hubo un error

def verificar_disponibilidad():
    """Verifica si el producto está disponible y espera a que se envíe el mensaje a Telegram."""
    try:
        response = requests.get(URL)
        print(f"Respuesta del servidor: {response.status_code}")
        if response.status_code == 404:
            print("❌ Producto NO disponible")
        elif response.status_code == 200:
            print("✅ Producto DISPONIBLE")
            mensaje_enviado = False
            while not mensaje_enviado:
                # Intentar enviar el mensaje y esperar que se envíe correctamente
                mensaje_enviado = enviar_telegram(f"🔥 ¡El producto está disponible! Compra aquí: {URL}")
                if not mensaje_enviado:
                    print("⚠️ El mensaje no se envió correctamente, reintentando...")
            print("✅ Notificación enviada correctamente")
        else:
            print(f"⚠️ Estado inesperado: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error al verificar disponibilidad: {e}")

# Bucle infinito con cuenta regresiva de 2 minutos
while True:
    try:
        verificar_disponibilidad()
        print("🔄 Verificando nuevamente en 2 minutos...\n")

        # Barra de progreso para la cuenta regresiva
        for _ in tqdm(range(120), desc="⏳ Esperando", unit="s"):  # 120 segundos = 2 minutos
            time.sleep(1)  # Espera 1 segundo antes de continuar con la siguiente verificación
    except Exception as e:
        print(f"⚠️ Error en el bucle principal: {e}")
