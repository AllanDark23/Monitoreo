# -*- coding: utf-8 -*-
"""
servidor_ia.py — Backend opcional para "Tom", el analista IA del dashboard CMT T.

Sin este servidor, el dashboard funciona igual: Tomz usa su motor local
(respuestas calculadas con JavaScript sobre los datos en pantalla).
Con este servidor corriendo, Tomzín responde en lenguaje natural usando
la API de Claude, recibiendo como contexto los datos y filtros de la pantalla.

USO:
  1) pip install flask flask-cors requests
  2) Definir la clave (NO escribirla dentro del código ni compartirla):
        Windows:   set ANTHROPIC_API_KEY=tu_clave
        Linux/Mac: export ANTHROPIC_API_KEY=tu_clave
  3) python servidor_ia.py
  4) Abrir index.html — el chat detecta el servidor automáticamente.
"""
import os, json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODELO = "claude-sonnet-4-6"

app = Flask(__name__)
CORS(app)  # permite que el HTML abierto localmente llame a este servidor

SISTEMA = (
    "Sos Tom, el analista de datos del Centro de Monitoreo  en El Salvador, "
    "una empresa distribuidora de gas propano. Respondés en español salvadoreño profesional "
    "pero cercano (voseo suave), de forma breve y accionable. "
    "SOLO podés usar los datos JSON que vienen en el mensaje: son las medidas visibles en el "
    "dashboard con los filtros que el usuario aplicó. No inventés cifras que no estén ahí. "
    "Si te preguntan algo fuera de esos datos, decilo con claridad y sugerí qué dato haría falta. "
    "Usá **negritas** para las cifras clave y máximo 6-8 líneas por respuesta."
)


@app.post("/preguntar")
def preguntar():
    if not API_KEY:
        return jsonify({"error": "Falta la variable de entorno ANTHROPIC_API_KEY"}), 500
    cuerpo = request.get_json(force=True)
    pregunta = cuerpo.get("pregunta", "")
    filtros = cuerpo.get("filtros", {})
    datos = cuerpo.get("datos", {})

    mensaje = (
        f"Filtros activos en pantalla: {json.dumps(filtros, ensure_ascii=False)}\n\n"
        f"Datos visibles del dashboard (JSON):\n{json.dumps(datos, ensure_ascii=False)}\n\n"
        f"Pregunta del usuario: {pregunta}"
    )

    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODELO,
            "max_tokens": 700,
            "system": SISTEMA,
            "messages": [{"role": "user", "content": mensaje}],
        },
        timeout=30,
    )
    r.raise_for_status()
    respuesta = "".join(b.get("text", "") for b in r.json().get("content", []))
    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    print("Tomzín backend en http://localhost:8765  (Ctrl+C para detener)")
    app.run(port=8765)
