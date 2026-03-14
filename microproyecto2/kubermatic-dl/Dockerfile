FROM python:3.8

WORKDIR /app

# copiar requirements primero (mejor cache de docker)
COPY requirements.txt .

# actualizar pip
RUN pip install --upgrade pip

# instalar dependencias
RUN pip install -r requirements.txt

# copiar el resto de archivos
COPY app.py .
COPY net.params .

CMD ["python", "app.py"]
