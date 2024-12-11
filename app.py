from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido a la aplicación del temporizador. Usa /temporizador con el parámetro 'fin' para ver el temporizador."

@app.route('/temporizador')
def temporizador():
    # Obtener la fecha de fin desde los parámetros
    fecha_fin = request.args.get('fin')
    if not fecha_fin:
        return "Por favor, proporciona una fecha de fin con el parámetro 'fin'.", 400

    try:
        fecha_fin = datetime.fromisoformat(fecha_fin)
    except ValueError:
        return "Formato de fecha incorrecto. Usa 'YYYY-MM-DDTHH:MM:SS'.", 400

    # Calcular el tiempo restante
    ahora = datetime.now()
    tiempo_restante = fecha_fin - ahora
    if tiempo_restante.total_seconds() <= 0:
        texto = "¡Tiempo terminado!"
    else:
        dias = tiempo_restante.days
        horas, resto = divmod(tiempo_restante.seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        texto = f"{dias} días, {horas:02}:{minutos:02}:{segundos:02}"

    # Crear la imagen
    ancho, alto = 800, 400
    imagen = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(imagen)

    # Fuente personalizada
    try:
        fuente = ImageFont.truetype("arial.ttf", 50)  # Asegúrate de que esta fuente exista
    except IOError:
        fuente = ImageFont.load_default()

    # Calcular posición del texto para centrarlo
    bbox = draw.textbbox((0, 0), texto, font=fuente)
    texto_ancho, texto_alto = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (ancho - texto_ancho) // 2
    y = (alto - texto_alto) // 2

    # Dibujar el texto
    draw.text((x, y), texto, font=fuente, fill=(0, 0, 0))

    # Enviar la imagen como respuesta
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    # Obtén el puerto de la variable de entorno (usado por Render) o usa 5000 como predeterminado
    port = int(os.environ.get('PORT', 5000))
    # Ejecuta la aplicación en 0.0.0.0 para que sea accesible externamente
    app.run(host='0.0.0.0', port=port)
