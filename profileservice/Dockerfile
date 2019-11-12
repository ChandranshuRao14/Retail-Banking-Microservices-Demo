#version number
FROM golang:latest 
WORKDIR /app
ADD . /app
RUN go build -o main . 
ENTRYPOINT ["/app/main"]
EXPOSE 8080