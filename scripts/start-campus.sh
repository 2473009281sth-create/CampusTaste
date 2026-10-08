#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ ! -f .env ]]; then
  echo '请先复制 .env.example 为 .env，并填写本地密钥。' >&2
  exit 1
fi
docker compose -f compose.campustaste.yml build \
  --build-arg "HTTP_PROXY=${HTTP_PROXY:-}" \
  --build-arg "HTTPS_PROXY=${HTTPS_PROXY:-}"
docker compose -f compose.campustaste.yml up -d --no-build --wait
echo '后端文档：http://localhost:8000/docs'
echo '就绪检查：http://localhost:8000/api/v1/utils/ready/'
