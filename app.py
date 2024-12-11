from flask import Flask, request, send_file
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/temporizador')
def temporizador():
    # Obtiene la fecha y hora de fin del temporizador desde la URL
    fecha_fin = request.args.get('fin')  # Ejemplo: "2023-12-31T23:59:59"
    if not fecha_fin:
        return "Por favor, proporciona una fecha de fin con el parámetro 'fin'.", 400

    try:
        fecha_fin = datetime.fromisoformat(fecha_fin)
    except ValueError:
        return "Formato de fecha no válido. Usa ISO 8601 (ej. 2023-12-31T23:59:59).", 400

    # Calcula el tiempo restante
    ahora = datetime.utcnow()
    tiempo_restante = fecha_fin - ahora

    if tiempo_restante.total_seconds() <= 0:
        mensaje = "¡Tiempo terminado!"
    else:
        dias = tiempo_restante.days
        horas, resto = divmod(tiempo_restante.seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        mensaje = f"{dias}d {horas}h {minutos}m {segundos}s"

    # Crea una imagen con Pillow
    ancho, alto = 400, 200
    imagen = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(imagen)

    # Añade el texto del temporizador
    fuente = ImageFont.load_default()
    draw.text((10, 90), mensaje, font=fuente, fill=(0, 0, 0))

    # Convierte la imagen a un archivo en memoria
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
