from flask import Blueprint, request, jsonify, render_template, current_app, url_for
from datetime import datetime
import re
import qrcode
import io
import base64
import os
from .models import DataModel, EventModel, QRModel

main = Blueprint('main', __name__)

@main.route('/')
def index():
    patente = request.args.get('patente')
    qr_code = None
    if patente:
        qr_record = QRModel.get_qr(patente)
        if qr_record:
            qr_code = qr_record['qr_code']
    return render_template('index.html', patente=patente, qr_code=qr_code)

@main.route('/registropatente', methods=['POST'])
def registro_patente():
    data = request.get_json()

    if 'patente' not in data or 'timestamp' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    patente = data['patente']
    timestamp = data['timestamp']
    ubicacion = data.get('ubicacion', 'Entrada principal')

    if not re.match(r'^[A-Za-z0-9]{6,}$', patente):
        return jsonify({'error': 'La patente debe tener al menos 6 caracteres y solo contener letras y números'}), 400

    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        return jsonify({'error': 'El timestamp debe estar en formato ISO 8601'}), 400

    registro = DataModel(patente=patente, ubicacion=ubicacion)
    registro.timestamp = timestamp
    registro.save_to_db()

    event = EventModel(patente=patente)
    event.start_event()

    qr_url = url_for('main.index', patente=patente, _external=True)
    qr = qrcode.make(qr_url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode('utf-8')

    qr_record = QRModel(patente=patente, qr_code=qr_code)
    qr_record.save_to_db()

    qr_filename = f"{patente}.png"
    qr_filepath = os.path.join(current_app.root_path, 'static', 'qr_codes', qr_filename)
    os.makedirs(os.path.dirname(qr_filepath), exist_ok=True)
    with open(qr_filepath, 'wb') as f:
        f.write(buffer.getvalue())

    return jsonify({'mensaje': 'Registro exitoso y temporizador iniciado', 'qr_code': qr_code}), 200

@main.route('/consultapatente/<patente>', methods=['GET'])
def consulta_patente(patente):
    registro = DataModel.get_data(patente)
    
    if not registro:
        return jsonify({'error': 'No se encontró el registro'}), 404

    return jsonify({
        'patente': registro['patente'],
        'timestamp': registro['timestamp'],
        'ubicacion': registro['ubicacion']
    }), 200

@main.route('/patenteinfo')
def patente_info():
    patente = request.args.get('patente')
    timestamp = request.args.get('timestamp')
    ubicacion = request.args.get('ubicacion')
    event = EventModel.get_event(patente)
    start_time = event['start_time'] if event else None
    return render_template('patenteinfo.html', patente=patente, timestamp=timestamp, ubicacion=ubicacion, start_time=start_time)

@main.route('/pagar/<patente>', methods=['POST'])
def pagar(patente):
    end_time = EventModel.stop_event(patente)
    if not end_time:
        return jsonify({'error': 'No se encontró un cronómetro activo para esta patente'}), 404

    event = EventModel.get_event(patente)
    if not event:
        return jsonify({'error': 'No se encontró un evento activo para esta patente'}), 404

    start_time = datetime.fromisoformat(event['start_time'])
    end_time = datetime.fromisoformat(end_time)
    elapsed_time = end_time - start_time
    elapsed_minutes = elapsed_time.total_seconds() / 60

    # Suponiendo que el costo es de $100 por minuto
    costo = round(elapsed_minutes * 100, 2)

    return jsonify({'costo': costo, 'end_time': end_time.isoformat()})