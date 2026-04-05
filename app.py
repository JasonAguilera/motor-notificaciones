from supabase import create_client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

from flask import Flask, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

# modelo simple
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([50, 55, 65, 70, 80])

modelo = LinearRegression()
modelo.fit(X, y)

@app.route("/")
def home():
    return {"mensaje": "API IA funcionando 🚀"}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        horas = data.get("horas")

        pred = modelo.predict([[horas]])
        resultado = float(pred[0])

        
        supabase.table("predicciones").insert({
            "horas": horas,
            "resultado": resultado
        }).execute()

        return jsonify({"resultado": resultado})

    except Exception as e:
        return jsonify({
            "error": str(e),
            "mensaje": "fallo en predict"
            }), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)