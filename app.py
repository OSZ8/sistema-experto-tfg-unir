from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Sistema Experto para la Toma de Decisiones Estratégicas en League of Legends - TFG UNIR"

if __name__ == '__main__':
    app.run(debug=True)
