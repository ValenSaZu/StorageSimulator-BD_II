from flask import Flask, request, jsonify, render_template
from database_manager import DatabaseManager

app = Flask(__name__)

@app.route('/')
def index():
    """Renderiza la página de inicio."""
    return render_template('index.html')

@app.route('/simulador', methods=['GET'])
def simulador():
    """Inicia el simulador con los parámetros seleccionados."""
    tipo_bd = request.args.get('tipo_bd')
    tipo_disco = request.args.get('tipo_disco')
    
    if not tipo_bd or not tipo_disco:
        return jsonify({"error": "Parámetros no válidos."}), 400
    
    db_manager = DatabaseManager(tipo_disco=tipo_disco, tipo_bd=tipo_bd)

    return jsonify({"mensaje": f"Simulador iniciado con {tipo_disco} y {tipo_bd}."}), 200

@app.route('/escribir', methods=['POST'])
def escribir():
    """Escribe datos en la dirección lógica."""
    data = request.json
    direccion_logica = data.get('direccion_logica')
    datos = data.get('datos')
    
    if not direccion_logica or not datos:
        return jsonify({"error": "Faltan datos"}), 400
    
    resultado = db_manager.escribir_dato(direccion_logica, datos)
    return jsonify({"resultado": resultado}), 200

@app.route('/leer', methods=['GET'])
def leer():
    """Lee datos de la dirección lógica."""
    direccion_logica = request.args.get('direccion_logica')
    
    if not direccion_logica:
        return jsonify({"error": "Dirección lógica no proporcionada"}), 400
    
    resultado = db_manager.leer_dato(direccion_logica)
    return jsonify({"resultado": resultado}), 200

@app.route('/borrar', methods=['DELETE'])
def borrar():
    """Borra datos en la dirección lógica."""
    direccion_logica = request.json.get('direccion_logica')
    
    if not direccion_logica:
        return jsonify({"error": "Dirección lógica no proporcionada"}), 400
    
    resultado = db_manager.borrar_dato(direccion_logica)
    return jsonify({"resultado": resultado}), 200

@app.route('/query', methods=['POST'])
def query():
    """Realiza una consulta en la base de datos."""
    consulta = request.json.get('consulta')
    
    if not consulta:
        return jsonify({"error": "Consulta no proporcionada"}), 400
    
    resultado = db_manager.realizar_query(consulta)
    return jsonify({"resultado": resultado}), 200

@app.route('/listar', methods=['GET'])
def listar():
    """Lista todos los datos almacenados en el disco."""
    datos = db_manager.listar_datos()
    return jsonify({"datos": datos}), 200

if __name__ == '__main__':
    app.run(debug=True)