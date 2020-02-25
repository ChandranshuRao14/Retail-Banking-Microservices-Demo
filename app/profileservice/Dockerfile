#version number
FROM golang:latest
WORKDIR /app
#cache dependencies for faster builds
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o main .
ENTRYPOINT ["/app/main"]
EXPOSE 8080