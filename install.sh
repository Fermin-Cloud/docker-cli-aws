#!/bin/bash

# Validar si Docker está instalado
if ! command -v docker &> /dev/null
then
    echo "Error: Docker no está instalado. Por favor, instala Docker para continuar."
    exit 1
fi

# Validar si Docker está corriendo
if ! docker info &> /dev/null
then
    echo "Error: Docker no está corriendo. Inicia el servicio de Docker y vuelve a intentarlo."
    exit 1
fi

# Validar si el Dockerfile existe en el directorio actual
if [ ! -f "dockerfile" ]; then
    echo "Error: No se encuentra un archivo Dockerfile en el directorio actual."
    exit 1
fi

# Validar si el archivo .env existe (opcional, si necesitas variables de entorno)
if [ ! -f ".env" ]; then
    echo "Advertencia: No se encontró el archivo .env. Asegúrate de tener las variables de entorno configuradas."
fi

# Validar si el directorio tiene permisos adecuados para construir la imagen
if [ ! -w "." ]; then
    echo "Error: No tienes permisos de escritura en el directorio actual. Asegúrate de tener los permisos necesarios."
    exit 1
fi

# Confirmación antes de proceder con la construcción de la imagen
read -p "¿Estás seguro de que deseas construir la imagen de Docker 'aws-cli'? (s/n): " confirm
if [[ ! "$confirm" =~ ^[sS]$ ]]; then
    echo "Proceso cancelado por el usuario."
    exit 0
fi

echo "Construyendo la imagen Docker 'aws-cli'..."
docker build -t aws-cli .

# Validar si la construcción de la imagen fue exitosa
if [ $? -eq 0 ]; then
    echo "¡La imagen 'aws-cli' se construyó correctamente!"
else
    echo "Error: Hubo un problema al construir la imagen."
    exit 1
fi
