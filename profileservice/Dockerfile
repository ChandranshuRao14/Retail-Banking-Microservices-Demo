#version number
FROM golang:latest 
WORKDIR /app
ADD . /app
RUN go build -o main . 
COPY ./svc.json /app
ENV GOOGLE_APPLICATION_CREDENTIALS /app/svc.json
ENTRYPOINT ["/app/main"]
EXPOSE 8080