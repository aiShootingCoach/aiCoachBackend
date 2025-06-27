# Użyj oficjalnego obrazu Pythona w wersji slim
FROM python:3.10-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki projektu
COPY . .

# Zainstaluj zależności
RUN pip install --no-cache-dir fastapi uvicorn python-multipart aiofiles

# Ustaw zmienną środowiskową dla katalogu uploads
ENV UPLOAD_DIR=/app/data/user_shots

# Utwórz katalog na pliki
RUN mkdir -p /app/data/user_shots

# Uruchom aplikację
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]