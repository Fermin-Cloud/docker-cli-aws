import requests

API_URL = "http://localhost:8000/translate/"

def traducir_texto(texto, idioma_origen, idioma_destino):
    data = {
        "text": texto,
        "source_language": idioma_origen,
        "target_language": idioma_destino
    }
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        return response.json().get("translated_text", "Error en la traducción")
    else:
        return f"Error en la solicitud: {response.text}"

if __name__ == "__main__":
    idioma_origen = "es"
    idioma_destino = "en"

    while True:
        texto_a_traducir = input("Ingrese el texto a traducir (o 'salir' para terminar): ")
        if texto_a_traducir.lower() == "s":
            break

        texto_traducido = traducir_texto(texto_a_traducir, idioma_origen, idioma_destino)
        print(f"Texto traducido: {texto_traducido}")
