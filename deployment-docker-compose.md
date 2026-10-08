# Docker Compose 部署参考

本文为上游模板自托管部署说明的中文版本。可通过 Docker Compose 将项目部署到自有远程服务器，使用 Traefik 处理 HTTPS 与请求路由。CampusTaste 当前未执行该部署流程。

## 准备工作

- 准备可访问的远程服务器。
- 配置应用域名及所需辅助服务子域名的 DNS，使其指向服务器，例如 `fastapi-project.example.com` 和 `adminer.fastapi-project.example.com`。
- 在服务器安装并配置 [Docker Engine](https://docs.docker.com/engine/install/)。

## 复制代码

```bash
rsync -av --exclude=".git/" --filter=":- .gitignore" ./ root@your-server.example.com:/root/code/app/
```

`--filter=":- .gitignore"` 让 rsync 沿用 Git 忽略规则，排除虚拟环境等内容。CampusTaste 的真实 `.env` 同样被忽略，部署配置需单独提供。

## 配置应用

### 环境变量

设置域名、项目名称和初始管理员邮箱：

```bash
export DOMAIN=fastapi-project.example.com
export PROJECT_NAME="Full Stack FastAPI Project"
export FIRST_SUPERUSER=admin@example.com
```

按需配置：

- `SMTP_HOST`：邮件服务商提供的 SMTP 主机地址。
- `SMTP_USER`：SMTP 用户名。
- `EMAILS_FROM_EMAIL`：发件邮箱。
- `SENTRY_DSN`：Sentry 连接配置。

### 密钥

为数据库密码、令牌签名密钥及初始管理员密码生成独立随机值：

```bash
export POSTGRES_PASSWORD="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export FIRST_SUPERUSER_PASSWORD="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

使用需要认证的邮件服务时，还应设置 `SMTP_PASSWORD`。

## 部署

```bash
cd /root/code/app/
docker compose -f compose.yml -f compose.deploy.yml build
docker compose -f compose.yml -f compose.deploy.yml run --rm backend bash scripts/prestart.sh
docker compose -f compose.yml -f compose.deploy.yml up -d
```

`compose.deploy.yml` 在共享配置上添加 HTTPS 和自动证书管理。显式指定这两个文件后，不加载 `compose.override.yml` 的本地开发配置。

后端 Docker 镜像构建时会构建前端，因此服务器无需另装 Bun 或提前准备前端产物。

## 通过 GitHub Actions 部署

模板的 `.github/workflows/deploy-docker-compose.yml` 工作流支持从 GitHub Actions 手动触发，在服务器执行部署命令。

自托管运行器直接在主机执行工作流，应仅用于信任贡献者和工作流代码的仓库；上游说明建议用于私有仓库。

### 配置仓库变量与密钥

进入仓库 **Settings（设置） > Secrets and variables（密钥与变量） > Actions**，添加变量：

- `DOMAIN`
- `PROJECT_NAME`
- `FIRST_SUPERUSER`

启用邮件时添加可选变量：

- `SMTP_HOST`
- `SMTP_USER`
- `EMAILS_FROM_EMAIL`

启用 Sentry 时添加 `SENTRY_DSN`。

添加仓库密钥：

- `POSTGRES_PASSWORD`
- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`

邮件服务需要认证时，添加 `SMTP_PASSWORD`。

### 安装自托管运行器

在服务器创建专用用户并授予 Docker 访问权限：

```bash
sudo adduser github
sudo usermod -aG docker github
sudo su - github
```

进入 GitHub 仓库 **Settings > Actions > Runners**，选择 **New self-hosted runner（新建自托管运行器）** 与 Linux，按页面命令下载、配置并注册。安装目录使用 `/home/github/actions-runner`。

注册后退出 `github` 用户会话，将运行器安装为系统服务：

```bash
exit
cd /home/github/actions-runner
sudo ./svc.sh install github
sudo ./svc.sh start
sudo ./svc.sh status
```

参见 GitHub 的[添加自托管运行器](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)和[配置系统服务](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/configure-the-application?platform=linux)说明。

### 触发部署

运行器上线后，打开仓库 **Actions** 页，选择 **Deploy with Docker Compose** 工作流，再选择 **Run workflow（运行工作流）**。

## 访问地址

将 `fastapi-project.example.com` 替换为实际域名：

- 应用（前端与 API）：`https://fastapi-project.example.com`。
- 交互文档：`https://fastapi-project.example.com/docs`。
- Adminer：`https://adminer.fastapi-project.example.com`。
