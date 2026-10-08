# 阶段 5：图片存储与异步缩略图

当前状态：已验证（2026-10-03）。

## 已实现范围

- MinIO 桶默认保持私有，原图和缩略图只能通过后端签发的短时 GET URL 访问。
- 上传接口限制读取字节数，并使用 Pillow 校验实际格式、可解码性、动画帧和解码后像素数。
- 只接受 JPEG、PNG、WebP；对象名使用服务端 UUID，不使用客户端文件名或路径。
- 图片直接绑定菜品或评价，上传人由 Access Token 写入；评价图片要求当前用户是评价作者。
- `imageasset` 保存对象位置、真实格式、尺寸、归属和公开处理状态。
- `imageprocessingjob` 保存投递、尝试次数、下次重试时间、错误和完成状态。
- Celery 通过 RabbitMQ 处理缩略图，使用晚确认、Worker 丢失重投和单任务预取。
- 缩略图固定写入 `thumbnails/{image_id}.webp`，任务重复执行不会创建多个结果。
- 暂时故障采用有上限的指数退避；无法解码的存量原图直接标记永久失败。
- 数据库记录先提交再投递消息；投递失败时任务保持待处理，由 Celery Beat 每 30 秒补偿扫描。
- 处理中任务超过 5 分钟会被扫描器重新置为待处理，用于 Worker 异常退出后的恢复。
- Worker 在存储访问期间持有任务行锁，补偿扫描使用 `FOR UPDATE SKIP LOCKED` 跳过正在执行的任务，避免把耗时任务误认作失联任务。代价是处理期间占用数据库连接，适合当前受大小限制的图片任务。
- 自动处理最多尝试 5 次，包含持久化的开始处理次数；重复消息不会绕过退避时间或重新执行失败、成功状态的任务。
- RabbitMQ 4 默认拒绝 Celery 某些临时非独占控制队列，本项目关闭远程控制、mingle 和 gossip；持久化图片任务队列继续正常工作。
- 审核员可查询失败图片；图片所有者、审核员或管理员可以人工重试失败任务。

## 接口

```text
POST /api/v1/dishes/{dish_id}/images
POST /api/v1/reviews/{review_id}/images
GET  /api/v1/images/{image_id}
GET  /api/v1/images/{image_id}/original-url
GET  /api/v1/images/{image_id}/thumbnail-url
POST /api/v1/images/{image_id}/retry
GET  /api/v1/image-jobs/failed
```

上传接口使用 `multipart/form-data` 的 `file` 字段。状态接口先返回 `pending`，Worker 完成后变为 `ready`；缩略图尚未就绪时请求缩略图 URL 返回 409。

## 可靠性边界

系统不宣称消息只消费一次。可靠性来自以下组合：

1. PostgreSQL 先持久化图片和任务，再投递 RabbitMQ。
2. 投递失败不会删除任务，周期扫描负责再次投递。
3. Celery 晚确认降低 Worker 执行中退出造成消息丢失的概率。
4. 固定缩略图对象名和数据库完成状态使重复投递、重复执行安全。
5. 失败次数达到配置上限后停止自动重试，保留错误并等待人工重试。

数据库与 MinIO 无法组成一个原子事务。原图上传成功但数据库提交失败时，服务会尽力删除原图；清理也失败时仍可能产生无数据库引用的孤儿对象，后续可增加按对象清单对账的运维命令。

签名 URL 默认为 15 分钟有效。签发时检查资源可见性，但之后隐藏评价不会立即撤销已签发的 URL；客户端持有者可在过期前继续访问。任务状态保存在 PostgreSQL，不依赖 Celery 结果后端。图片上传只绑定当前请求指定的资源，未提供将他人图片重新绑定到自己资源的入口。

## 本地启动与验收

在 WSL 终端执行：

```bash
cd /home/david/CampusTaste
sudo docker compose up -d --wait db redis rabbitmq minio mailpit

cd backend
uv run alembic upgrade head

cd ..
sudo docker compose up -d --build backend worker beat
sudo docker compose ps

cd backend
uv run python scripts/test-stage5.py
uv run alembic check
uv run ruff check app tests
uv run ruff format --check app tests
uv run mypy app
uv run ty check app
```

访问地址：MinIO API 为 `http://localhost:9000`，管理控制台为 `http://localhost:9001`，RabbitMQ 管理界面为 `http://localhost:15672`。

## 实际验收结果

MinIO 官方预构建镜像在当前环境返回访问拒绝，已改为通过 `docker/minio/Dockerfile` 构建官方固定版本 `RELEASE.2025-10-15T17-29-55Z`，并保留其许可证。来源及源码构建说明：https://github.com/minio/minio/releases/tag/RELEASE.2025-10-15T17-29-55Z 。本地 Docker 构建阶段使用 host 网络；WSL 用户如使用本机代理，需要通过标准 `HTTP_PROXY`、`HTTPS_PROXY` 构建参数传入，Docker daemon 代理不会自动传入构建步骤。

- 依赖已锁定：Celery、MinIO Python SDK、Pillow。
- Ruff、格式检查、mypy、ty、Compose 配置检查通过。
- OpenAPI 成功生成，共 48 条路径，其中 7 条为阶段 5 图片接口。
- Alembic 从空库到 head 的离线 PostgreSQL SQL 生成通过。
- 实际图片解码及 1200×800 到 480×320 WebP 缩略图生成通过。
- 不依赖外部服务的图片安全校验与缩略图单元测试 3 项通过。
- 用户启动 MinIO、RabbitMQ、PostgreSQL、Redis 和 Mailpit 后，真实迁移和集成验收已完成。
- 开发库及独立 `campustaste_test` 数据库升级至 `f4d5e6f7a8b9`。
- 一次性 PostgreSQL 数据库完成空库升级、降级至阶段 4、再升级，随后清理了仅本次创建的临时数据库；模型漂移检查无差异。
- 完整后端测试 96 项通过，语句覆盖率 90%，唯一警告来自模板的 Starlette TestClient 兼容层。
- 真实流水线测试通过 MinIO 上传下载、WebP 缩略图、签名 URL、匿名访问拒绝、RabbitMQ 投递、独立 Worker 消费、重复投递、永久失败及人工重试。
- 恢复验证实际停止并重启 Worker，并构造过期 `PROCESSING` 记录验证补偿；该测试不等同于在每个执行窗口强杀 Worker 的故障穷举。
- 暂时故障退避、自动尝试上限、归属和隐藏资源权限由独立 PostgreSQL 加受控故障注入测试覆盖；Broker 故障投递由受控失败注入验证，未停止用户运行中的 RabbitMQ。
- 验收期间创建的 Worker 进程已停止，用户启动的依赖容器保持运行。日常异步处理仍需按上方命令启动 Worker 和 Beat。
