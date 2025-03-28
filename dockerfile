FROM ubuntu:latest

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    python3 \
    python3-pip \
    python3-venv 

# Instalar AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm awscliv2.zip

# Configurar entorno de trabajo
WORKDIR /app
COPY requirements.txt .

# Crear y activar el entorno virtual
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["/app/venv/bin/uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
