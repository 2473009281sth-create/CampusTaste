# CampusTaste 前端开发

前端沿用模板，使用 [Vite](https://vitejs.dev/)、[React](https://react.dev/)、[TypeScript](https://www.typescriptlang.org/)、[TanStack Query](https://tanstack.com/query)、[TanStack Router](https://tanstack.com/router)、[Tailwind CSS](https://tailwindcss.com/) 和 [shadcn/ui](https://ui.shadcn.com/)。当前阶段 0 已验证后端，前端构建与端到端测试尚未运行。

## 环境要求

- [Bun](https://bun.sh/)。
- 已启动并完成数据库迁移的后端。

## 快速开始

在项目根目录安装依赖并启动前端开发服务器：

```bash
bun install
bun run dev
```

在浏览器打开 <http://localhost:5173/>。

先用 Docker Compose 启动 PostgreSQL，再在 `backend` 目录执行 `uv run bash scripts/prestart.sh` 和 `uv run fastapi dev`。完整流程见[开发指南](../development.md)。

若需由 FastAPI 提供构建后的前端，在 `frontend` 目录运行 `bun run build`，然后访问 `http://localhost:8000`。其他可用命令见 `frontend/package.json`。

## 移除前端的上游参考流程

如果今后明确决定只保留 API，可按以下流程调整；当前项目保留前端，此处仅说明模板做法。

- 删除 `./frontend` 目录。
- 删除 `backend/app/main.py` 中的 `app.frontend()` 调用。
- 删除 `backend/Dockerfile` 中的前端构建阶段及 `COPY --from=frontend-build` 指令。
- 删除 `compose.override.yml` 中的 `playwright` 服务。
- 删除 `.github/workflows/deploy.yml` 中的 **Set up Bun**、**Install frontend dependencies** 和 **Build frontend** 步骤。
- 删除 `.fastapicloudignore` 中的 `!backend/app/frontend/` 条目。

## 生成 API 客户端

### 自动生成

在项目根目录运行：

```bash
bash ./scripts/generate-client.sh
```

检查生成结果后，将变更纳入版本管理。

### 手动生成

确保后端正在运行。从 `http://localhost:8000/api/v1/openapi.json` 下载 OpenAPI JSON，保存为 `frontend/openapi.json`，然后在 `frontend` 目录执行：

```bash
bun run generate-client
```

检查并保存生成的变更。后端修改影响 OpenAPI 模式时，需要重新生成客户端。

## 使用远程 API

默认情况下，构建后的前端与 FastAPI 应用使用同源 API。通过 Vite 开发服务器访问远程 API 时，可在 `frontend/.env` 设置 API 地址：

```env
VITE_API_URL=https://my-domain.example.com
```

前端启动后会将该地址作为 API 基础地址。

## 代码结构

- `frontend/src`：前端主要代码。
- `frontend/public`：静态资源。
- `frontend/src/client`：自动生成的 OpenAPI 客户端。
- `frontend/src/components`：界面组件，`ui` 子目录存放 shadcn/ui 组件。
- `frontend/src/hooks`：自定义 Hooks。
- `frontend/src/lib`：共享工具函数。
- `frontend/src/routes`：页面与路由。

## 使用 Playwright 进行端到端测试

模板包含初始 Playwright 测试。先启动 Docker Compose 后端：

```bash
docker compose run --rm backend bash scripts/prestart.sh
docker compose up -d --wait backend
```

运行测试：

```bash
bunx playwright test
```

也可使用交互界面查看和操作测试浏览器：

```bash
bunx playwright test --ui
```

以下为上游测试环境清理命令，**会删除数据卷及其中的数据**，仅适用于可丢弃的测试环境：

```bash
docker compose down -v
```

需要更新测试时，在测试目录修改或新增测试文件。详细用法见 [Playwright 官方文档](https://playwright.dev/docs/intro)。当前用户如无 Docker socket 权限，需要在容器管理命令前使用 `sudo`。
