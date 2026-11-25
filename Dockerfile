from python:3.14-slim

workdir /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py index.html model.pkl ./

EXPOSE 8000

CMD ['uvicorn', 'app:app', '--host', '0.0.0.0', '--port', '8000']