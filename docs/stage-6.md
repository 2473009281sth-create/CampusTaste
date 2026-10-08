# 阶段 6：工程化、负载测试与交付

当前状态：已验证（2026-10-04）。本地后端部署、测试和只读压测通过；GitHub Actions 已配置并校验 YAML，未在云端运行。

## 实现范围

- 后端演示栈 `compose.campustaste.yml` 与 `scripts/start-campus.sh`：保留原模板前端栈，新增不构建模板前端的后端镜像；迁移和演示数据初始化成功后，API、Worker、Beat 才启动。端口绑定本机，不发布公网。
- 应用日志使用 JSON，包含 UTC 时间、请求 ID、路由模板、状态码、耗时；不记录请求头、查询串、正文。异常只记录类型，避免将连接凭据写入应用日志。第三方服务器日志不保证采用同一格式。
- 存活接口 `/api/v1/utils/health-check/` 保留；新增就绪接口 `/api/v1/utils/ready/`，检查 PostgreSQL、Redis、RabbitMQ、MinIO，失败返回 503，不输出异常内容。
- CI 启动真实依赖，执行 Ruff、mypy、ty、独立测试库完整 pytest、覆盖率门槛和 Alembic 模型漂移检查。GitHub Actions 配置已写入，但未推送，尚未有云端运行结果。
- Locust 只读负载使用独立 PostgreSQL 库和 Redis 14，生成 100 个菜品、100 个普通用户、10000 条评价；依赖与 API、压测进程共享本机资源。
- 演示、接口、架构取舍、排障、简历和面试索引见本目录交付文档。

## 启动和验证

在项目根目录，确认 `.env` 已填写本地密钥：

```bash
sudo bash scripts/start-campus.sh
```

若使用已有本地代理，且端口为 7897：

```bash
sudo env HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bash scripts/start-campus.sh
```

构建中的 `network: host` 用于 WSL 原生 Docker 访问本机代理；Docker Desktop 的网络模式不同，需要按实际代理地址调整。Docker 拉取基础镜像使用守护进程自己的代理，构建参数不能替代它。

```bash
curl -f http://localhost:8000/api/v1/utils/ready/
cd backend
UV_CACHE_DIR=/tmp/campustaste-uv-cache uv run --frozen --package app python scripts/test-stage5.py
UV_CACHE_DIR=/tmp/campustaste-uv-cache uv run --frozen --package app python scripts/run-loadtest.py
```

沿用 `test-stage5.py` 文件名，但它运行全部后端测试。脚本会创建并使用独立 `campustaste_test` 库和 Redis DB 15；测试清理仅针对测试数据。压测保留 `campustaste_loadtest` 库，重复执行不会重复插入确定性数据，使用 Redis DB 14。压测脚本占用 8010 端口，只启动和停止自己创建的 API 子进程。

## 当前验证记录

- Ruff 和格式检查通过（68 个 Python 文件）；mypy 检查 41 个应用文件通过；ty 指定项目虚拟环境后通过。
- 日志脱敏、请求 ID、就绪失败与存活分离专项测试：2 项通过。
- Compose 配置解析与启动脚本语法检查通过。
- 初次镜像构建在 `ghcr.io` 拉取 uv 时 TLS 超时；已改为通过 PyPI 安装固定 uv 0.12.1，并支持构建代理。
- 用户在 WSL 使用代理启动后端演示栈成功，真实 HTTP 存活、就绪和 OpenAPI 均返回 200，响应包含请求 ID；四个依赖检查全部为 ok。
- 新镜像 API 上传真实 PNG，Compose Worker 生成 480×320 WebP，签名 URL 访问返回 200；构造本次图片的待补偿任务后，Compose Beat 定时补偿实际完成。仅清理了本次验证创建的图片、任务与存储对象。
- 独立 PostgreSQL 库与 Redis DB 15 上完整测试 98 项通过，语句覆盖率 90%，34.61 秒；唯一警告为模板 TestClient 兼容层弃用提示。Alembic check 没有模型漂移。
- Locust 最终统计：10 用户 1932 请求、32.85 RPS、P50 7ms、P95 15ms；30 用户 5591 请求、96.72 RPS、P50 7ms、P95 17ms；两轮失败数均为 0。负载条件与局限见 performance.md。
- GitHub Actions 未推送或远程执行；未部署公网，未验收模板前端。没有用本机只读负载证明服务容量上限。
- 临时测试 Worker 和压测 API 已停止，用户启动的 Compose 服务保留运行，测试库和压测库保留供复现。

## 面试问题

1. 存活与就绪有什么区别？存活证明 API 进程能应答，就绪检查本项目依赖；就绪失败不等于应该立即重启进程。
2. 为什么 request_id 使用 ContextVar？让同一请求的日志关联，同时避免并发请求共享普通全局变量。客户端 ID 有字符及长度限制，不是认证凭据。
3. 就绪能证明 Worker 工作吗？不能；这里只检查依赖连接，Worker 处理链路依赖任务状态与集成验证。
4. 压测能证明多少容量？只能说明记录的资源、数据规模和只读负载下的表现，不能推导公网可用性、写入容量或性能提升比例。
5. 为什么 CI 用独立数据库？测试会创建并清理数据，必须与开发数据库隔离；迁移和模型漂移也要在真实 PostgreSQL 验证。
