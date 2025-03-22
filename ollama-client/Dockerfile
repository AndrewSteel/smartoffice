FROM python:3.11-slim

WORKDIR /app
COPY describe.py .

# Installiere benötigte Python-Pakete
RUN pip install pymongo paho-mqtt

CMD ["python", "describe.py"]