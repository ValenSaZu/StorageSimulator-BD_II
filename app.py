from flask import Flask, request, jsonify, render_template
from database_manager import DatabaseManager

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulador')
def simulador():
    return render_template('simulador.html')

if __name__ == "__main__":
    app.run(debug=True)