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

if __name__ == "__main__":
    app.run(debug=True)