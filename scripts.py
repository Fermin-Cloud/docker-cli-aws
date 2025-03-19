import subprocess
import json
import os
from dotenv import load_dotenv

# docker build -t aws-cli .
# docker run --rm -it --env-file .env -v "$(pwd)":/app aws-cli /bin/sh

load_dotenv() 

def traducir_texto(texto, idioma_origen, idioma_destino):
    region = os.getenv("AWS_REGION")

    if not region:
        print("Falta la variable de entorno AWS_REGION.")
        return None

    comando_docker = [
        "docker", "run", 
        "-e", f"AWS_ACCESS_KEY_ID={os.getenv('AWS_ACCESS_KEY_ID')}",
        "-e", f"AWS_SECRET_ACCESS_KEY={os.getenv('AWS_SECRET_ACCESS_KEY')}",
        "-e", f"AWS_REGION={region}",
        f"{os.getenv('CONTAINER_NAME')}",  
        "aws", "translate", "translate-text",
        "--text", texto,
        "--source-language-code", idioma_origen,
        "--target-language-code", idioma_destino,
        "--region", region
    ]

    resultado = subprocess.run(comando_docker, capture_output=True, text=True)

    if resultado.returncode == 0:
        try:
            respuesta = json.loads(resultado.stdout)
            return respuesta.get("TranslatedText", "No translation found")
        except json.JSONDecodeError:
            print("Error al procesar la respuesta JSON:", resultado.stdout)
            return None
    else:
        print(f"Error ejecutando AWS CLI: {resultado.stderr}")
        return None

texto_a_traducir = "Hola, mundo"
idioma_origen = "es"
idioma_destino = "en"

texto_traducido = traducir_texto(texto_a_traducir, idioma_origen, idioma_destino)

if texto_traducido:
    print(f"Texto traducido: {texto_traducido}")
