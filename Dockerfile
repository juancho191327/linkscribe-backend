FROM python:3.11 as build-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim
RUN apt-get update -y && apt-get install build-essential -y
RUN pip install transformers
RUN pip install tensorflow
WORKDIR /app
COPY --from=build-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pwd 
COPY  . .

RUN pwd && ls -la

EXPOSE 8080
#CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "--reload-dir", ".", "api:app", "--port", "8080"]
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8080"]
