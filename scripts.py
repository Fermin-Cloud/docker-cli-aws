import subprocess
import json
import os

def traducir_texto(texto, idioma_origen, idioma_destino):
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION")

    if not all([access_key_id, secret_access_key, region]):
        print("Faltan algunas variables de entorno necesarias.")
        return None
    
    comando_docker = [
        "docker", "exec", "aws-cli",  
        "aws", "translate", "translate-text",
        "--text", texto,
        "--source-language-code", idioma_origen,
        "--target-language-code", idioma_destino,
        "--region", region
    ]

   
    resultado = subprocess.run(comando_docker, capture_output=True, text=True, env={
        **os.environ,  
        "AWS_ACCESS_KEY_ID": access_key_id,
        "AWS_SECRET_ACCESS_KEY": secret_access_key,
        "AWS_REGION": region
    })

    if resultado.returncode == 0:
        respuesta = json.loads(resultado.stdout)
        return respuesta["TranslatedText"]
    else:
        print(f"Error: {resultado.stderr}")
        return None

texto_a_traducir = "Hola, mundo"
idioma_origen = "es"
idioma_destino = "en"

texto_traducido = traducir_texto(texto_a_traducir, idioma_origen, idioma_destino)

if texto_traducido:
    print(f"Texto traducido: {texto_traducido}")
