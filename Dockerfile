FROM python:3 AS development

RUN pip install pipenv

ENV PIPENV_VENV_IN_PROJECT true
ENV FLASK_APP watch.py
ENV PS1 " 🐳 \[\033[1;36m\]\W\[\033[0;35m\] # \[\033[0m\]"

FROM development

WORKDIR /app

ENV PATH $PATH:/app/.venv/bin
ENV PYTHONPATH /app/src/

COPY /Pipfile /app/

RUN pipenv install

COPY / /app

EXPOSE 80

WORKDIR /app/src/
ENTRYPOINT [ "/app/.venv/bin/python" ]
CMD [ "-m", "flask", "run", "--host", "0.0.0.0", "--port", "80" ]
