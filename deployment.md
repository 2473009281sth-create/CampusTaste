# FastAPI Cloud 部署参考

本文是上游模板部署说明的中文版本，介绍如何使用附带的 GitHub Actions 工作流部署至 [FastAPI Cloud](https://fastapicloud.com)。CampusTaste 当前仅完成本地阶段 0 验收，尚未验证或执行公网部署。

## 创建云应用

在 FastAPI Cloud 创建应用，将[应用目录](https://fastapicloud.com/docs/builds-and-deployments/application-directory/)设为 `backend`。

可通过 [Neon](https://fastapicloud.com/docs/integrations/neon-integration/) 或 [Supabase](https://fastapicloud.com/docs/integrations/supabase-integration/) 集成连接 PostgreSQL；两者都会自动配置 `DATABASE_URL` 密钥。使用其他 PostgreSQL 服务商时，也可手动设置连接地址。

## 配置应用

### 环境变量

在云应用中添加以下必需的[环境变量](https://fastapicloud.com/docs/builds-and-deployments/environment-variables/)：

- `PROJECT_NAME`：项目名称，用于 API 文档与邮件。
- `FIRST_SUPERUSER`：初始管理员邮箱。
- `FRONTEND_HOST`：应用的公网地址，例如自动生成的 `https://your-app.fastapicloud.dev` 或自定义域名。

启用邮件时，根据邮件服务商配置以下可选变量：

- `SMTP_HOST`
- `SMTP_USER`
- `EMAILS_FROM_EMAIL`

启用 Sentry 时配置 `SENTRY_DSN`。

### 密钥

添加以下必需值，并标记为密钥：

- `SECRET_KEY`：用于令牌签名的密钥。
- `FIRST_SUPERUSER_PASSWORD`：初始管理员密码。
- `DATABASE_URL`：PostgreSQL 连接地址；数据库集成可自动配置。

使用需要认证的邮件服务时，将 `SMTP_PASSWORD` 也设为密钥。

可使用以下命令分别生成 `SECRET_KEY` 和管理员密码：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 配置持续部署

模板的 `.github/workflows/deploy.yml` 在推送至 `master` 时构建前端、准备数据库并部署应用，也可从 **Actions** 页手动触发。CampusTaste 本地分支为 `main`，正式使用前需核对触发条件。

登录 FastAPI Cloud，并将[部署令牌](https://fastapicloud.com/docs/advanced-features/deploy-tokens/)及应用 ID 配置为 GitHub 仓库密钥：

```bash
uv run fastapi login
uv run fastapi cloud setup-ci --secrets-only --app-id <your-app-id>
```

如果 GitHub CLI 已安装且已认证，该命令会自动配置 `FASTAPI_CLOUD_TOKEN` 和 `FASTAPI_CLOUD_APP_ID`；否则会输出对应值，需在仓库 **Settings（设置） > Secrets and variables（密钥与变量） > Actions** 中手动添加。

工作流在部署前执行迁移并创建初始管理员。在上述设置页添加仓库变量：

- `PROJECT_NAME`
- `FIRST_SUPERUSER`

添加仓库密钥：

- `DATABASE_URL`
- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`

这些值应与云应用一致。数据库地址由服务商提供，并须允许 GitHub 托管运行器连接，以完成数据库准备步骤。

部署工作流依次执行：

1. 安装并构建前端，将产物写入 `backend/app/frontend`。
2. 执行 `backend/scripts/prestart.sh`，应用迁移并创建初始管理员。
3. 运行 `uv run fastapi deploy` 部署应用。

## 访问地址

将 `your-app.fastapicloud.dev` 替换为实际应用域名：

- 应用（前端和 API）：`https://your-app.fastapicloud.dev`。
- 交互文档：`https://your-app.fastapicloud.dev/docs`。

## Docker Compose 部署

部署到自有服务器时，参见 [Docker Compose 部署指南](deployment-docker-compose.md)。

## GitHub 仓库自动化

上游提供的仓库自动化使用以下 GitHub Apps：

- [Latest Changes](https://github.com/apps/latest-changes)：PR 合并后更新 `release-notes.md`。
- [PR Push](https://github.com/apps/pr-push)：允许提交前检查工作流向 PR 分支推送自动修复。
- [PR Submit](https://github.com/apps/pr-submit)：供 **Bump pre-commit hooks** 和 **Prepare Release** 工作流创建 PR。

使用 [Smokeshow](https://github.com/samuelcolvin/smokeshow) 发布覆盖率报告时，需添加仓库密钥 `SMOKESHOW_AUTH_KEY`。
