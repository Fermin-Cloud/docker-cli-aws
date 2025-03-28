from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import json
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

def traducir_texto(texto, idioma_origen, idioma_destino):
    region = os.getenv("AWS_REGION")

    if not region:
        return {"error": "Falta la variable de entorno AWS_REGION."}

    comando_aws = [
        "aws", "translate", "translate-text",
        "--text", texto,
        "--source-language-code", idioma_origen,
        "--target-language-code", idioma_destino,
        "--region", region
    ]

    try:
        resultado = subprocess.run(comando_aws, capture_output=True, text=True, check=True)
        respuesta = json.loads(resultado.stdout)
        return {"translated_text": respuesta.get("TranslatedText", "No translation found")}
    except subprocess.CalledProcessError as e:
        return {"error": f"Error ejecutando AWS CLI: {e}", "stderr": e.stderr}
    except json.JSONDecodeError:
        return {"error": f"Error al procesar la respuesta JSON: {resultado.stdout}"}

@app.post("/translate/")
async def translate_text(request: TranslationRequest):
    return traducir_texto(request.text, request.source_language, request.target_language)

@app.get("/")
def read_root():
    return {"message": "¡Servidor en ejecución!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
