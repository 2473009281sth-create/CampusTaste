# 阶段 0 交付与验收

当前状态：已验证（2026-09-23）。本次完成阶段 0 的后端启动验收，未进入阶段 1。

## 最终实际验收结果

- 用户在 WSL 启动 db/mailpit，截图显示均 Healthy。Docker Compose 2.40.3；代理普通用户调用 docker compose ps 仍因 socket 权限失败，未修改权限，通过数据库真实连接继续验证。
- PostgreSQL 实际版本 18.6；开发库 `app` 完成全部五个 Alembic 迁移，`alembic current` 为 `fe56fa70289e (head)`；`prestart.sh` 成功创建初始管理员。
- 通过 PostgreSQL 管理连接创建独立 `campustaste_test` 库并执行迁移，然后运行原 `uv run --locked bash scripts/test.sh`：**58 passed，2 warnings，6.27 秒，语句覆盖率 91%**。测试清理只作用于独立测试库，开发管理员保留。
- `uv run --locked ruff check app tests`：All checks passed。
- 临时监听 `127.0.0.1:18000` 的真实 HTTP 检查：`/docs`、`/api/v1/openapi.json`、存活接口均 200；使用 .env 中的管理员账号登录 200；Bearer test-token 返回对应用户且不含密码哈希；错误密码 400；无 Bearer 令牌 401。没有输出密码或令牌。
- 临时后端进程检查后已停止；PostgreSQL/Mailpit 保持运行。下文启动命令可供自行体验。
- 日志：`.local/migration-verified.log`、`.local/tests-verified.log`、`.local/server-verified.log`、`.local/http-verified.log`；覆盖率报告 `backend/htmlcov/index.html`。日志与报告不入库。
- 两项上游警告：Starlette TestClient 的 httpx 使用弃用提示、未构建前端目录提示。均不影响当前开发模式后端验收，阶段 0 不升级锁定依赖或改造前端。
- 前端页面构建、浏览器端 E2E、GitHub Actions 未运行；91% 是模板后端测试结果，不是新增校园业务的覆盖率。

以下初次失败记录保留用于排障，以本节最终结果为准。

## 初次环境与检查（历史）

初始目录只有 `.vscode/extensions.json`，不属于 Git 仓库；已保留该文件，创建 main 分支，尚无提交。Git 2.43.0，系统 Python 3.12.3，uv 0.12.1；python、poetry、docker、psql、postgres、bun 均未找到。使用 uv 管理的 Python 3.14.6，不改动系统 Python。

执行工具最初因 bubblewrap 的 `/mnt/wslg/distro` 挂载错误无法启动；经命令权限批准后在沙箱外执行。没有安装系统 Docker 或更改系统服务。

| 实际命令或检查 | 结果 |
| --- | --- |
| `git status --short --branch`（引入前） | fatal: not a git repository |
| `docker --version` / `docker compose version` | command not found |
| `uv sync --locked --project backend` | 通过，75 个包安装，保留 uv.lock |
| backend 中 `uv run --locked ruff check app tests` | All checks passed |
| `docker compose up -d db mailpit` | command not found，无法启动服务 |
| backend 中 `uv run --locked bash scripts/prestart.sh` | 退出 1，PostgreSQL localhost:5432 Connection refused；未完成迁移和初始化 |
| backend 中 `FASTAPI_ENV=development uv run --locked pytest tests/ -x -q`，通过进程环境将库改为 campustaste_test | 数据库连接失败，首个 fixture setup 错误；不是测试通过 |
| `FASTAPI_ENV=development uv run --locked uvicorn app.main:app --host 127.0.0.1 --port 18000` | 临时启动后验证，再停止 |
| GET `/docs`、`/api/v1/openapi.json`、`/api/v1/utils/health-check/` | HTTP 200 |
| POST `/api/v1/login/access-token`（占位密码，仅探测数据库路径） | HTTP 500，数据库不可用；正常登录未验证 |
| `git check-ignore .env` | 命中，实际配置权限 0600 |

本地详细日志：`.local/migration.log`、`.local/tests.log`、`.local/server.log`、`.local/http.log`，不加入 Git。最初验收脚本曾因日志目录不存在失败，创建目录后重跑。最初未设置进程 FASTAPI_ENV 的 pytest/Uvicorn 因前端目录缺失失败，按上游开发模式显式设置后解决；Pydantic 读取 .env 不会自动导出整个进程环境。

## 设计与边界

沿用同步 `def` 路由、SQLModel Session 和 psycopg；FastAPI 在线程池处理同步路由。阶段 0 不改成异步数据库。迁移使用 Alembic，不启用被注释的 create_all。模板 Item 只是原示例，不代表菜品模型。

本地后端 + Compose PostgreSQL/Mailpit 是模板推荐流程，避免为后端验收先构建整个前端。Docker 缺失时不以 SQLite 或 Mock 冒充 PostgreSQL。健康接口只返回存活状态，不检查数据库，不能说明就绪。暂不加入 Redis、RabbitMQ、Celery、MinIO 或校园业务。

## 本地启动（可复制）

先在当前 WSL 发行版中配置可用的 Docker Engine/Compose，或启用 Docker Desktop 的 WSL 集成；以 `docker info` 和 `docker compose version` 成功为准。以下仅针对本项目开发数据库。

```bash
cd /home/david/CampusTaste
sudo docker info
docker compose version
# 本次已生成 .env；新克隆才复制 .env.example 并填写随机密钥，不能覆盖已有配置。
uv sync --locked --project backend
sudo docker compose up -d --wait db mailpit
cd backend
uv run --locked bash scripts/prestart.sh
uv run --locked alembic current
uv run --locked fastapi dev --host 127.0.0.1
```

`prestart.sh` 先 `alembic upgrade head`，再执行 `app/initial_data.py` 创建初始管理员。预期迁移 head 为 `fe56fa70289e`。初始管理员邮箱与密码从根目录 .env 读取，不写入文档、终端日志或 Git。模板 fastapi dev 自动进入开发模式。API 文档地址 http://127.0.0.1:8000/docs。

另开终端执行登录验收（不打印密码和令牌）：

```bash
cd /home/david/CampusTaste/backend
uv run --locked python - <<'PYCODE'
import httpx
from app.core.config import settings
with httpx.Client(base_url="http://127.0.0.1:8000") as client:
    for path in ("/docs", "/api/v1/openapi.json", "/api/v1/utils/health-check/"):
        assert client.get(path).status_code == 200, path
    response = client.post("/api/v1/login/access-token", data={
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    })
    assert response.status_code == 200, response.status_code
    token = response.json()["access_token"]
    response = client.post("/api/v1/login/test-token", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == settings.FIRST_SUPERUSER
    response = client.post("/api/v1/login/access-token", data={
        "username": settings.FIRST_SUPERUSER, "password": "wrong-password",
    })
    assert response.status_code == 400
print("文档、正确密码登录、令牌认证、错误密码拒绝：通过")
PYCODE
```

## 原后端测试：独立数据库

模板 `tests/conftest.py` 结束时删除全部 Item/User，因此不能指向有用数据的库。下面只创建独立 `campustaste_test`；若已经存在，跳过 createdb，不删除重建。

```bash
cd /home/david/CampusTaste
sudo docker compose exec -T db createdb -U postgres campustaste_test
cd backend
uv run --locked python - <<'PYCODE'
import os
import subprocess
from app.core.config import settings
env = os.environ.copy()
env["FASTAPI_ENV"] = "development"
env["DATABASE_URL"] = str(settings.DATABASE_URL).rsplit("/", 1)[0] + "/campustaste_test"
subprocess.run(["uv", "run", "--locked", "bash", "scripts/prestart.sh"], env=env, check=True)
subprocess.run(["uv", "run", "--locked", "bash", "scripts/test.sh"], env=env, check=True)
PYCODE
uv run --locked ruff check app tests
```

完整 pytest 已通过并生成覆盖率报告，结果见顶部最终验收。不能把 `-x` 的失败探测当成完整套件验收。开发服务可用 `docker compose stop db mailpit` 停止并保留卷。

## 一条登录请求的路径

1. `app/main.py` 挂载 `api/main.py` 的路由，前缀 `/api/v1`。
2. `api/routes/login.py:login_access_token` 接收表单（不是 JSON），OAuth2PasswordRequestForm 将邮箱放在 username 字段。
3. `api/deps.py:get_db` 为请求提供同步 Session，结束后关闭；`core/db.py` 的 engine 根据 DATABASE_URL 连接 PostgreSQL。
4. `crud.py:authenticate` → `get_user_by_email` → `select(User).where(User.email == email)` 查询数据库。
5. `core/security.py:verify_password` 使用 pwdlib 验证哈希，默认 Argon2，兼容 bcrypt；需要升级旧哈希时 authenticate 会提交更新。
6. 路由检查密码与 is_active。失败返回模板定义的 400；成功调用 create_access_token，生成包含 sub（用户 UUID）、exp（UTC 到期时间）的 HS256 JWT。
7. 后续 Bearer 请求通过 `get_current_user` 验签，并重新查数据库确认用户存在且启用。UserPublic 不返回密码哈希。

本阶段未增加 Refresh Token 或角色系统；模板只有 is_superuser。默认 Access Token 有效期 8 天。当前 CRUD 内部有 commit，后续业务事务需明确边界，不能直接组合多个自提交操作实现评分一致性。

## 面试问题与回答要点

1. **SQLModel 与 Pydantic、SQLAlchemy 的关系？** SQLModel 结合两者；User(table=True) 映射表，UserCreate/UserPublic 表达输入输出，Session 和查询依赖 SQLAlchemy。
2. **登录为什么不用解密数据库密码？** 数据库保存哈希，pwdlib 验证；默认 Argon2，盐和参数在哈希中。JWT 是签名令牌，不应把密码放进载荷。
3. **为什么需要 Alembic？** 模型描述当前结构，迁移描述可追踪的结构演进；create_all 不能代替版本管理与已有表变更。
4. **为什么文档和健康接口正常，登录仍失败？** 前者不访问数据库；登录需查询 User。存活与就绪是不同信号，本轮数据库未运行就是实际例子。
5. **模板测试有什么副作用？** session 级 fixture 初始化用户并在结束时清空 User/Item。应使用独立 PostgreSQL 测试库；本次已使用独立 PostgreSQL 数据库通过测试。

## 未完成与后续范围

阶段 0 后端验收已完成。前端未构建，CI 未验证；普通用户管理 Docker 仍需 sudo。没有新增校园业务。下一阶段仅在明确授权后做基础模型、角色权限与菜品审核。

## 继续阶段 0：环境复查（历史，随后已解决）

再次执行 `docker compose version`、`docker info` 均显示 docker: command not found；`/var/run/docker.sock` 不存在。系统为 WSL2 Ubuntu 24.04，PID 1 为 systemd。`sudo -n true` 返回 `sudo: a password is required`，当前代理不能交互输入系统密码，因此无法自行完成系统级 Docker 安装。没有修改系统服务或安装系统包，也没有重新执行已知缺数据库的测试。

本机 apt 索引提供 Ubuntu 维护的 docker.io 和 docker-compose-v2，可在自己的 WSL 终端执行：

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2
sudo systemctl start docker
sudo docker info
sudo docker compose version
```

这是 Ubuntu 软件源的包，不是 Docker 官方 Docker CE 软件源安装方式。后续若当前用户无 Docker socket 权限，可在本文 docker 命令前加 sudo；无需更改 socket 权限。不要在聊天中发送 sudo 密码。

如采用 Windows Docker Desktop，则启用当前 Ubuntu 发行版的 WSL Integration，使用该路径即可，无需同时安装另一套 Engine。参考 [Docker 官方 WSL 文档](https://docs.docker.com/desktop/features/wsl/)；独立 Docker CE 安装参考 [官方 Ubuntu 文档](https://docs.docker.com/engine/install/ubuntu/)。

Docker 可用后先在本机终端启动依赖：

```bash
cd /home/david/CampusTaste
sudo docker compose up -d --wait db mailpit
```

若 Docker Desktop 集成已允许普通用户访问，则去掉 sudo。依赖启动后可以继续执行本文件的迁移、登录和独立测试库步骤。阶段状态保持“被阻塞”。
