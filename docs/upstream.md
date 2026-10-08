# 模板来源与归属

- 上游：https://github.com/fastapi/full-stack-fastapi-template
- 采用 master 提交：`cb740b656d7a0a6c5e12c7bf8e50343ec94ee9c7`。
- 获取日期：2026-09-23；通过临时目录浅克隆后导入文件，不携带上游 Git 历史。
- 许可证：MIT，Copyright (c) 2019 Sebastián Ramírez；根目录 LICENSE 原样保留。
- 原目录没有 Git 仓库，只有 `.vscode/extensions.json`；该文件原样保留。
- 未导入上游 `.agents/`、`.claude/` 助手技能配置，它们不是运行依赖。

## 原模板能力

用户注册、密码哈希、JWT Access Token、用户与 Item CRUD、找回密码、React 前端、SQLModel 模型、Alembic 迁移、pytest、Ruff、Compose、GitHub Actions 均来自上游，不属于本人从零实现。

当前关键结构：`backend/app/main.py` 挂载 API 和前端；`api/routes/` 路由；`api/deps.py` Session 与鉴权依赖；`crud.py` 数据操作；`models.py` User/Item 与输入输出模型；`core/` 配置、数据库、安全；`app/alembic/versions/` 五个迁移；`backend/tests/` 登录、用户、Item、开发辅助接口及 CRUD 测试。

## 阶段 0 本地调整

保留后端、前端、迁移及锁文件原样；本项目仅增加需求、路线、来源、验收文档，以及本地配置保护。上游默认跟踪 `.env`，此处改为 `.env.example` 保留无敏感信息的示例，根 `.env` 生成随机开发密钥、权限 0600，加入忽略规则。`.env`、`.venv/`、`.local/` 不应入库。development.md 已同步说明本项目忽略真实 .env、跟踪 .env.example 的做法。

当前本地 Git 分支 main，无提交、无远程配置。上游 Actions 沿用原配置，未执行；其 master 分支与默认 .env 假设后续需在工程化阶段调整，不能宣称 CI 已可用。没有推送、PR 或公网部署。

## 版本

沿用 `.python-version` 的 3.14（本地 uv 安装 3.14.6）及根 `uv.lock`，用 `uv sync --locked --project backend` 安装。锁定 FastAPI 0.141.1、Pydantic 2.13.4、SQLModel 0.0.39、SQLAlchemy 2.0.51、Alembic 1.19.1、psycopg 3.3.4、pytest 9.1.1、Ruff 0.16.4。Compose 使用 PostgreSQL 18；镜像标签沿用上游，未额外固定镜像摘要。前端保留 bun.lock，未安装或构建。

## 中文文档维护（2026-09-24）

根据用户要求，根 README、前后端 README、开发指南、两份部署指南、贡献指南及上游发布记录已翻译为中文。发布记录保留全部原有链接、版本标题和作者署名；贡献指南明确描述上游规则，部署指南明确属于未执行的参考流程。LICENSE 保持原文。pytest 自动生成的缓存说明不属于项目维护文档，保持工具原样。

中文说明同时适配本项目实际情况：本地 .env 不入库、测试使用独立数据库、明确 CI/前端尚未验证；修正上游后端 README 关于测试脚本透传 pytest 参数的说明。本次仅修改 Markdown，未改变业务代码、依赖或阶段范围。后续维护的 Markdown 文档继续使用中文，命令、路径和技术标识保留原文。
