FROM python:3.11.14-alpine3.23

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

ENV DB_URI=
EXPOSE 8000

CMD uvicorn library_app:app --host localhost --port 8000
