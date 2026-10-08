# CampusTaste 后端开发

## 环境要求

- [Docker](https://www.docker.com/) 与 Docker Compose，用于 PostgreSQL、Redis 和 Mailpit。
- [uv](https://docs.astral.sh/uv/)，用于 Python 和依赖管理。
- 使用根目录 `.python-version` 和 `uv.lock` 指定的版本。

## 本地开发

在项目根目录启动依赖；当前用户无 Docker socket 权限时，需加 `sudo`：

```bash
docker compose up -d --wait db redis mailpit
```

进入 `backend` 目录，安装依赖、执行迁移与初始化，然后启动后端：

```bash
uv sync --locked
uv run --locked bash scripts/prestart.sh
uv run --locked fastapi dev --host 127.0.0.1
```

API 地址为 `http://localhost:8000`，交互文档地址为 `http://localhost:8000/docs`。详细验收步骤见[阶段 0 文档](../docs/stage-0.md)。

## 日常开发与代码结构

在 `backend` 目录使用 `uv run` 执行后端命令。编辑器的 Python 解释器应选择项目根目录 `.venv/bin/python`。

- `app/models.py`：SQLModel 数据表和请求响应模型。
- `app/api/`：API 路由与依赖。
- `app/crud.py`：数据创建、读取、更新和删除操作。
- `app/core/`：配置、数据库连接与安全工具。
- `app/alembic/`：数据库迁移。
- `tests/`：后端测试。

## VS Code 编辑器配置

模板提供调试与测试相关编辑器配置，可用于断点、变量检查及 Python 测试面板。本项目保留工作区原有 `.vscode/extensions.json`，需要结合实际安装的扩展使用。

## 使用 Docker Compose 运行完整应用

```bash
docker compose run --rm backend bash scripts/prestart.sh
docker compose watch
```

应用地址为 `http://localhost:8000`。

### 本地覆盖配置

`compose.override.yml` 配置发布端口、源码同步、镜像重建和后端重载。未显式指定文件列表时，Compose 自动加载此文件。

进入后端容器：

```bash
docker compose exec backend bash
```

## 后端测试

模板测试会在结束时清空 User 和 Item 数据。请先按照[阶段 0 的独立测试库步骤](../docs/stage-0.md)配置 `DATABASE_URL`，不要直接指向开发或生产数据。

配置好独立测试库后，在 `backend` 目录执行：

```bash
uv run --locked bash scripts/test.sh
```

测试由 pytest 执行，可在 `tests/` 修改或新增用例。模板含 GitHub Actions 工作流，但本项目尚未验证 CI，且需要处理分支名与 `.env` 的配置差异。

### 在运行中的测试容器内执行

仅当容器连接的是可丢弃测试库时，可运行：

```bash
docker compose exec backend bash scripts/tests-start.sh
```

当前 `tests-start.sh` 调用 `test.sh`；附加参数被后者用作覆盖率 HTML 标题，不会传给 pytest。需要首次失败就停止时，应直接调用：

```bash
docker compose exec -e FASTAPI_ENV=development backend pytest tests/ -x
```

### 覆盖率

测试脚本生成 `backend/htmlcov/index.html`，可用浏览器查看。阶段 0 实测 58 项通过，语句覆盖率 91%；这属于原模板测试结果。

## 数据库迁移

修改模型后，应新增 Alembic 迁移并升级数据库。Alembic 已配置导入 `app/models.py` 中的 SQLModel 模型。

在 `backend` 目录生成迁移，例如新增字段后：

```bash
uv run --locked alembic revision --autogenerate -m "Add column last_name to User model"
```

检查自动生成的内容，确认正确后执行：

```bash
uv run --locked alembic upgrade head
```

将迁移文件纳入版本管理。CampusTaste 明确使用迁移管理表结构，不采用上游可选的 `SQLModel.metadata.create_all(engine)` 方式，也不删除已有迁移重新初始化。

## 邮件模板

模板使用 [React Email](https://react.email)，源码位于 `packages/react-email/`。`emails` 目录中每个组件对应一种邮件，`ui` 目录包含布局、标题、按钮、链接和提示等共享组件。

`backend/app/email-templates/` 中的 HTML 是生成产物，应用会发送这些内容，不应直接手动编辑。

在项目根目录启动邮件预览：

```bash
bun run email:dev
```

后端值在组件属性中表示为 Jinja 占位符，例如 `username = "{{ username }}"`。邮件上下文在 `app/utils.py` 的 `generate_*_email()` 函数中构建，新增占位符时需同步更新上下文。

完成修改后重新导出：

```bash
bun run email:export
```
