# CampusTaste 开发指南

本文根据上游模板整理为中文，具体已验收结果见[阶段 0 记录](docs/stage-0.md)。当前普通用户管理 Docker 需使用 `sudo`；下文保留通用命令，根据本机权限添加前缀。

## 本地开发

使用 Docker Compose 运行 PostgreSQL、Redis 和 Mailpit，在本机运行 FastAPI 与 Vite 开发服务器。

在项目根目录启动依赖：

```bash
docker compose up -d --wait db redis mailpit
```

进入 `backend` 目录，安装锁定依赖并准备数据库：

```bash
uv sync --locked
uv run --locked bash scripts/prestart.sh
```

启动 FastAPI 开发服务器：

```bash
uv run --locked fastapi dev --host 127.0.0.1
```

在另一个终端，从项目根目录安装前端依赖并启动 Vite：

```bash
bun install
bun run dev
```

可访问以下地址：

- 前端开发服务器：<http://localhost:5173>。
- 后端 API：<http://localhost:8000>。
- Swagger UI 交互文档：<http://localhost:8000/docs>。
- Mailpit：<http://localhost:8025>。

前端开发服务器根据 `frontend/.env` 连接 `http://localhost:8000` 的后端。

### 由 FastAPI 提供前端

在 `frontend` 目录构建：

```bash
bun run build
```

产物写入 `backend/app/frontend`，由 FastAPI 在 <http://localhost:8000> 提供。修改前端后需重新构建。

## 使用 Docker Compose 运行完整应用

```bash
docker compose run --rm backend bash scripts/prestart.sh
docker compose watch
```

可访问以下地址：

- 应用（前端与 API）：<http://localhost:8000>。
- 交互文档：<http://localhost:8000/docs>。
- Adminer 数据库管理界面：<http://localhost:8080>。
- Traefik 路由管理界面：<http://localhost:8090>。
- Mailpit：<http://localhost:8025>。

启动容器中的后端前，应先停止占用 `8000` 端口的本机 FastAPI。首次启动需要等待服务就绪；使用 `docker compose logs` 查看全部日志，或 `docker compose logs backend` 查看后端日志。

## Mailpit 本地邮件测试

[Mailpit](https://mailpit.axllent.org) 捕获本地开发邮件，不向外部收件人实际投递。本机后端连接 `localhost:1025`，Compose 后端连接 `mailpit` 服务。在 <http://localhost:8025> 查看捕获的邮件。

## Compose 文件与环境变量

- `compose.yml`：共享配置，Compose 默认加载。
- `compose.override.yml`：本地端口、源码挂载等开发配置，默认叠加到主配置上。
- `compose.deploy.yml`：HTTPS 和自动证书等部署配置，部署时需显式与主配置组合。

后端从根目录 `.env` 读取配置。Compose 也使用它进行变量插值，并向容器传递所需配置。修改变量后需重新启动应用：

```bash
docker compose watch
```

## `.env` 文件

CampusTaste 跟踪 `.env.example`，真实 `.env` 已加入 Git 忽略规则，不提交密钥。现有工作区已生成随机开发密钥，不要用示例覆盖。

本机进程使用 `localhost` 连接依赖；Compose 为容器覆盖数据库和 SMTP 主机名，改用服务名。部署密钥应按 [FastAPI Cloud 指南](deployment.md)或 [Compose 部署指南](deployment-docker-compose.md)配置，不使用本地开发密钥。

## 提交前钩子与静态检查

项目使用 [prek](https://prek.j178.dev/) 运行代码检查和格式化，它是 [pre-commit](https://pre-commit.com/) 的替代工具。配置位于根目录 `.pre-commit-config.yaml`。

### 安装自动钩子

`prek` 已列入项目依赖。在根目录运行：

```bash
uv run prek install -f
```

`-f` 会覆盖已有的提交前钩子。之后执行 `git commit` 时，prek 会检查并格式化待提交代码。若文件被修改，需要检查变更并重新暂存后再提交。

### 手动检查

```bash
uv run prek run --all-files
```

本阶段实际执行的是后端 Ruff 检查；完整钩子及 CI 的验证状态见阶段记录。
