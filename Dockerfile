#Importamos una imagen de python para no tener que construir todo en base al SO
FROM python:3.12-slim

#Elijo el directorio raíz de la aplicación como directorio de trabajo 
WORKDIR .

#Copio primero el archivo requirements.txt para aprovechar la cache de python
COPY requirements.txt .

#Instalo las dependencias necesarias para la aplicación
RUN pip install --no-cache-dir -r requirements.txt

#Copio la aplicación a la imagen de Docker 
COPY . . 

#Expongo el puerto 8000 para levantar el servidor
EXPOSE 8000

#Ejecuto el comando para poder ejecutar el servidor y así correr la app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]