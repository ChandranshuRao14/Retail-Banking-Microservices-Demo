FROM python:3.8.0
WORKDIR loadgen
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["sh", "-c","sleep 10; locust --no-web -c 100"]