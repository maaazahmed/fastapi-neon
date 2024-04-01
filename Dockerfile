FROM python:latest
WORKDIR /app
COPY . .
COPY pyproject.toml .
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "fastapi_neon.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]

# FROM python:latest
# COPY . .
# COPY pyproject.toml . 
# ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
# RUN pip3 install poetry
# RUN poetry config virtualenvs.create false
# RUN poetry install --no-dev
# RUN poetry install
# EXPOSE 8000
# CMD [ "poetry", "run", "uvicorn", "fastapi_neon.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]