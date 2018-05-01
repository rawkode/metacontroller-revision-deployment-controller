FROM python:3 AS dependencies

WORKDIR /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

# Image with dependencies, but nothing else added; for development
FROM dependencies AS development

FROM dependencies AS production

WORKDIR /app
COPY / /app

ENV FLASK_APP watch.py

WORKDIR /app/src

ENTRYPOINT [ "python" ]
CMD [ "-m", "flask", "run", "--host", "0.0.0.0", "--port", "80" ]
