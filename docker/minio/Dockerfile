FROM golang:1.24.8-bookworm AS builder

ARG MINIO_VERSION=RELEASE.2025-10-15T17-29-55Z
WORKDIR /src
RUN git clone --depth 1 --branch "${MINIO_VERSION}" https://github.com/minio/minio.git .
RUN CGO_ENABLED=0 go build -trimpath -o /out/minio .

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /out/minio /usr/local/bin/minio
COPY --from=builder /src/LICENSE /usr/share/licenses/minio/LICENSE
EXPOSE 9000 9001
ENTRYPOINT ["minio"]
