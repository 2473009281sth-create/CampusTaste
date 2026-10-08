# 上游模板发布记录

本文翻译自采用提交的上游发布记录，保留版本、PR 链接与贡献者署名。历史条目反映当时的模板实现，不代表 CampusTaste 已实现或仍使用这些功能；当前项目进度见 [docs/roadmap.md](docs/roadmap.md)。

## 最新变更

### 修复

* 🐛 修复 Sonner 提示消息的主题同步。 PR [#2450](https://github.com/fastapi/full-stack-fastapi-template/pull/2450)，作者：[@chris-bs23](https://github.com/chris-bs23)。
* 🐛 为吸顶布局页头添加背景。 PR [#2384](https://github.com/fastapi/full-stack-fastapi-template/pull/2384)，作者：[@istoutjesdijk](https://github.com/istoutjesdijk)。

### 重构

* ♻️ 简化数据库就绪检查。 PR [#2460](https://github.com/fastapi/full-stack-fastapi-template/pull/2460)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✅ 简化密码重置端到端测试。 PR [#2453](https://github.com/fastapi/full-stack-fastapi-template/pull/2453)，作者：[@alejsdev](https://github.com/alejsdev)。
* 💄 重构邮件模板与组件，改进样式。 PR [#2451](https://github.com/fastapi/full-stack-fastapi-template/pull/2451)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 将本地邮件测试工具从 Mailcatcher 替换为 Mailpit。 PR [#2436](https://github.com/fastapi/full-stack-fastapi-template/pull/2436)，作者：[@alejsdev](https://github.com/alejsdev)。

### 文档

* 📝 在 README.md 中补充 Mailpit 和 React Email。 PR [#2452](https://github.com/fastapi/full-stack-fastapi-template/pull/2452)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 简化项目文档。 PR [#2442](https://github.com/fastapi/full-stack-fastapi-template/pull/2442)，作者：[@tiangolo](https://github.com/tiangolo)。

### 内部维护

* ⬆ 将 traefik 从 3.6 升级至 v3.7（docker-compose 分组）。 PR [#2465](https://github.com/fastapi/full-stack-fastapi-template/pull/2465)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新提交前钩子。 PR [#2471](https://github.com/fastapi/full-stack-fastapi-template/pull/2471)，作者：[@pr-submit[bot]](https://github.com/apps/pr-submit)。
* ⬆ 将 pwdlib[argon2,bcrypt] 的版本要求从 >=0.3.0 更新为 >=0.3.1。 PR [#2468](https://github.com/fastapi/full-stack-fastapi-template/pull/2468)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 sentry-sdk[fastapi] 的版本要求从 <3.0.0,>=2.66.1 更新为 >=2.68.1,<3.0.0。 PR [#2467](https://github.com/fastapi/full-stack-fastapi-template/pull/2467)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 python-packages 分组中的 4 项依赖。 PR [#2466](https://github.com/fastapi/full-stack-fastapi-template/pull/2466)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 github-actions 分组中的 4 项依赖。 PR [#2464](https://github.com/fastapi/full-stack-fastapi-template/pull/2464)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 Typer 最低版本提高至 `0.26.1`。 PR [#2459](https://github.com/fastapi/full-stack-fastapi-template/pull/2459)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* ⬆️ 将 setup-uv Action 更新至 10.0.1。 PR [#2458](https://github.com/fastapi/full-stack-fastapi-template/pull/2458)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。

## 0.12.0 (2026-08-12)

### 功能

* ☁️ 添加 FastAPI Cloud 部署支持。 PR [#2438](https://github.com/fastapi/full-stack-fastapi-template/pull/2438)，作者：[@tiangolo](https://github.com/tiangolo)。

### 修复

* 🐳 将前端资源纳入 Docker 构建上下文。 PR [#2440](https://github.com/fastapi/full-stack-fastapi-template/pull/2440)，作者：[@tiangolo](https://github.com/tiangolo)。

### 内部维护

* 👷 将自动标签功能迁移到 Latest Changes。 PR [#2439](https://github.com/fastapi/full-stack-fastapi-template/pull/2439)，作者：[@tiangolo](https://github.com/tiangolo)。

## 0.11.1 (2026-08-11)

### 重构

* ♻️ 简化 Docker Compose 部署。 PR [#2435](https://github.com/fastapi/full-stack-fastapi-template/pull/2435)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 改用 `DATABASE_URL`，替代分散的连接配置变量。 PR [#2184](https://github.com/fastapi/full-stack-fastapi-template/pull/2184)，作者：[@patrick91](https://github.com/patrick91)。

### 内部维护

* ⬆ 更新 npm-packages 分组中的 33 项依赖，涉及 1 个目录。 PR [#2433](https://github.com/fastapi/full-stack-fastapi-template/pull/2433)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。

## 0.11.0 (2026-08-11)

### 功能

* ✨ 引入 react-email 编写邮件模板。 PR [#2421](https://github.com/fastapi/full-stack-fastapi-template/pull/2421)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 使用 FastAPI 入口配置。 PR [#2360](https://github.com/fastapi/full-stack-fastapi-template/pull/2360)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 为 FastAPI 和 SQLModel 添加 library-skills。 PR [#2354](https://github.com/fastapi/full-stack-fastapi-template/pull/2354)，作者：[@tiangolo](https://github.com/tiangolo)。

### 修复

* ✅ 修复注册测试中的竞争问题。 PR [#2422](https://github.com/fastapi/full-stack-fastapi-template/pull/2422)，作者：[@tiangolo](https://github.com/tiangolo)。

### 重构

* ♻️ 移除 Copier 项目生成流程。 PR [#2430](https://github.com/fastapi/full-stack-fastapi-template/pull/2430)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 简化 CORS 配置。 PR [#2429](https://github.com/fastapi/full-stack-fastapi-template/pull/2429)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 使用 `FASTAPI_ENV` 控制开发模式。 PR [#2427](https://github.com/fastapi/full-stack-fastapi-template/pull/2427)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 在启动前显式准备数据库，不再依赖启动前自动钩子。 PR [#2426](https://github.com/fastapi/full-stack-fastapi-template/pull/2426)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 要求显式配置 SECRET_KEY。 PR [#2425](https://github.com/fastapi/full-stack-fastapi-template/pull/2425)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 简化 uv 工作区配置。 PR [#2423](https://github.com/fastapi/full-stack-fastapi-template/pull/2423)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 在 Compose 中使用 FastAPI 入口配置。 PR [#2420](https://github.com/fastapi/full-stack-fastapi-template/pull/2420)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 要求 Compose 配置值非空。 PR [#2418](https://github.com/fastapi/full-stack-fastapi-template/pull/2418)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 简化可选环境配置。 PR [#2417](https://github.com/fastapi/full-stack-fastapi-template/pull/2417)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 简化 Copier 环境配置。 PR [#2416](https://github.com/fastapi/full-stack-fastapi-template/pull/2416)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 简化环境默认值。 PR [#2415](https://github.com/fastapi/full-stack-fastapi-template/pull/2415)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 简化本地开发流程。 PR [#2414](https://github.com/fastapi/full-stack-fastapi-template/pull/2414)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 简化环境配置。 PR [#2413](https://github.com/fastapi/full-stack-fastapi-template/pull/2413)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 简化 Traefik 部署，将其纳入应用服务栈。 PR [#2412](https://github.com/fastapi/full-stack-fastapi-template/pull/2412)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 由 FastAPI 提供前端资源。 PR [#2393](https://github.com/fastapi/full-stack-fastapi-template/pull/2393)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 重构 PostgreSQL 环境变量配置。 PR [#2392](https://github.com/fastapi/full-stack-fastapi-template/pull/2392)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 重构模型，改进类型定义。 PR [#2356](https://github.com/fastapi/full-stack-fastapi-template/pull/2356)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 将 FastAPI VS Code 扩展加入推荐列表。 PR [#2206](https://github.com/fastapi/full-stack-fastapi-template/pull/2206)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 更新页面元信息标题。 PR [#2179](https://github.com/fastapi/full-stack-fastapi-template/pull/2179)，作者：[@alejsdev](https://github.com/alejsdev)。

### 升级

* ⬆️ 升级 FastAPI 版本。 PR [#2357](https://github.com/fastapi/full-stack-fastapi-template/pull/2357)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 将 Python 升级至 3.14。 PR [#2352](https://github.com/fastapi/full-stack-fastapi-template/pull/2352)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 升级 Sentry 和 FastAPI。 PR [#2181](https://github.com/fastapi/full-stack-fastapi-template/pull/2181)，作者：[@patrick91](https://github.com/patrick91)。

### 文档

* 📝 移除过时的本地域名设置说明。 PR [#2428](https://github.com/fastapi/full-stack-fastapi-template/pull/2428)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 明确环境配置说明。 PR [#2419](https://github.com/fastapi/full-stack-fastapi-template/pull/2419)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 改进 README 截图的替代文本。 PR [#2359](https://github.com/fastapi/full-stack-fastapi-template/pull/2359)，作者：[@Bmowville](https://github.com/Bmowville)。
* ✏️ 修复 .env 中 DOMAIN 注释的拼写错误。 PR [#2305](https://github.com/fastapi/full-stack-fastapi-template/pull/2305)，作者：[@serhiiur](https://github.com/serhiiur)。
* 📝 更新安全政策。 PR [#2297](https://github.com/fastapi/full-stack-fastapi-template/pull/2297)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 添加 `CONTRIBUTING.md`。 PR [#2159](https://github.com/fastapi/full-stack-fastapi-template/pull/2159)，作者：[@alejsdev](https://github.com/alejsdev)。

### 内部维护

* 👷 添加自动发布流程。 PR [#2431](https://github.com/fastapi/full-stack-fastapi-template/pull/2431)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 移除旧标签检查。 PR [#2424](https://github.com/fastapi/full-stack-fastapi-template/pull/2424)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔐 使用 PR Submit 创建拉取请求。 PR [#2411](https://github.com/fastapi/full-stack-fastapi-template/pull/2411)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 使用 GitHub CLI 进行 Git 认证。 PR [#2410](https://github.com/fastapi/full-stack-fastapi-template/pull/2410)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 使用 PR Push 的提交身份。 PR [#2409](https://github.com/fastapi/full-stack-fastapi-template/pull/2409)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔒 使用 PR Push 替代提交前检查的个人访问令牌。 PR [#2407](https://github.com/fastapi/full-stack-fastapi-template/pull/2407)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 将 `@hey-api/openapi-ts` 从 0.73.0 升级至 0.97.3 and migrate to new client。 PR [#2388](https://github.com/fastapi/full-stack-fastapi-template/pull/2388)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* 🔥 移除旧的 Latest Changes 工作流。 PR [#2403](https://github.com/fastapi/full-stack-fastapi-template/pull/2403)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆ 将 psycopg[binary] 的版本要求从 <4.0.0,>=3.1.13 更新为 >=3.3.4,<4.0.0。 PR [#2399](https://github.com/fastapi/full-stack-fastapi-template/pull/2399)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 github-actions 分组中的 5 项依赖。 PR [#2397](https://github.com/fastapi/full-stack-fastapi-template/pull/2397)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 sentry-sdk[fastapi] 的版本要求从 <3.0.0,>=2.63.0 更新为 >=2.66.1,<3.0.0。 PR [#2400](https://github.com/fastapi/full-stack-fastapi-template/pull/2400)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 python-packages 分组中的 3 项依赖。 PR [#2398](https://github.com/fastapi/full-stack-fastapi-template/pull/2398)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 改进私有仓库工作流。 PR [#2394](https://github.com/fastapi/full-stack-fastapi-template/pull/2394)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 将 latest-changes 升级至 0.7.1。 PR [#2389](https://github.com/fastapi/full-stack-fastapi-template/pull/2389)，作者：[@tiangolo](https://github.com/tiangolo)。
* 将 axios 从 1.16.0 升级至 1.18.0（位置或分组：/frontend）。 PR [#2386](https://github.com/fastapi/full-stack-fastapi-template/pull/2386)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新提交前钩子。 PR [#2382](https://github.com/fastapi/full-stack-fastapi-template/pull/2382)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆ 更新 python-packages 分组中的 2 项依赖，涉及 1 个目录。 PR [#2380](https://github.com/fastapi/full-stack-fastapi-template/pull/2380)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 sentry-sdk[fastapi] 的版本要求从 <3.0.0,>=2.0.0 更新为 >=2.63.0,<3.0.0。 PR [#2373](https://github.com/fastapi/full-stack-fastapi-template/pull/2373)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 github-actions 分组中的 5 项依赖，涉及 1 个目录。 PR [#2379](https://github.com/fastapi/full-stack-fastapi-template/pull/2379)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 添加更新提交前钩子版本的 GitHub 工作流。 PR [#2363](https://github.com/fastapi/full-stack-fastapi-template/pull/2363)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* 🔧 将 Dependabot 检查周期设置为每月。 PR [#2364](https://github.com/fastapi/full-stack-fastapi-template/pull/2364)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* ⬆ 更新 npm-packages 分组中的 37 项依赖，涉及 1 个目录。 PR [#2333](https://github.com/fastapi/full-stack-fastapi-template/pull/2333)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 更新 latest-changes。 PR [#2375](https://github.com/fastapi/full-stack-fastapi-template/pull/2375)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆ 将 playwright 从 v1.58.2-noble 升级至 v1.61.1-noble（位置或分组：/frontend in the docker group across 1 directory）。 PR [#2361](https://github.com/fastapi/full-stack-fastapi-template/pull/2361)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 issue-manager 更新至 0.8.1。 PR [#2368](https://github.com/fastapi/full-stack-fastapi-template/pull/2368)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆ 将 emails 从 0.6 升级至 1.1.2（位置或分组：the python-packages group across 1 directory）。 PR [#2369](https://github.com/fastapi/full-stack-fastapi-template/pull/2369)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 https://github.com/crate-ci/typos 从 v1.46.0 升级至 1.47.2（位置或分组：the pre-commit group across 1 directory）。 PR [#2343](https://github.com/fastapi/full-stack-fastapi-template/pull/2343)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/checkout 从 6.0.3 升级至 7.0.0（位置或分组：the github-actions）。 PR [#2362](https://github.com/fastapi/full-stack-fastapi-template/pull/2362)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 latest-changes 更新至 0.6.1。 PR [#2367](https://github.com/fastapi/full-stack-fastapi-template/pull/2367)，作者：[@tiangolo](https://github.com/tiangolo)。
* ➕ 将 prek 移入顶层依赖。 PR [#2353](https://github.com/fastapi/full-stack-fastapi-template/pull/2353)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 对 pyproject.toml 的键排序。 PR [#2350](https://github.com/fastapi/full-stack-fastapi-template/pull/2350)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 简化拉取请求工作流触发条件。 PR [#2349](https://github.com/fastapi/full-stack-fastapi-template/pull/2349)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 将 issue-manager 更新至 0.7.1。 PR [#2348](https://github.com/fastapi/full-stack-fastapi-template/pull/2348)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 将 issue-manager 更新至 0.7.0。 PR [#2347](https://github.com/fastapi/full-stack-fastapi-template/pull/2347)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔒️ 更新 zizmor 工作流安全检查。 PR [#2345](https://github.com/fastapi/full-stack-fastapi-template/pull/2345)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 添加检查拼写错误的提交前钩子。 PR [#2317](https://github.com/fastapi/full-stack-fastapi-template/pull/2317)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* 将 form-data 从 4.0.5 升级至 4.0.6（位置或分组：/frontend）。 PR [#2337](https://github.com/fastapi/full-stack-fastapi-template/pull/2337)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 starlette 从 1.0.1 升级至 1.3.1。 PR [#2338](https://github.com/fastapi/full-stack-fastapi-template/pull/2338)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 python-packages 分组中的 16 项依赖，涉及 1 个目录。 PR [#2340](https://github.com/fastapi/full-stack-fastapi-template/pull/2340)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 github-actions 分组中的 2 项依赖。 PR [#2332](https://github.com/fastapi/full-stack-fastapi-template/pull/2332)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pyjwt 从 2.12.0 升级至 2.13.0。 PR [#2336](https://github.com/fastapi/full-stack-fastapi-template/pull/2336)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pytest 从 7.4.4 升级至 9.0.3。 PR [#2330](https://github.com/fastapi/full-stack-fastapi-template/pull/2330)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 axios 从 1.13.5 升级至 1.16.0（位置或分组：/frontend）。 PR [#2323](https://github.com/fastapi/full-stack-fastapi-template/pull/2323)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 lxml 从 6.0.2 升级至 6.1.0。 PR [#2266](https://github.com/fastapi/full-stack-fastapi-template/pull/2266)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 mako 从 1.3.10 升级至 1.3.12。 PR [#2278](https://github.com/fastapi/full-stack-fastapi-template/pull/2278)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pygments 从 2.19.2 升级至 2.20.0。 PR [#2248](https://github.com/fastapi/full-stack-fastapi-template/pull/2248)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 requests 从 2.32.5 升级至 2.33.0。 PR [#2245](https://github.com/fastapi/full-stack-fastapi-template/pull/2245)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 python-dotenv 从 1.2.1 升级至 1.2.2。 PR [#2265](https://github.com/fastapi/full-stack-fastapi-template/pull/2265)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 starlette 从 0.46.2 升级至 1.0.1。 PR [#2322](https://github.com/fastapi/full-stack-fastapi-template/pull/2322)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 github-actions 分组中的 6 项依赖，涉及 1 个目录。 PR [#2326](https://github.com/fastapi/full-stack-fastapi-template/pull/2326)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 配置 Dependabot 分组更新并每周检查。 PR [#2293](https://github.com/fastapi/full-stack-fastapi-template/pull/2293)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* 🔥 移除已集中到 GitHub 仓库的配置文件。 PR [#2300](https://github.com/fastapi/full-stack-fastapi-template/pull/2300)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆ 将 actions/add-to-project 从 1.0.2 升级至 2.0.0。 PR [#2273](https://github.com/fastapi/full-stack-fastapi-template/pull/2273)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 python-multipart 从 0.0.21 升级至 0.0.27。 PR [#2277](https://github.com/fastapi/full-stack-fastapi-template/pull/2277)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 idna 从 3.11 升级至 3.15。 PR [#2294](https://github.com/fastapi/full-stack-fastapi-template/pull/2294)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔒️ 仅允许团队成员修改依赖。 PR [#2292](https://github.com/fastapi/full-stack-fastapi-template/pull/2292)，作者：[@svlandeg](https://github.com/svlandeg)。
* ⬆ 将 urllib3 从 2.6.3 升级至 2.7.0。 PR [#2282](https://github.com/fastapi/full-stack-fastapi-template/pull/2282)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔒️ 添加 zizmor 并修复审计发现的问题。 PR [#2260](https://github.com/fastapi/full-stack-fastapi-template/pull/2260)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* 🔒 使用提交 SHA 固定 GitHub Actions 版本。 PR [#2246](https://github.com/fastapi/full-stack-fastapi-template/pull/2246)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* 🔨 添加提交前钩子，确保最新发布标题包含日期。 PR [#2205](https://github.com/fastapi/full-stack-fastapi-template/pull/2205)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* 👷 将 `ty` 加入提交前检查。 PR [#2227](https://github.com/fastapi/full-stack-fastapi-template/pull/2227)，作者：[@svlandeg](https://github.com/svlandeg)。
* ⬆ 将 dorny/paths-filter 从 3 升级至 4。 PR [#2230](https://github.com/fastapi/full-stack-fastapi-template/pull/2230)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pyjwt 从 2.10.1 升级至 2.12.0。 PR [#2231](https://github.com/fastapi/full-stack-fastapi-template/pull/2231)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 25.3.2 升级至 25.5.0。 PR [#2233](https://github.com/fastapi/full-stack-fastapi-template/pull/2233)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-devtools 从 1.159.10 升级至 1.166.7。 PR [#2234](https://github.com/fastapi/full-stack-fastapi-template/pull/2234)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 tailwindcss 从 4.2.0 升级至 4.2.1。 PR [#2226](https://github.com/fastapi/full-stack-fastapi-template/pull/2226)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/download-artifact 从 7 升级至 8。 PR [#2208](https://github.com/fastapi/full-stack-fastapi-template/pull/2208)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/upload-artifact 从 6 升级至 7。 PR [#2207](https://github.com/fastapi/full-stack-fastapi-template/pull/2207)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router 从 1.157.3 升级至 1.163.3。 PR [#2215](https://github.com/fastapi/full-stack-fastapi-template/pull/2215)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router-devtools 从 1.159.10 升级至 1.163.3。 PR [#2212](https://github.com/fastapi/full-stack-fastapi-template/pull/2212)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query 从 5.90.20 升级至 5.90.21。 PR [#2213](https://github.com/fastapi/full-stack-fastapi-template/pull/2213)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 25.1.0 升级至 25.3.2。 PR [#2214](https://github.com/fastapi/full-stack-fastapi-template/pull/2214)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 tailwindcss 从 4.1.18 升级至 4.2.0。 PR [#2198](https://github.com/fastapi/full-stack-fastapi-template/pull/2198)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 axios 从 1.13.4 升级至 1.13.5。 PR [#2199](https://github.com/fastapi/full-stack-fastapi-template/pull/2199)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @vitejs/plugin-react-swc 从 4.2.2 升级至 4.2.3。 PR [#2200](https://github.com/fastapi/full-stack-fastapi-template/pull/2200)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 dotenv 从 17.2.3 升级至 17.3.1。 PR [#2185](https://github.com/fastapi/full-stack-fastapi-template/pull/2185)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-devtools 从 1.157.17 升级至 1.159.10。 PR [#2186](https://github.com/fastapi/full-stack-fastapi-template/pull/2186)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router-devtools 从 1.157.17 升级至 1.159.10。 PR [#2188](https://github.com/fastapi/full-stack-fastapi-template/pull/2188)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 biome schema version 从 2.3.12 升级至 2.3.14。 PR [#2178](https://github.com/fastapi/full-stack-fastapi-template/pull/2178)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 @biomejs/biome 从 2.3.12 升级至 2.3.14。 PR [#2177](https://github.com/fastapi/full-stack-fastapi-template/pull/2177)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 lucide-react 从 0.562.0 升级至 0.563.0。 PR [#2176](https://github.com/fastapi/full-stack-fastapi-template/pull/2176)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query 从 5.90.19 升级至 5.90.20。 PR [#2174](https://github.com/fastapi/full-stack-fastapi-template/pull/2174)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 playwright 从 v1.58.0-noble 升级至 v1.58.2-noble（位置或分组：/frontend）。 PR [#2175](https://github.com/fastapi/full-stack-fastapi-template/pull/2175)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 通过提交前钩子运行 mypy。 PR [#2169](https://github.com/fastapi/full-stack-fastapi-template/pull/2169)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* ⬆ 将 @tanstack/router-devtools 从 1.153.2 升级至 1.157.17。 PR [#2166](https://github.com/fastapi/full-stack-fastapi-template/pull/2166)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 25.0.10 升级至 25.1.0。 PR [#2168](https://github.com/fastapi/full-stack-fastapi-template/pull/2168)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 axios 从 1.13.2 升级至 1.13.4。 PR [#2164](https://github.com/fastapi/full-stack-fastapi-template/pull/2164)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 更新 biome.json 中的配置模式版本为 2.3.12。 PR [#2154](https://github.com/fastapi/full-stack-fastapi-template/pull/2154)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 @biomejs/biome 从 2.3.11 升级至 2.3.12。 PR [#2153](https://github.com/fastapi/full-stack-fastapi-template/pull/2153)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 playwright 从 v1.57.0-noble 升级至 v1.58.0-noble（位置或分组：/frontend）。 PR [#2150](https://github.com/fastapi/full-stack-fastapi-template/pull/2150)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router 从 1.153.2 升级至 1.156.0。 PR [#2152](https://github.com/fastapi/full-stack-fastapi-template/pull/2152)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 zod 从 4.3.5 升级至 4.3.6。 PR [#2151](https://github.com/fastapi/full-stack-fastapi-template/pull/2151)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 25.0.9 升级至 25.0.10。 PR [#2149](https://github.com/fastapi/full-stack-fastapi-template/pull/2149)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router-devtools 从 1.153.2 升级至 1.156.0。 PR [#2147](https://github.com/fastapi/full-stack-fastapi-template/pull/2147)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。

## 0.10.0 (2026-01-23)

### 功能

* ✅ 添加 Item 和管理员测试，并重构现有测试。 PR [#2146](https://github.com/fastapi/full-stack-fastapi-template/pull/2146)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 为 User 和 Item 模型添加 created_at 字段并更新接口。 PR [#2144](https://github.com/fastapi/full-stack-fastapi-template/pull/2144)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 从 npm 迁移至 Bun。 PR [#2097](https://github.com/fastapi/full-stack-fastapi-template/pull/2097)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 配置 Node 单仓库多包结构。 PR [#2095](https://github.com/fastapi/full-stack-fastapi-template/pull/2095)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🧑‍💻 引入 uv 工作区。 PR [#2090](https://github.com/fastapi/full-stack-fastapi-template/pull/2090)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 添加推荐的 VS Code 扩展。 PR [#1386](https://github.com/fastapi/full-stack-fastapi-template/pull/1386)，作者：[@tobiase](https://github.com/tobiase)。
* ✨ 默认使用 pwdlib 和 Argon2，并添加自动升级旧 Bcrypt 密码哈希的逻辑及测试。 PR [#2104](https://github.com/fastapi/full-stack-fastapi-template/pull/2104)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔨 在提交前生成前端 SDK，移除专用工作流。 PR [#2111](https://github.com/fastapi/full-stack-fastapi-template/pull/2111)，作者：[@tiangolo](https://github.com/tiangolo)。

### 修复

* 🐛 在管理员路由增加用户认证检查，限制非管理员访问。 PR [#2145](https://github.com/fastapi/full-stack-fastapi-template/pull/2145)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛 在 `read_user_by_id` 中处理不存在的用户 ID。 PR [#1396](https://github.com/fastapi/full-stack-fastapi-template/pull/1396)，作者：[@saltie2193](https://github.com/saltie2193)。

### 重构

* 🔥 从推荐扩展中移除已由 Python 扩展包含的 debugpy。 PR [#2143](https://github.com/fastapi/full-stack-fastapi-template/pull/2143)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 根据新的顶层目录结构更新生产环境前端构建上下文。 PR [#2108](https://github.com/fastapi/full-stack-fastapi-template/pull/2108)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🚚 将 Docker Compose 文件改为 `compose.yml` 等新名称。 PR [#2106](https://github.com/fastapi/full-stack-fastapi-template/pull/2106)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔒️ 使认证处理耗时保持一致，避免用户枚举攻击。 PR [#2105](https://github.com/fastapi/full-stack-fastapi-template/pull/2105)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✅ 修复单元测试中错误的模拟方式（问题 #1780）。 PR [#1781](https://github.com/fastapi/full-stack-fastapi-template/pull/1781)，作者：[@vicaya](https://github.com/vicaya)。
* 🐛更新 `items.py`，权限不足时返回 `403`。 PR [#1543](https://github.com/fastapi/full-stack-fastapi-template/pull/1543)，作者：[@jpizquierdo](https://github.com/jpizquierdo)。
* ✅ 在 `test_user.py` 中使用正确的 `is_active` 字段。 PR [#1479](https://github.com/fastapi/full-stack-fastapi-template/pull/1479)，作者：[@nauanbek](https://github.com/nauanbek)。
* ♻️ 删除重复代码，简化密码重置逻辑。 PR [#1440](https://github.com/fastapi/full-stack-fastapi-template/pull/1440)，作者：[@youneshenniwrites](https://github.com/youneshenniwrites)。

### 升级

* ⬆ 将 postgres 从 17 升级至 18。 PR [#1910](https://github.com/fastapi/full-stack-fastapi-template/pull/1910)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 traefik 从 3.0 升级至 3.6。 PR [#1973](https://github.com/fastapi/full-stack-fastapi-template/pull/1973)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。

### 文档

* 📝 更新部署文档。 PR [#2109](https://github.com/fastapi/full-stack-fastapi-template/pull/2109)，作者：[@tiangolo](https://github.com/tiangolo)。

### 内部维护

* 🎨 格式化 Python 脚本测试。 PR [#2112](https://github.com/fastapi/full-stack-fastapi-template/pull/2112)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔨 更新 generate-client.sh 及文档。 PR [#2110](https://github.com/fastapi/full-stack-fastapi-template/pull/2110)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔥 移除未使用的旧脚本。 PR [#2107](https://github.com/fastapi/full-stack-fastapi-template/pull/2107)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 为 issue-manager 添加 `maybe-ai` 标签配置。 PR [#2103](https://github.com/fastapi/full-stack-fastapi-template/pull/2103)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 将 Dockerfile 中的 uv 更新为 0.9.26。 PR [#2102](https://github.com/fastapi/full-stack-fastapi-template/pull/2102)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 lucide-react 从 0.556.0 升级至 0.562.0。 PR [#2101](https://github.com/fastapi/full-stack-fastapi-template/pull/2101)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 更新 Dependabot 的包生态配置。 PR [#2100](https://github.com/fastapi/full-stack-fastapi-template/pull/2100)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 将 Biome 配置模式版本更新为 2.3.11。 PR [#2099](https://github.com/fastapi/full-stack-fastapi-template/pull/2099)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 在 `package.json` 中添加测试脚本。 PR [#2098](https://github.com/fastapi/full-stack-fastapi-template/pull/2098)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🎨 应用提交前检查修复。 PR [#2055](https://github.com/fastapi/full-stack-fastapi-template/pull/2055)，作者：[@GniLudio](https://github.com/GniLudio)。
* 👷 更新提交前检查工作流。 PR [#2096](https://github.com/fastapi/full-stack-fastapi-template/pull/2096)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 更新 biome.json 配置模式版本。 PR [#2092](https://github.com/fastapi/full-stack-fastapi-template/pull/2092)，作者：[@alejsdev](https://github.com/alejsdev)。
* 撤销“将 pre-commit-config.yaml 中的 ruff format 改用 --check”的修改。 PR [#2091](https://github.com/fastapi/full-stack-fastapi-template/pull/2091)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 将 pre-commit-config.yaml 中的 ruff format 改用 --check。 PR [#2077](https://github.com/fastapi/full-stack-fastapi-template/pull/2077)，作者：[@ryansydnor](https://github.com/ryansydnor)。
* ⬆ 将 actions/checkout 从 5 升级至 6。 PR [#2074](https://github.com/fastapi/full-stack-fastapi-template/pull/2074)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 添加提交前检查工作流。 PR [#2056](https://github.com/fastapi/full-stack-fastapi-template/pull/2056)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* ⬆ 将 @tanstack/router-devtools 从 1.140.0 升级至 1.142.8（位置或分组：/frontend）。 PR [#2060](https://github.com/fastapi/full-stack-fastapi-template/pull/2060)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router 从 1.141.2 升级至 1.142.8（位置或分组：/frontend）。 PR [#2062](https://github.com/fastapi/full-stack-fastapi-template/pull/2062)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @biomejs/biome 从 2.3.8 升级至 2.3.10（位置或分组：/frontend）。 PR [#2061](https://github.com/fastapi/full-stack-fastapi-template/pull/2061)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router-devtools 从 1.139.12 升级至 1.142.8（位置或分组：/frontend）。 PR [#2063](https://github.com/fastapi/full-stack-fastapi-template/pull/2063)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 zod 从 4.1.13 升级至 4.2.1（位置或分组：/frontend）。 PR [#2064](https://github.com/fastapi/full-stack-fastapi-template/pull/2064)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 配置覆盖率；主要测试失败时立即报告，不等待 Smokeshow。 PR [#2054](https://github.com/fastapi/full-stack-fastapi-template/pull/2054)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* 👷 始终运行 Smokeshow，包括测试失败时。 PR [#2053](https://github.com/fastapi/full-stack-fastapi-template/pull/2053)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* ⬆ 将 @tanstack/react-router 从 1.140.0 升级至 1.141.2（位置或分组：/frontend）。 PR [#2045](https://github.com/fastapi/full-stack-fastapi-template/pull/2045)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/download-artifact 从 6 升级至 7。 PR [#2051](https://github.com/fastapi/full-stack-fastapi-template/pull/2051)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/upload-artifact 从 5 升级至 6。 PR [#2050](https://github.com/fastapi/full-stack-fastapi-template/pull/2050)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 24.10.1 升级至 25.0.2（位置或分组：/frontend）。 PR [#2048](https://github.com/fastapi/full-stack-fastapi-template/pull/2048)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tailwindcss/vite 从 4.1.17 升级至 4.1.18（位置或分组：/frontend）。 PR [#2049](https://github.com/fastapi/full-stack-fastapi-template/pull/2049)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 vite 从 7.2.7 升级至 7.3.0（位置或分组：/frontend）。 PR [#2047](https://github.com/fastapi/full-stack-fastapi-template/pull/2047)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 react-dom 从 19.2.1 升级至 19.2.3（位置或分组：/frontend）。 PR [#2046](https://github.com/fastapi/full-stack-fastapi-template/pull/2046)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。

## 0.9.0 (2025-12-08)

### 功能

* ✨ 为所有页面添加元信息标题支持。 PR [#2039](https://github.com/fastapi/full-stack-fastapi-template/pull/2039)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🛂 将前端迁移至 Shadcn。 PR [#2010](https://github.com/fastapi/full-stack-fastapi-template/pull/2010)，作者：[@alejsdev](https://github.com/alejsdev)。

### 修复

* 🐛 将 `EMAILS_FROM_NAME` 类型从 `EmailStr` 修正为 `str`。 PR [#1940](https://github.com/fastapi/full-stack-fastapi-template/pull/1940)，作者：[@martin0258](https://github.com/martin0258)。
* 🐛 使 `parse_cors` 对空字符串和空列表的处理保持一致。 PR [#1672](https://github.com/fastapi/full-stack-fastapi-template/pull/1672)，作者：[@rolkotaki](https://github.com/rolkotaki)。
* 🐛 用户选择菜单项后关闭侧边抽屉。 PR [#1515](https://github.com/fastapi/full-stack-fastapi-template/pull/1515)，作者：[@dtellz](https://github.com/dtellz)。
* 🐛 修复编辑用户字段时要求填写密码的校验问题。 PR [#1508](https://github.com/fastapi/full-stack-fastapi-template/pull/1508)，作者：[@jpizquierdo](https://github.com/jpizquierdo)。

### 重构

* ♻️ 更新密码最大长度。 PR [#1447](https://github.com/fastapi/full-stack-fastapi-template/pull/1447)，作者：[@michaelAlvarino](https://github.com/michaelAlvarino)。
* 🚚 将后端测试移至 `app` 目录之外。 PR [#1862](https://github.com/fastapi/full-stack-fastapi-template/pull/1862)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* ✨ 为 Vite 环境变量添加 ImportMetaEnv 和 ImportMeta 接口。 PR [#1860](https://github.com/fastapi/full-stack-fastapi-template/pull/1860)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 更新 `tsconfig.json` 并修复错误。 PR [#1859](https://github.com/fastapi/full-stack-fastapi-template/pull/1859)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 移除 ChangePassword 组件保存按钮的 disabled 属性。 PR [#1844](https://github.com/fastapi/full-stack-fastapi-template/pull/1844)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷🏻‍♀️  更新客户端生成的 CI 流程。 PR [#1573](https://github.com/fastapi/full-stack-fastapi-template/pull/1573)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 移除继承类中的冗余字段。 PR [#1520](https://github.com/fastapi/full-stack-fastapi-template/pull/1520)，作者：[@tzway](https://github.com/tzway)。
* 🎨 微调骨架屏及其他组件的界面。 PR [#1507](https://github.com/fastapi/full-stack-fastapi-template/pull/1507)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🎨 微调界面。 PR [#1506](https://github.com/fastapi/full-stack-fastapi-template/pull/1506)，作者：[@alejsdev](https://github.com/alejsdev)。

### 升级

* ⬆ 将 @types/react 从 19.1.12 升级至 19.1.13（位置或分组：/frontend）。 PR [#1888](https://github.com/fastapi/full-stack-fastapi-template/pull/1888)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-plugin 从 1.131.41 升级至 1.131.43（位置或分组：/frontend）。 PR [#1887](https://github.com/fastapi/full-stack-fastapi-template/pull/1887)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pydantic 从 2.11.7 升级至 2.11.9（位置或分组：/backend）。 PR [#1891](https://github.com/fastapi/full-stack-fastapi-template/pull/1891)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @chakra-ui/react 从 3.26.0 升级至 3.27.0（位置或分组：/frontend）。 PR [#1890](https://github.com/fastapi/full-stack-fastapi-template/pull/1890)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 axios 从 1.12.0 升级至 1.12.2（位置或分组：/frontend）。 PR [#1889](https://github.com/fastapi/full-stack-fastapi-template/pull/1889)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 24.3.1 升级至 24.4.0（位置或分组：/frontend）。 PR [#1886](https://github.com/fastapi/full-stack-fastapi-template/pull/1886)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-devtools 从 1.131.41 升级至 1.131.42（位置或分组：/frontend）。 PR [#1881](https://github.com/fastapi/full-stack-fastapi-template/pull/1881)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-plugin 从 1.131.39 升级至 1.131.41（位置或分组：/frontend）。 PR [#1879](https://github.com/fastapi/full-stack-fastapi-template/pull/1879)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query-devtools 从 5.87.3 升级至 5.87.4（位置或分组：/frontend）。 PR [#1876](https://github.com/fastapi/full-stack-fastapi-template/pull/1876)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 axios 从 1.11.0 升级至 1.12.0（位置或分组：/frontend）。 PR [#1878](https://github.com/fastapi/full-stack-fastapi-template/pull/1878)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-devtools 从 1.131.40 升级至 1.131.41（位置或分组：/frontend）。 PR [#1877](https://github.com/fastapi/full-stack-fastapi-template/pull/1877)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router 从 1.131.40 升级至 1.131.41（位置或分组：/frontend）。 PR [#1875](https://github.com/fastapi/full-stack-fastapi-template/pull/1875)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-devtools 从 1.131.36 升级至 1.131.37（位置或分组：/frontend）。 PR [#1871](https://github.com/fastapi/full-stack-fastapi-template/pull/1871)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-plugin 从 1.131.36 升级至 1.131.37（位置或分组：/frontend）。 PR [#1870](https://github.com/fastapi/full-stack-fastapi-template/pull/1870)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query 从 5.87.1 升级至 5.87.4（位置或分组：/frontend）。 PR [#1868](https://github.com/fastapi/full-stack-fastapi-template/pull/1868)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @biomejs/biome 从 2.2.3 升级至 2.2.4（位置或分组：/frontend）。 PR [#1869](https://github.com/fastapi/full-stack-fastapi-template/pull/1869)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router 从 1.131.36 升级至 1.131.37（位置或分组：/frontend）。 PR [#1872](https://github.com/fastapi/full-stack-fastapi-template/pull/1872)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 Biome 升级至最新版本。 PR [#1861](https://github.com/fastapi/full-stack-fastapi-template/pull/1861)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆️ 更新 TanStack Router 依赖。 PR [#1853](https://github.com/fastapi/full-stack-fastapi-template/pull/1853)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆️ 将 @tanstack/react-query 从 5.28.14 升级至 5.87.1。 PR [#1852](https://github.com/fastapi/full-stack-fastapi-template/pull/1852)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 @chakra-ui/react 从 3.8.0 升级至 3.26.0（位置或分组：/frontend）。 PR [#1796](https://github.com/fastapi/full-stack-fastapi-template/pull/1796)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 更新 @hey-api/openapi-ts 版本及 Dependabot 配置。 PR [#1845](https://github.com/fastapi/full-stack-fastapi-template/pull/1845)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆️ 更新 Playwright。 PR [#1793](https://github.com/fastapi/full-stack-fastapi-template/pull/1793)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆️ 升级 React 及相关依赖。 PR [#1843](https://github.com/fastapi/full-stack-fastapi-template/pull/1843)，作者：[@alejsdev](https://github.com/alejsdev)。

### 文档

* 📝 添加使用 Mailcatcher 进行本地邮件测试的配置说明。 PR [#2038](https://github.com/fastapi/full-stack-fastapi-template/pull/2038)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 在 `README` 中添加 Vite 链接。 PR [#2037](https://github.com/fastapi/full-stack-fastapi-template/pull/2037)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 修复过时的工作流徽章。 PR [#2028](https://github.com/fastapi/full-stack-fastapi-template/pull/2028)，作者：[@AymanAlSuleihi](https://github.com/AymanAlSuleihi)。
* 📝 更新文档。 PR [#2036](https://github.com/fastapi/full-stack-fastapi-template/pull/2036)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✏️ 修复 `deployment.md` 的拼写错误。 PR [#1679](https://github.com/fastapi/full-stack-fastapi-template/pull/1679)，作者：[@cassmtnr](https://github.com/cassmtnr)。

### 内部维护

* 🔥 移除未使用的依赖。 PR [#2035](https://github.com/fastapi/full-stack-fastapi-template/pull/2035)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 react-dom 从 19.2.0 升级至 19.2.1（位置或分组：/frontend）。 PR [#2032](https://github.com/fastapi/full-stack-fastapi-template/pull/2032)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 vite 从 7.2.6 升级至 7.2.7（位置或分组：/frontend）。 PR [#2033](https://github.com/fastapi/full-stack-fastapi-template/pull/2033)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-plugin 从 1.139.12 升级至 1.140.0（位置或分组：/frontend）。 PR [#2034](https://github.com/fastapi/full-stack-fastapi-template/pull/2034)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 lucide-react 从 0.555.0 升级至 0.556.0（位置或分组：/frontend）。 PR [#2031](https://github.com/fastapi/full-stack-fastapi-template/pull/2031)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 在 Biome 配置中支持 Tailwind CSS 指令。 PR [#2029](https://github.com/fastapi/full-stack-fastapi-template/pull/2029)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 react-hook-form 从 7.66.1 升级至 7.67.0（位置或分组：/frontend）。 PR [#2018](https://github.com/fastapi/full-stack-fastapi-template/pull/2018)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query 从 5.90.10 升级至 5.90.11（位置或分组：/frontend）。 PR [#2019](https://github.com/fastapi/full-stack-fastapi-template/pull/2019)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 axios 从 1.12.2 升级至 1.13.2（位置或分组：/frontend）。 PR [#2020](https://github.com/fastapi/full-stack-fastapi-template/pull/2020)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-devtools 从 1.139.3 升级至 1.139.12（位置或分组：/frontend）。 PR [#2021](https://github.com/fastapi/full-stack-fastapi-template/pull/2021)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 playwright 从 v1.56.1-noble 升级至 v1.57.0-noble（位置或分组：/frontend）。 PR [#2016](https://github.com/fastapi/full-stack-fastapi-template/pull/2016)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 更新 `biome.json` 配置模式版本。 PR [#2017](https://github.com/fastapi/full-stack-fastapi-template/pull/2017)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 vite 从 7.2.2 升级至 7.2.6（位置或分组：/frontend）。 PR [#2015](https://github.com/fastapi/full-stack-fastapi-template/pull/2015)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @biomejs/biome 从 2.3.7 升级至 2.3.8（位置或分组：/frontend）。 PR [#2014](https://github.com/fastapi/full-stack-fastapi-template/pull/2014)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query-devtools 从 5.91.0 升级至 5.91.1（位置或分组：/frontend）。 PR [#2013](https://github.com/fastapi/full-stack-fastapi-template/pull/2013)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-plugin 从 1.133.15 升级至 1.139.12（位置或分组：/frontend）。 PR [#2012](https://github.com/fastapi/full-stack-fastapi-template/pull/2012)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 form-data 从 4.0.4 升级至 4.0.5（位置或分组：/frontend）。 PR [#2011](https://github.com/fastapi/full-stack-fastapi-template/pull/2011)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/checkout 从 5 升级至 6。 PR [#2007](https://github.com/fastapi/full-stack-fastapi-template/pull/2007)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/react 从 19.2.2 升级至 19.2.7（位置或分组：/frontend）。 PR [#2003](https://github.com/fastapi/full-stack-fastapi-template/pull/2003)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-devtools 从 1.131.42 升级至 1.139.3（位置或分组：/frontend）。 PR [#2001](https://github.com/fastapi/full-stack-fastapi-template/pull/2001)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 typescript 从 5.9.2 升级至 5.9.3（位置或分组：/frontend）。 PR [#2002](https://github.com/fastapi/full-stack-fastapi-template/pull/2002)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/react-dom 从 19.2.2 升级至 19.2.3（位置或分组：/frontend）。 PR [#2004](https://github.com/fastapi/full-stack-fastapi-template/pull/2004)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 24.10.0 升级至 24.10.1（位置或分组：/frontend）。 PR [#2005](https://github.com/fastapi/full-stack-fastapi-template/pull/2005)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pydantic-settings 从 2.11.0 升级至 2.12.0（位置或分组：/backend）。 PR [#2000](https://github.com/fastapi/full-stack-fastapi-template/pull/2000)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 alembic 从 1.17.1 升级至 1.17.2（位置或分组：/backend）。 PR [#1999](https://github.com/fastapi/full-stack-fastapi-template/pull/1999)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @biomejs/biome 从 2.2.4 升级至 2.3.7（位置或分组：/frontend）。 PR [#1998](https://github.com/fastapi/full-stack-fastapi-template/pull/1998)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 react-hook-form 从 7.66.0 升级至 7.66.1（位置或分组：/frontend）。 PR [#1997](https://github.com/fastapi/full-stack-fastapi-template/pull/1997)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @vitejs/plugin-react-swc 从 4.2.1 升级至 4.2.2（位置或分组：/frontend）。 PR [#1996](https://github.com/fastapi/full-stack-fastapi-template/pull/1996)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @chakra-ui/react 从 3.29.0 升级至 3.30.0（位置或分组：/frontend）。 PR [#1995](https://github.com/fastapi/full-stack-fastapi-template/pull/1995)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query-devtools 从 5.90.2 升级至 5.91.0（位置或分组：/frontend）。 PR [#1994](https://github.com/fastapi/full-stack-fastapi-template/pull/1994)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 为 Dependabot 更新添加标签。 PR [#1992](https://github.com/fastapi/full-stack-fastapi-template/pull/1992)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 dotenv 从 17.2.2 升级至 17.2.3（位置或分组：/frontend）。 PR [#1957](https://github.com/fastapi/full-stack-fastapi-template/pull/1957)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @chakra-ui/react 从 3.27.0 升级至 3.29.0（位置或分组：/frontend）。 PR [#1974](https://github.com/fastapi/full-stack-fastapi-template/pull/1974)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/react-dom 从 19.2.1 升级至 19.2.2（位置或分组：/frontend）。 PR [#1975](https://github.com/fastapi/full-stack-fastapi-template/pull/1975)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query 从 5.90.2 升级至 5.90.7（位置或分组：/frontend）。 PR [#1976](https://github.com/fastapi/full-stack-fastapi-template/pull/1976)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 vite 从 7.1.11 升级至 7.2.2（位置或分组：/frontend）。 PR [#1977](https://github.com/fastapi/full-stack-fastapi-template/pull/1977)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pydantic 从 2.12.3 升级至 2.12.4（位置或分组：/backend）。 PR [#1978](https://github.com/fastapi/full-stack-fastapi-template/pull/1978)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 js-yaml 从 4.1.0 升级至 4.1.1（位置或分组：/frontend）。 PR [#1983](https://github.com/fastapi/full-stack-fastapi-template/pull/1983)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/checkout 从 5 升级至 6。 PR [#1988](https://github.com/fastapi/full-stack-fastapi-template/pull/1988)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 升级 `latest-changes` GitHub Action 并固定 `actions/checkout@v5`。 PR [#2006](https://github.com/fastapi/full-stack-fastapi-template/pull/2006)，作者：[@svlandeg](https://github.com/svlandeg)。
* ⬆ 将 @vitejs/plugin-react-swc 从 4.1.0 升级至 4.2.0（位置或分组：/frontend）。 PR [#1958](https://github.com/fastapi/full-stack-fastapi-template/pull/1958)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/download-artifact 从 5 升级至 6。 PR [#1959](https://github.com/fastapi/full-stack-fastapi-template/pull/1959)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 24.5.2 升级至 24.9.1（位置或分组：/frontend）。 PR [#1961](https://github.com/fastapi/full-stack-fastapi-template/pull/1961)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/upload-artifact 从 4 升级至 5。 PR [#1962](https://github.com/fastapi/full-stack-fastapi-template/pull/1962)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 react-hook-form 从 7.62.0 升级至 7.65.0（位置或分组：/frontend）。 PR [#1964](https://github.com/fastapi/full-stack-fastapi-template/pull/1964)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 alembic 从 1.17.0 升级至 1.17.1（位置或分组：/backend）。 PR [#1970](https://github.com/fastapi/full-stack-fastapi-template/pull/1970)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 修复 issue-manager 提醒配置。 PR [#1972](https://github.com/fastapi/full-stack-fastapi-template/pull/1972)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆ 将 @vitejs/plugin-react-swc 从 4.0.1 升级至 4.1.0（位置或分组：/frontend）。 PR [#1897](https://github.com/fastapi/full-stack-fastapi-template/pull/1897)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 playwright 从 v1.55.0-noble 升级至 v1.56.1-noble（位置或分组：/frontend）。 PR [#1943](https://github.com/fastapi/full-stack-fastapi-template/pull/1943)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 为 `issue-manager` 的 `waiting` 标签配置提醒。 PR [#1939](https://github.com/fastapi/full-stack-fastapi-template/pull/1939)，作者：[@YuriiMotov](https://github.com/YuriiMotov)。
* ⬆ 将 vite 从 7.1.9 升级至 7.1.11（位置或分组：/frontend）。 PR [#1949](https://github.com/fastapi/full-stack-fastapi-template/pull/1949)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pydantic 从 2.11.10 升级至 2.12.3（位置或分组：/backend）。 PR [#1947](https://github.com/fastapi/full-stack-fastapi-template/pull/1947)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 更新 /frontend 中的 react-dom 和 @types/react-dom。 PR [#1934](https://github.com/fastapi/full-stack-fastapi-template/pull/1934)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 alembic 从 1.16.5 升级至 1.17.0（位置或分组：/backend）。 PR [#1935](https://github.com/fastapi/full-stack-fastapi-template/pull/1935)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/setup-node 从 5 升级至 6。 PR [#1937](https://github.com/fastapi/full-stack-fastapi-template/pull/1937)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-plugin 从 1.132.41 升级至 1.133.15（位置或分组：/frontend）。 PR [#1946](https://github.com/fastapi/full-stack-fastapi-template/pull/1946)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 astral-sh/setup-uv 从 6 升级至 7。 PR [#1925](https://github.com/fastapi/full-stack-fastapi-template/pull/1925)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 vite 从 7.1.7 升级至 7.1.9（位置或分组：/frontend）。 PR [#1919](https://github.com/fastapi/full-stack-fastapi-template/pull/1919)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/router-plugin 从 1.131.44 升级至 1.132.41（位置或分组：/frontend）。 PR [#1920](https://github.com/fastapi/full-stack-fastapi-template/pull/1920)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query-devtools 从 5.87.4 升级至 5.90.2（位置或分组：/frontend）。 PR [#1921](https://github.com/fastapi/full-stack-fastapi-template/pull/1921)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pydantic 从 2.11.9 升级至 2.11.10（位置或分组：/backend）。 PR [#1922](https://github.com/fastapi/full-stack-fastapi-template/pull/1922)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 tiangolo/issue-manager 从 0.5.1 升级至 0.6.0。 PR [#1912](https://github.com/fastapi/full-stack-fastapi-template/pull/1912)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/react 从 19.1.13 升级至 19.1.15（位置或分组：/frontend）。 PR [#1906](https://github.com/fastapi/full-stack-fastapi-template/pull/1906)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pydantic-settings 从 2.10.1 升级至 2.11.0（位置或分组：/backend）。 PR [#1907](https://github.com/fastapi/full-stack-fastapi-template/pull/1907)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query 从 5.90.1 升级至 5.90.2（位置或分组：/frontend）。 PR [#1905](https://github.com/fastapi/full-stack-fastapi-template/pull/1905)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 24.4.0 升级至 24.5.2（位置或分组：/frontend）。 PR [#1903](https://github.com/fastapi/full-stack-fastapi-template/pull/1903)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 vite 从 7.1.5 升级至 7.1.7（位置或分组：/frontend）。 PR [#1893](https://github.com/fastapi/full-stack-fastapi-template/pull/1893)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query 从 5.87.4 升级至 5.90.1（位置或分组：/frontend）。 PR [#1896](https://github.com/fastapi/full-stack-fastapi-template/pull/1896)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-router 从 1.131.44 升级至 1.131.50（位置或分组：/frontend）。 PR [#1894](https://github.com/fastapi/full-stack-fastapi-template/pull/1894)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 将 uv 和 npm 依赖的 Dependabot 更新周期设为每周。 PR [#1880](https://github.com/fastapi/full-stack-fastapi-template/pull/1880)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 pydantic 从 2.9.2 升级至 2.11.7（位置或分组：/backend）。 PR [#1864](https://github.com/fastapi/full-stack-fastapi-template/pull/1864)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 更新覆盖率配置并简化测试脚本。 PR [#1867](https://github.com/fastapi/full-stack-fastapi-template/pull/1867)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 在 Ruff 中启用 T201 规则，禁止 print 语句。 PR [#1865](https://github.com/fastapi/full-stack-fastapi-template/pull/1865)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 @tanstack/react-query-devtools 从 5.87.1 升级至 5.87.3（位置或分组：/frontend）。 PR [#1863](https://github.com/fastapi/full-stack-fastapi-template/pull/1863)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 vite 从 6.3.4 升级至 7.1.5（位置或分组：/frontend）。 PR [#1857](https://github.com/fastapi/full-stack-fastapi-template/pull/1857)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 22.15.3 升级至 24.3.1（位置或分组：/frontend）。 PR [#1854](https://github.com/fastapi/full-stack-fastapi-template/pull/1854)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @vitejs/plugin-react-swc 从 3.9.0 升级至 4.0.1（位置或分组：/frontend）。 PR [#1856](https://github.com/fastapi/full-stack-fastapi-template/pull/1856)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 axios 从 1.9.0 升级至 1.11.0（位置或分组：/frontend）。 PR [#1855](https://github.com/fastapi/full-stack-fastapi-template/pull/1855)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 alembic 从 1.15.2 升级至 1.16.5（位置或分组：/backend）。 PR [#1847](https://github.com/fastapi/full-stack-fastapi-template/pull/1847)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 email-validator 从 2.2.0 升级至 2.3.0（位置或分组：/backend）。 PR [#1850](https://github.com/fastapi/full-stack-fastapi-template/pull/1850)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pydantic-settings 从 2.9.1 升级至 2.10.1（位置或分组：/backend）。 PR [#1851](https://github.com/fastapi/full-stack-fastapi-template/pull/1851)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 react-error-boundary 从 5.0.0 升级至 6.0.0（位置或分组：/frontend）。 PR [#1849](https://github.com/fastapi/full-stack-fastapi-template/pull/1849)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query-devtools 从 5.74.9 升级至 5.87.1（位置或分组：/frontend）。 PR [#1848](https://github.com/fastapi/full-stack-fastapi-template/pull/1848)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 dotenv 从 16.4.5 升级至 17.2.2（位置或分组：/frontend）。 PR [#1846](https://github.com/fastapi/full-stack-fastapi-template/pull/1846)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 node 从 20 升级至 24（位置或分组：/frontend）。 PR [#1621](https://github.com/fastapi/full-stack-fastapi-template/pull/1621)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/labeler 从 5 升级至 6。 PR [#1839](https://github.com/fastapi/full-stack-fastapi-template/pull/1839)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/setup-python 从 5 升级至 6。 PR [#1835](https://github.com/fastapi/full-stack-fastapi-template/pull/1835)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/setup-node 从 4 升级至 5。 PR [#1836](https://github.com/fastapi/full-stack-fastapi-template/pull/1836)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 自动检测 PR 合并冲突并添加标签。 PR [#1838](https://github.com/fastapi/full-stack-fastapi-template/pull/1838)，作者：[@svlandeg](https://github.com/svlandeg)。
* 🔧 添加前端静态检查提交前钩子。 PR [#1791](https://github.com/fastapi/full-stack-fastapi-template/pull/1791)，作者：[@alexrockhill](https://github.com/alexrockhill)。
* ⬆ 将 form-data 从 4.0.2 升级至 4.0.4（位置或分组：/frontend）。 PR [#1725](https://github.com/fastapi/full-stack-fastapi-template/pull/1725)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/checkout 从 4 升级至 5。 PR [#1768](https://github.com/fastapi/full-stack-fastapi-template/pull/1768)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/download-artifact 从 4 升级至 5。 PR [#1754](https://github.com/fastapi/full-stack-fastapi-template/pull/1754)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 tiangolo/latest-changes 从 0.3.2 升级至 0.4.0。 PR [#1744](https://github.com/fastapi/full-stack-fastapi-template/pull/1744)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 bcrypt 从 4.0.1 升级至 4.3.0（位置或分组：/backend）。 PR [#1601](https://github.com/fastapi/full-stack-fastapi-template/pull/1601)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 react-error-boundary 从 4.0.13 升级至 5.0.0（位置或分组：/frontend）。 PR [#1602](https://github.com/fastapi/full-stack-fastapi-template/pull/1602)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 vite 从 6.3.3 升级至 6.3.4（位置或分组：/frontend）。 PR [#1608](https://github.com/fastapi/full-stack-fastapi-template/pull/1608)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @playwright/test 从 1.45.2 升级至 1.52.0（位置或分组：/frontend）。 PR [#1586](https://github.com/fastapi/full-stack-fastapi-template/pull/1586)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pydantic-settings 从 2.5.2 升级至 2.9.1（位置或分组：/backend）。 PR [#1589](https://github.com/fastapi/full-stack-fastapi-template/pull/1589)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 next-themes 从 0.4.4 升级至 0.4.6（位置或分组：/frontend）。 PR [#1598](https://github.com/fastapi/full-stack-fastapi-template/pull/1598)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @types/node 从 20.10.5 升级至 22.15.3（位置或分组：/frontend）。 PR [#1599](https://github.com/fastapi/full-stack-fastapi-template/pull/1599)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @tanstack/react-query-devtools 从 5.28.14 升级至 5.74.9（位置或分组：/frontend）。 PR [#1597](https://github.com/fastapi/full-stack-fastapi-template/pull/1597)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 sqlmodel 从 0.0.22 升级至 0.0.24（位置或分组：/backend）。 PR [#1596](https://github.com/fastapi/full-stack-fastapi-template/pull/1596)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 python-multipart 从 0.0.10 升级至 0.0.20（位置或分组：/backend）。 PR [#1595](https://github.com/fastapi/full-stack-fastapi-template/pull/1595)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 alembic 从 1.13.2 升级至 1.15.2（位置或分组：/backend）。 PR [#1594](https://github.com/fastapi/full-stack-fastapi-template/pull/1594)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 postgres 从 12 升级至 17。 PR [#1580](https://github.com/fastapi/full-stack-fastapi-template/pull/1580)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 axios 从 1.8.2 升级至 1.9.0（位置或分组：/frontend）。 PR [#1592](https://github.com/fastapi/full-stack-fastapi-template/pull/1592)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 react-icons 从 5.4.0 升级至 5.5.0（位置或分组：/frontend）。 PR [#1581](https://github.com/fastapi/full-stack-fastapi-template/pull/1581)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 jinja2 从 3.1.4 升级至 3.1.6（位置或分组：/backend）。 PR [#1591](https://github.com/fastapi/full-stack-fastapi-template/pull/1591)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 pyjwt 从 2.9.0 升级至 2.10.1（位置或分组：/backend）。 PR [#1588](https://github.com/fastapi/full-stack-fastapi-template/pull/1588)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 httpx 从 0.27.2 升级至 0.28.1（位置或分组：/backend）。 PR [#1587](https://github.com/fastapi/full-stack-fastapi-template/pull/1587)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 form-data 从 4.0.0 升级至 4.0.2（位置或分组：/frontend）。 PR [#1578](https://github.com/fastapi/full-stack-fastapi-template/pull/1578)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 @biomejs/biome 从 1.6.1 升级至 1.9.4（位置或分组：/frontend）。 PR [#1582](https://github.com/fastapi/full-stack-fastapi-template/pull/1582)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 Dependabot 的 Python uv 更新目标设为后端目录。 PR [#1577](https://github.com/fastapi/full-stack-fastapi-template/pull/1577)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 更新 Dependabot 配置。 PR [#1576](https://github.com/fastapi/full-stack-fastapi-template/pull/1576)，作者：[@alejsdev](https://github.com/alejsdev)。
* 将 @babel/runtime 从 7.23.9 升级至 7.27.0（位置或分组：/frontend）。 PR [#1570](https://github.com/fastapi/full-stack-fastapi-template/pull/1570)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 更新 /frontend 中的 esbuild、@vitejs/plugin-react-swc 和 vite。 PR [#1571](https://github.com/fastapi/full-stack-fastapi-template/pull/1571)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 将 axios 从 1.7.4 升级至 1.8.2（位置或分组：/frontend）。 PR [#1568](https://github.com/fastapi/full-stack-fastapi-template/pull/1568)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 astral-sh/setup-uv 从 5 升级至 6。 PR [#1566](https://github.com/fastapi/full-stack-fastapi-template/pull/1566)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧  为 Dependabot 添加 npm 和 Docker 包生态。 PR [#1535](https://github.com/fastapi/full-stack-fastapi-template/pull/1535)，作者：[@alejsdev](https://github.com/alejsdev)。

## 0.8.0 (2025-02-19)

### 功能

* 🛂 迁移至 Chakra UI v3。 PR [#1496](https://github.com/fastapi/full-stack-fastapi-template/pull/1496)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加仅限本地使用的私有 API，供端到端测试使用。 PR [#1429](https://github.com/fastapi/full-stack-fastapi-template/pull/1429)，作者：[@patrick91](https://github.com/patrick91)。
* ✨ 迁移至最新 openapi-ts。 PR [#1430](https://github.com/fastapi/full-stack-fastapi-template/pull/1430)，作者：[@patrick91](https://github.com/patrick91)。

### 修复

* 🧑‍🔧 修正 htmlFor 的值。 PR [#1456](https://github.com/fastapi/full-stack-fastapi-template/pull/1456)，作者：[@wesenbergg](https://github.com/wesenbergg)。

### 重构

* ♻️ 收到 401/403 时将用户重定向至 `login`。 PR [#1501](https://github.com/fastapi/full-stack-fastapi-template/pull/1501)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛 重构密码重置测试，创建普通用户而非使用管理员。 PR [#1499](https://github.com/fastapi/full-stack-fastapi-template/pull/1499)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 将 `config.py` 中的邮箱类型由 `str` 改为 `EmailStr`。 PR [#1492](https://github.com/fastapi/full-stack-fastapi-template/pull/1492)，作者：[@jpizquierdo](https://github.com/jpizquierdo)。
* 🔧 移除创建路由器时未使用的上下文。 PR [#1498](https://github.com/fastapi/full-stack-fastapi-template/pull/1498)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 利用级联删除移除冗余的 Item 删除代码。 PR [#1481](https://github.com/fastapi/full-stack-fastapi-template/pull/1481)，作者：[@nauanbek](https://github.com/nauanbek)。
* ✏️ 修复几处拼写错误。 PR [#1485](https://github.com/fastapi/full-stack-fastapi-template/pull/1485)，作者：[@rjmunro](https://github.com/rjmunro)。
* 🎨 将 `prefix` 和 `tags` 移至路由器配置。 PR [#1439](https://github.com/fastapi/full-stack-fastapi-template/pull/1439)，作者：[@patrick91](https://github.com/patrick91)。
* ♻️ 使用 openapi-ts 配置替代修改 ID 的脚本。 PR [#1434](https://github.com/fastapi/full-stack-fastapi-template/pull/1434)，作者：[@patrick91](https://github.com/patrick91)。
* 👷 通过分片并行、Docker 缓存和环境变量提升 Playwright CI 速度。 PR [#1405](https://github.com/fastapi/full-stack-fastapi-template/pull/1405)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 添加 PaginationFooter 组件。 PR [#1381](https://github.com/fastapi/full-stack-fastapi-template/pull/1381)，作者：[@saltie2193](https://github.com/saltie2193)。
* ♻️ 重构代码，统一从配置读取加密算法名称。 PR [#1160](https://github.com/fastapi/full-stack-fastapi-template/pull/1160)，作者：[@sameeramin](https://github.com/sameeramin)。
* 🔊 默认启用邮件工具日志。 PR [#1374](https://github.com/fastapi/full-stack-fastapi-template/pull/1374)，作者：[@ihmily](https://github.com/ihmily)。
* 🔧 添加 `ENV PYTHONUNBUFFERED=1`，直接输出 Docker 日志。 PR [#1378](https://github.com/fastapi/full-stack-fastapi-template/pull/1378)，作者：[@tiangolo](https://github.com/tiangolo)。
* 💡 移除不必要的注释。 PR [#1260](https://github.com/fastapi/full-stack-fastapi-template/pull/1260)，作者：[@sebhani](https://github.com/sebhani)。

### 升级

* ⬆️ 更新 Dockerfile，使用 uv 0.5.11。 PR [#1454](https://github.com/fastapi/full-stack-fastapi-template/pull/1454)，作者：[@alejsdev](https://github.com/alejsdev)。

### 文档

* 📝 移除已弃用的手动客户端 SDK 步骤。 PR [#1494](https://github.com/fastapi/full-stack-fastapi-template/pull/1494)，作者：[@chandy](https://github.com/chandy)。
* 📝 更新前端 README.md。 PR [#1462](https://github.com/fastapi/full-stack-fastapi-template/pull/1462)，作者：[@getmarkus](https://github.com/getmarkus)。
* 📝 在 `frontend/README.md` 中说明移除前端时也应移除 Playwright。 PR [#1452](https://github.com/fastapi/full-stack-fastapi-template/pull/1452)，作者：[@youben11](https://github.com/youben11)。
* 📝 更新 `deployment.md`，说明在非 root 虚拟机中安装 GitHub Runner。 PR [#1412](https://github.com/fastapi/full-stack-fastapi-template/pull/1412)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 在 `development.md` 中添加 MailCatcher。 PR [#1387](https://github.com/fastapi/full-stack-fastapi-template/pull/1387)，作者：[@tobiase](https://github.com/tobiase)。

### 内部维护

* 🔧 配置路径别名，简化导入。 PR [#1497](https://github.com/fastapi/full-stack-fastapi-template/pull/1497)，作者：[@alejsdev](https://github.com/alejsdev)。
* 将 vite 从 5.0.13 升级至 5.4.14（位置或分组：/frontend）。 PR [#1469](https://github.com/fastapi/full-stack-fastapi-template/pull/1469)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 astral-sh/setup-uv 从 4 升级至 5。 PR [#1453](https://github.com/fastapi/full-stack-fastapi-template/pull/1453)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 astral-sh/setup-uv 从 3 升级至 4。 PR [#1433](https://github.com/fastapi/full-stack-fastapi-template/pull/1433)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 tiangolo/latest-changes 从 0.3.1 升级至 0.3.2。 PR [#1418](https://github.com/fastapi/full-stack-fastapi-template/pull/1418)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 更新 issue-manager 工作流。 PR [#1398](https://github.com/fastapi/full-stack-fastapi-template/pull/1398)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷 修复 Smokeshow，在 CI 中检出文件。 PR [#1395](https://github.com/fastapi/full-stack-fastapi-template/pull/1395)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 更新 `labeler.yml`。 PR [#1388](https://github.com/fastapi/full-stack-fastapi-template/pull/1388)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 将 Playwright 的 .auth 目录加入 `.gitignore`。 PR [#1383](https://github.com/fastapi/full-stack-fastapi-template/pull/1383)，作者：[@justin-p](https://github.com/justin-p)。
* ⬆️ 将 rollup 从 4.6.1 升级至 4.22.5（位置或分组：/frontend）。 PR [#1379](https://github.com/fastapi/full-stack-fastapi-template/pull/1379)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 astral-sh/setup-uv 从 2 升级至 3。 PR [#1364](https://github.com/fastapi/full-stack-fastapi-template/pull/1364)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
*  👷 更新提交前 end-of-file-fixer 钩子，排除 email-templates。 PR [#1296](https://github.com/fastapi/full-stack-fastapi-template/pull/1296)，作者：[@goabonga](https://github.com/goabonga)。
* ⬆ 将 tiangolo/issue-manager 从 0.5.0 升级至 0.5.1。 PR [#1332](https://github.com/fastapi/full-stack-fastapi-template/pull/1332)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 使用运行 Copier 的同一 Python 环境执行任务。 PR [#1157](https://github.com/fastapi/full-stack-fastapi-template/pull/1157)，作者：[@waketzheng](https://github.com/waketzheng)。
* 👷 调整客户端生成流程，出现错误时失败退出。 PR [#1377](https://github.com/fastapi/full-stack-fastapi-template/pull/1377)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 仅对同仓库 PR 生成并提交客户端，对 fork 仓库显示错误。 PR [#1376](https://github.com/fastapi/full-stack-fastapi-template/pull/1376)，作者：[@tiangolo](https://github.com/tiangolo)。

## 0.7.1 (2024-09-27)

### 主要变化

* 从 Poetry 迁移至 [`uv`](https://github.com/astral-sh/uv)。
* 简化并改进 Docker Compose 文件及 Traefik Dockerfile。
* API 使用 `api.example.com`，前端使用 `dashboard.example.com`，以便按需分别部署。
* Compose 后端和前端改用与本地开发服务器相同的端口，切换运行方式时无需修改前端配置。

### 功能

* 🩺 添加数据库健康检查。 PR [#1342](https://github.com/fastapi/full-stack-fastapi-template/pull/1342)，作者：[@tiangolo](https://github.com/tiangolo)。

### 重构

* ♻️ 更新配置，使用顶层 `.env` 文件。 PR [#1359](https://github.com/fastapi/full-stack-fastapi-template/pull/1359)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 从 Poetry 迁移至 uv。 PR [#1356](https://github.com/fastapi/full-stack-fastapi-template/pull/1356)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔥 移除开发依赖和 Jupyter 的特殊逻辑，上游未记录且已不再使用该做法。 PR [#1355](https://github.com/fastapi/full-stack-fastapi-template/pull/1355)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 使用 Docker Compose `watch`。 PR [#1354](https://github.com/fastapi/full-stack-fastapi-template/pull/1354)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 使用官方基础 Python Docker 镜像。 PR [#1351](https://github.com/fastapi/full-stack-fastapi-template/pull/1351)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🚚 调整脚本位置，简化目录结构。 PR [#1352](https://github.com/fastapi/full-stack-fastapi-template/pull/1352)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 重构启动前迁移，将其移至独立容器。 PR [#1350](https://github.com/fastapi/full-stack-fastapi-template/pull/1350)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 默认将 `FRONTEND_HOST` 纳入 CORS 来源。 PR [#1348](https://github.com/fastapi/full-stack-fastapi-template/pull/1348)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 使用 `api.example.com` 和 `dashboard.example.com` 简化域名，并改善 localhost 开发体验。 PR [#1344](https://github.com/fastapi/full-stack-fastapi-template/pull/1344)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔥 简化 Traefik，移除增加复杂度的 www 重定向。 PR [#1343](https://github.com/fastapi/full-stack-fastapi-template/pull/1343)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔥 支持 Mac 上的 Arm Docker 镜像，移除旧补丁。 PR [#1341](https://github.com/fastapi/full-stack-fastapi-template/pull/1341)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 移除 ItemCreate 模型中的重复信息。 PR [#1287](https://github.com/fastapi/full-stack-fastapi-template/pull/1287)，作者：[@jjaakko](https://github.com/jjaakko)。

### 升级

* ⬆️ 升级 FastAPI。 PR [#1349](https://github.com/fastapi/full-stack-fastapi-template/pull/1349)，作者：[@tiangolo](https://github.com/tiangolo)。

### 文档

* 💡 在 Dockerfile 注释中添加 uv 参考说明。 PR [#1357](https://github.com/fastapi/full-stack-fastapi-template/pull/1357)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 在 `backend/README.md` 中添加邮件模板说明。 PR [#1311](https://github.com/fastapi/full-stack-fastapi-template/pull/1311)，作者：[@alejsdev](https://github.com/alejsdev)。

### 内部维护

* 👷 停止同步标签，避免覆盖手动添加的标签。 PR [#1307](https://github.com/fastapi/full-stack-fastapi-template/pull/1307)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 在 GitHub Actions 中使用 uv 缓存。 PR [#1366](https://github.com/fastapi/full-stack-fastapi-template/pull/1366)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 更新 GitHub Actions 格式。 PR [#1363](https://github.com/fastapi/full-stack-fastapi-template/pull/1363)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 使用 `uv` 管理的 Python 环境生成客户端。 PR [#1362](https://github.com/fastapi/full-stack-fastapi-template/pull/1362)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 在 uv 管理的 Python 环境中运行测试，不再从 Docker 容器运行。 PR [#1361](https://github.com/fastapi/full-stack-fastapi-template/pull/1361)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔨 更新 `generate-client.sh`，修复生成逻辑并在错误时退出。 PR [#1360](https://github.com/fastapi/full-stack-fastapi-template/pull/1360)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 添加独立于测试的后端静态检查 GitHub Actions 工作流。 PR [#1358](https://github.com/fastapi/full-stack-fastapi-template/pull/1358)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 改进 Playwright CI 作业。 PR [#1335](https://github.com/fastapi/full-stack-fastapi-template/pull/1335)，作者：[@patrick91](https://github.com/patrick91)。
* 👷 更新 `issue-manager.yml`。 PR [#1329](https://github.com/fastapi/full-stack-fastapi-template/pull/1329)，作者：[@tiangolo](https://github.com/tiangolo)。
* 💚 使用 upload-artifact 时将 `include-hidden-files` 设为 `True`。 PR [#1327](https://github.com/fastapi/full-stack-fastapi-template/pull/1327)，作者：[@svlandeg](https://github.com/svlandeg)。
* 👷🏻 自动生成前端客户端。 PR [#1320](https://github.com/fastapi/full-stack-fastapi-template/pull/1320)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛 修复 `.github/labeler.yml`。 PR [#1322](https://github.com/fastapi/full-stack-fastapi-template/pull/1322)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷 更新 `.github/labeler.yml`。 PR [#1321](https://github.com/fastapi/full-stack-fastapi-template/pull/1321)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷 更新 `latest-changes` GitHub Action。 PR [#1315](https://github.com/fastapi/full-stack-fastapi-template/pull/1315)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 更新 labeler 配置。 PR [#1308](https://github.com/fastapi/full-stack-fastapi-template/pull/1308)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 更新 labeler，使其只添加一个标签。 PR [#1304](https://github.com/fastapi/full-stack-fastapi-template/pull/1304)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 将 axios 从 1.6.2 升级至 1.7.4（位置或分组：/frontend）。 PR [#1301](https://github.com/fastapi/full-stack-fastapi-template/pull/1301)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 更新 labeler GitHub Action 依赖。 PR [#1302](https://github.com/fastapi/full-stack-fastapi-template/pull/1302)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 更新 labeler GitHub Action 权限。 PR [#1300](https://github.com/fastapi/full-stack-fastapi-template/pull/1300)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 添加 label-checker GitHub Action。 PR [#1299](https://github.com/fastapi/full-stack-fastapi-template/pull/1299)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 添加 labeler GitHub Action。 PR [#1298](https://github.com/fastapi/full-stack-fastapi-template/pull/1298)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 添加 add-to-project GitHub Action。 PR [#1297](https://github.com/fastapi/full-stack-fastapi-template/pull/1297)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 更新 issue-manager。 PR [#1288](https://github.com/fastapi/full-stack-fastapi-template/pull/1288)，作者：[@tiangolo](https://github.com/tiangolo)。

## 0.7.0 (2024-08-02)

本次包含许多新内容！🎁

* 使用 Playwright 进行端到端测试。
* 添加 Mailcatcher 配置，用于开发和测试邮件处理。
* 添加分页。
* 数据库主键使用 UUID。
* 添加用户注册。
* 支持部署到多个环境（预发布、生产）。
* 包含多项重构与改进。
* 升级多项依赖。

### 功能

* ✨ 添加用户设置端到端测试。 PR [#1271](https://github.com/tiangolo/full-stack-fastapi-template/pull/1271)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加密码重置端到端测试。 PR [#1270](https://github.com/tiangolo/full-stack-fastapi-template/pull/1270)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加用户注册端到端测试。 PR [#1268](https://github.com/tiangolo/full-stack-fastapi-template/pull/1268)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加注册功能，默认设置 `OPEN_USER_REGISTRATION=True`。 PR [#1265](https://github.com/tiangolo/full-stack-fastapi-template/pull/1265)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加登录端到端测试。 PR [#1264](https://github.com/tiangolo/full-stack-fastapi-template/pull/1264)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加 Playwright 前端端到端测试初始配置。 PR [#1261](https://github.com/tiangolo/full-stack-fastapi-template/pull/1261)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加 Mailcatcher 配置。 PR [#1244](https://github.com/tiangolo/full-stack-fastapi-template/pull/1244)，作者：[@patrick91](https://github.com/patrick91)。
* ✨ 为 Item 列表添加分页。 PR [#1239](https://github.com/tiangolo/full-stack-fastapi-template/pull/1239)，作者：[@patrick91](https://github.com/patrick91)。
* 🗃️ 为数据库模型和输入数据添加 max_length 校验。 PR [#1233](https://github.com/tiangolo/full-stack-fastapi-template/pull/1233)，作者：[@estebanx64](https://github.com/estebanx64)。
* ✨ 在开发构建中添加 TanStack React Query 开发工具。 PR [#1217](https://github.com/tiangolo/full-stack-fastapi-template/pull/1217)，作者：[@tomerb](https://github.com/tomerb)。
* ✨ 支持在同一服务器部署预发布和生产等多个环境。 PR [#1128](https://github.com/tiangolo/full-stack-fastapi-template/pull/1128)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 更新 CI GitHub Actions，支持私有仓库。 PR [#1125](https://github.com/tiangolo/full-stack-fastapi-template/pull/1125)，作者：[@tiangolo](https://github.com/tiangolo)。

### 修复

* 🐛 修复欢迎页，使其显示已登录用户。 PR [#1218](https://github.com/tiangolo/full-stack-fastapi-template/pull/1218)，作者：[@tomerb](https://github.com/tomerb)。
* 🐛 修复本地 Traefik 代理网络配置导致的网关超时。 PR [#1184](https://github.com/tiangolo/full-stack-fastapi-template/pull/1184)，作者：[@JoelGotsch](https://github.com/JoelGotsch)。
* ♻️ 修复 .env 中初始管理员密码变化后的测试。 PR [#1165](https://github.com/tiangolo/full-stack-fastapi-template/pull/1165)，作者：[@billzhong](https://github.com/billzhong)。
* 🐛 修复密码重置问题。 PR [#1171](https://github.com/tiangolo/full-stack-fastapi-template/pull/1171)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛 修复前端目录没有 index.html 时的 403 错误。 PR [#1094](https://github.com/tiangolo/full-stack-fastapi-template/pull/1094)，作者：[@tiangolo](https://github.com/tiangolo)。

### 重构

* 🚨 修复 Docker 构建警告。 PR [#1283](https://github.com/tiangolo/full-stack-fastapi-template/pull/1283)，作者：[@erip](https://github.com/erip)。
* ♻️ 重新生成客户端，使用 UUID 替代整数 ID，并更新前端。 PR [#1281](https://github.com/tiangolo/full-stack-fastapi-template/pull/1281)，作者：[@rehanabdul](https://github.com/rehanabdul)。
* ♻️ 微调前端。 PR [#1273](https://github.com/tiangolo/full-stack-fastapi-template/pull/1273)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 添加随机密码工具并重构测试。 PR [#1277](https://github.com/tiangolo/full-stack-fastapi-template/pull/1277)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构模型，使用级联删除关系。 PR [#1276](https://github.com/tiangolo/full-stack-fastapi-template/pull/1276)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔥 移除 `USERS_OPEN_REGISTRATION` 配置，默认开放注册。 PR [#1274](https://github.com/tiangolo/full-stack-fastapi-template/pull/1274)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 在 Alembic 中复用配置中的数据库 URL。 PR [#1229](https://github.com/tiangolo/full-stack-fastapi-template/pull/1229)，作者：[@patrick91](https://github.com/patrick91)。
* 🔧 更新 Playwright 配置与测试，使用环境变量。 PR [#1266](https://github.com/tiangolo/full-stack-fastapi-template/pull/1266)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构数据库模型，使用 UUID 替代整数 ID。 PR [#1259](https://github.com/tiangolo/full-stack-fastapi-template/pull/1259)，作者：[@estebanx64](https://github.com/estebanx64)。
* ♻️ 更新表单输入框宽度。 PR [#1263](https://github.com/tiangolo/full-stack-fastapi-template/pull/1263)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 在工具模块中使用 now(timezone.utc) 替代已弃用的 utcnow()。 PR [#1247](https://github.com/tiangolo/full-stack-fastapi-template/pull/1247)，作者：[@jalvarezz13](https://github.com/jalvarezz13)。
* 🎨 格式化前端代码。 PR [#1262](https://github.com/tiangolo/full-stack-fastapi-template/pull/1262)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 从 Navbar 中抽取专用 AddModal 组件。 PR [#1246](https://github.com/tiangolo/full-stack-fastapi-template/pull/1246)，作者：[@ajbloureiro](https://github.com/ajbloureiro)。
* ♻️ 更新 `login.tsx`，避免用户名或密码为空时出错。 PR [#1257](https://github.com/tiangolo/full-stack-fastapi-template/pull/1257)，作者：[@jmondaud](https://github.com/jmondaud)。
* ♻️ 重构密码找回功能。 PR [#1242](https://github.com/tiangolo/full-stack-fastapi-template/pull/1242)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🎨 执行格式化与静态检查。 PR [#1243](https://github.com/tiangolo/full-stack-fastapi-template/pull/1243)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🎨 生成 OpenAPI 客户端后运行 Biome。 PR [#1226](https://github.com/tiangolo/full-stack-fastapi-template/pull/1226)，作者：[@tomerb](https://github.com/tomerb)。
* ♻️ 更新 DeleteConfirmation 组件，使用新服务。 PR [#1224](https://github.com/tiangolo/full-stack-fastapi-template/pull/1224)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 更新客户端服务。 PR [#1223](https://github.com/tiangolo/full-stack-fastapi-template/pull/1223)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⚒️ 微调前端。 PR [#1210](https://github.com/tiangolo/full-stack-fastapi-template/pull/1210)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🚚 将资源移至 public 目录。 PR [#1206](https://github.com/tiangolo/full-stack-fastapi-template/pull/1206)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构重定向标签，简化移除前端的操作。 PR [#1208](https://github.com/tiangolo/full-stack-fastapi-template/pull/1208)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔒️ 从 python-jose 迁移至 PyJWT。 PR [#1203](https://github.com/tiangolo/full-stack-fastapi-template/pull/1203)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🔥 移除重复代码。 PR [#1185](https://github.com/tiangolo/full-stack-fastapi-template/pull/1185)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 添加 delete_user_me 接口及对应测试。 PR [#1179](https://github.com/tiangolo/full-stack-fastapi-template/pull/1179)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✅ 更新测试，增加数据库记录验证。 PR [#1178](https://github.com/tiangolo/full-stack-fastapi-template/pull/1178)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🚸 使用 `useSuspenseQuery` 获取成员并显示骨架屏。 PR [#1174](https://github.com/tiangolo/full-stack-fastapi-template/pull/1174)，作者：[@patrick91](https://github.com/patrick91)。
* 🎨 格式化工具代码。 PR [#1173](https://github.com/tiangolo/full-stack-fastapi-template/pull/1173)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 在 Item 页面使用 Suspense。 PR [#1167](https://github.com/tiangolo/full-stack-fastapi-template/pull/1167)，作者：[@patrick91](https://github.com/patrick91)。
* 🚸 将登录字段标记为必填。 PR [#1166](https://github.com/tiangolo/full-stack-fastapi-template/pull/1166)，作者：[@patrick91](https://github.com/patrick91)。
* 🚸 改进登录功能。 PR [#1163](https://github.com/tiangolo/full-stack-fastapi-template/pull/1163)，作者：[@patrick91](https://github.com/patrick91)。
* 🥅 在登录页处理 AxiosErrors。 PR [#1162](https://github.com/tiangolo/full-stack-fastapi-template/pull/1162)，作者：[@patrick91](https://github.com/patrick91)。
* 🎨 格式化前端代码。 PR [#1161](https://github.com/tiangolo/full-stack-fastapi-template/pull/1161)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重新生成前端客户端。 PR [#1156](https://github.com/tiangolo/full-stack-fastapi-template/pull/1156)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 将 ModelsOut 重命名为 ModelsPublic。 PR [#1154](https://github.com/tiangolo/full-stack-fastapi-template/pull/1154)，作者：[@estebanx64](https://github.com/estebanx64)。
* ♻️ 将前端客户端生成工具从 `openapi-typescript-codegen` 迁移至 `@hey-api/openapi-ts`。 PR [#1151](https://github.com/tiangolo/full-stack-fastapi-template/pull/1151)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔥 移除未使用的导出并更新依赖。 PR [#1146](https://github.com/tiangolo/full-stack-fastapi-template/pull/1146)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 按环境配置更新 Sentry DSN 初始化。 PR [#1145](https://github.com/tiangolo/full-stack-fastapi-template/pull/1145)，作者：[@estebanx64](https://github.com/estebanx64)。
* ♻️ 重构与微调，将 `UserCreateOpen` 等重命名为 `UserRegister` 等。 PR [#1143](https://github.com/tiangolo/full-stack-fastapi-template/pull/1143)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🎨 格式化导入语句。 PR [#1140](https://github.com/tiangolo/full-stack-fastapi-template/pull/1140)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构并移除 `React.FC`。 PR [#1139](https://github.com/tiangolo/full-stack-fastapi-template/pull/1139)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 在前端添加邮箱格式规则并重构。 PR [#1138](https://github.com/tiangolo/full-stack-fastapi-template/pull/1138)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🥅 为 FastAPI 应用配置 Sentry。 PR [#1136](https://github.com/tiangolo/full-stack-fastapi-template/pull/1136)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🔥 移除已弃用的 Docker Compose version 键。 PR [#1129](https://github.com/tiangolo/full-stack-fastapi-template/pull/1129)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🎨 使用 Biome 格式化。 PR [#1097](https://github.com/tiangolo/full-stack-fastapi-template/pull/1097)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🎨 更新 Biome 格式化器的引号样式。 PR [#1095](https://github.com/tiangolo/full-stack-fastapi-template/pull/1095)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 使用 Biome 替代 ESLint 和 Prettier 进行前端格式化与静态检查。 PR [#719](https://github.com/tiangolo/full-stack-fastapi-template/pull/719)，作者：[@santigandolfo](https://github.com/santigandolfo)。
* 🎨 统一使用按钮样式变体。 PR [#722](https://github.com/tiangolo/full-stack-fastapi-template/pull/722)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🛠️ 改进 `modify-openapi-operationids.js`。 PR [#720](https://github.com/tiangolo/full-stack-fastapi-template/pull/720)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 使用 unittest.mock 替代 pytest-mock，并移除 pytest-cov。 PR [#717](https://github.com/tiangolo/full-stack-fastapi-template/pull/717)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🛠️ 微调前端。 PR [#715](https://github.com/tiangolo/full-stack-fastapi-template/pull/715)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻ 更新 Docker 镜像，避免 M1 Mac 上的错误。 PR [#710](https://github.com/tiangolo/full-stack-fastapi-template/pull/710)，作者：[@dudil](https://github.com/dudil)。
* ✏ 修复 `backend/app/api/routes/items.py` 和 `backend/app/api/routes/users.py` 中变量名的拼写错误。 PR [#711](https://github.com/tiangolo/full-stack-fastapi-template/pull/711)，作者：[@disrupted](https://github.com/disrupted)。

### 升级

* ⬆️ 将 SQLModel 更新为 `>=0.0.21`。 PR [#1275](https://github.com/tiangolo/full-stack-fastapi-template/pull/1275)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆️ 升级 Traefik。 PR [#1241](https://github.com/tiangolo/full-stack-fastapi-template/pull/1241)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 将 requests 从 2.31.0 升级至 2.32.0（位置或分组：/backend）。 PR [#1211](https://github.com/tiangolo/full-stack-fastapi-template/pull/1211)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 jinja2 从 3.1.3 升级至 3.1.4（位置或分组：/backend）。 PR [#1196](https://github.com/tiangolo/full-stack-fastapi-template/pull/1196)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 将 gunicorn 从 21.2.0 升级至 22.0.0（位置或分组：/backend）。 PR [#1176](https://github.com/tiangolo/full-stack-fastapi-template/pull/1176)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 将 idna 从 3.6 升级至 3.7（位置或分组：/backend）。 PR [#1168](https://github.com/tiangolo/full-stack-fastapi-template/pull/1168)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🆙 将 React Query 更新为 TanStack Query。 PR [#1153](https://github.com/tiangolo/full-stack-fastapi-template/pull/1153)，作者：[@patrick91](https://github.com/patrick91)。
* 将 vite 从 5.0.12 升级至 5.0.13（位置或分组：/frontend）。 PR [#1149](https://github.com/tiangolo/full-stack-fastapi-template/pull/1149)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 将 follow-redirects 从 1.15.5 升级至 1.15.6（位置或分组：/frontend）。 PR [#734](https://github.com/tiangolo/full-stack-fastapi-template/pull/734)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。

### 文档

* 📝 将 tiangolo 仓库链接更新为 fastapi 组织仓库链接。 PR [#1285](https://github.com/fastapi/full-stack-fastapi-template/pull/1285)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 在前端 `README.md` 中添加 Playwright 端到端测试说明。 PR [#1279](https://github.com/tiangolo/full-stack-fastapi-template/pull/1279)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 更新 release-notes.md。 PR [#1220](https://github.com/tiangolo/full-stack-fastapi-template/pull/1220)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✏️ 更新 `README.md`。 PR [#1205](https://github.com/tiangolo/full-stack-fastapi-template/pull/1205)，作者：[@Craz1k0ek](https://github.com/Craz1k0ek)。
* ✏️ 修复 `deployment.md` 中的 Adminer URL。 PR [#1194](https://github.com/tiangolo/full-stack-fastapi-template/pull/1194)，作者：[@PhilippWu](https://github.com/PhilippWu)。
* 📝 在后端文档中添加开放用户注册说明。 PR [#1191](https://github.com/tiangolo/full-stack-fastapi-template/pull/1191)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 更新 release-notes.md。 PR [#1164](https://github.com/tiangolo/full-stack-fastapi-template/pull/1164)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 更新 `README.md`。 PR [#716](https://github.com/tiangolo/full-stack-fastapi-template/pull/716)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 更新私有仓库克隆与同步更新说明。 PR [#1127](https://github.com/tiangolo/full-stack-fastapi-template/pull/1127)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 添加 CI 密钥 LATEST_CHANGES 和 SMOKESHOW_AUTH_KEY 的文档。 PR [#1126](https://github.com/tiangolo/full-stack-fastapi-template/pull/1126)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✏️ 修复 `backend/README.md` 中不使用迁移时的文件路径说明。 PR [#1116](https://github.com/tiangolo/full-stack-fastapi-template/pull/1116)，作者：[@leonlowitzki](https://github.com/leonlowitzki)。
* 📝 添加提交前钩子和代码静态检查文档。 PR [#718](https://github.com/tiangolo/full-stack-fastapi-template/pull/718)，作者：[@estebanx64](https://github.com/estebanx64)。
* 📝 修复 `development.md` 中的 localhost URL。 PR [#1099](https://github.com/tiangolo/full-stack-fastapi-template/pull/1099)，作者：[@efonte](https://github.com/efonte)。
* ✏ 统一标题。 PR [#708](https://github.com/tiangolo/full-stack-fastapi-template/pull/708)，作者：[@codesmith-emmy](https://github.com/codesmith-emmy)。
* 📝 更新 `README.md` 中深色模式截图的位置。 PR [#706](https://github.com/tiangolo/full-stack-fastapi-template/pull/706)，作者：[@alejsdev](https://github.com/alejsdev)。

### 内部维护

* 🔧 更新部署工作流，排除主仓库。 PR [#1284](https://github.com/tiangolo/full-stack-fastapi-template/pull/1284)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷 更新 issue-manager.yml GitHub Action 权限。 PR [#1278](https://github.com/tiangolo/full-stack-fastapi-template/pull/1278)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 将 setuptools 从 69.1.1 升级至 70.0.0（位置或分组：/backend）。 PR [#1255](https://github.com/tiangolo/full-stack-fastapi-template/pull/1255)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 certifi 从 2024.2.2 升级至 2024.7.4（位置或分组：/backend）。 PR [#1250](https://github.com/tiangolo/full-stack-fastapi-template/pull/1250)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆️ 将 urllib3 从 2.2.1 升级至 2.2.2（位置或分组：/backend）。 PR [#1235](https://github.com/tiangolo/full-stack-fastapi-template/pull/1235)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 在 Biome 中忽略 `src/routeTree.gen.ts`。 PR [#1175](https://github.com/tiangolo/full-stack-fastapi-template/pull/1175)，作者：[@patrick91](https://github.com/patrick91)。
* 👷 更新 Smokeshow 下载产物的 GitHub Action。 PR [#1198](https://github.com/tiangolo/full-stack-fastapi-template/pull/1198)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 更新 `.nvmrc` 中的 Node.js 版本。 PR [#1192](https://github.com/tiangolo/full-stack-fastapi-template/pull/1192)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔥 从提交前检查配置中移除 ESLint 和 Prettier。 PR [#1096](https://github.com/tiangolo/full-stack-fastapi-template/pull/1096)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 更新 mypy 配置，忽略 .venv 目录。 PR [#1155](https://github.com/tiangolo/full-stack-fastapi-template/pull/1155)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🚨 启用 `ARG001`，防止未使用的参数。 PR [#1152](https://github.com/tiangolo/full-stack-fastapi-template/pull/1152)，作者：[@patrick91](https://github.com/patrick91)。
* 🔥 移除 isort 配置，改用 Ruff。 PR [#1144](https://github.com/tiangolo/full-stack-fastapi-template/pull/1144)，作者：[@patrick91](https://github.com/patrick91)。
* 🔧 更新提交前检查配置，排除生成的客户端目录。 PR [#1150](https://github.com/tiangolo/full-stack-fastapi-template/pull/1150)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 修改 `.nvmrc` 格式。 PR [#1148](https://github.com/tiangolo/full-stack-fastapi-template/pull/1148)，作者：[@patrick91](https://github.com/patrick91)。
* 🎨 在 Ruff 检查与格式化时忽略 Alembic。 PR [#1131](https://github.com/tiangolo/full-stack-fastapi-template/pull/1131)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🔧 添加 GitHub 讨论、问题模板及安全政策。 PR [#1105](https://github.com/tiangolo/full-stack-fastapi-template/pull/1105)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⬆ 将 dawidd6/action-download-artifact 从 3.1.2 升级至 3.1.4。 PR [#1103](https://github.com/tiangolo/full-stack-fastapi-template/pull/1103)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 🔧 将 Biome 加入提交前检查配置。 PR [#1098](https://github.com/tiangolo/full-stack-fastapi-template/pull/1098)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔥 删除残留的 Celery 文件。 PR [#727](https://github.com/tiangolo/full-stack-fastapi-template/pull/727)，作者：[@dr-neptune](https://github.com/dr-neptune)。
* ⚙️ 在提交前检查配置中添加 Prettier 和 ESLint。 PR [#714](https://github.com/tiangolo/full-stack-fastapi-template/pull/714)，作者：[@alejsdev](https://github.com/alejsdev)。

## 0.6.0 (2024-03-12)

使用最新 FastAPI、Pydantic、SQLModel 🚀

全新前端：React、TS、Vite、Chakra UI、TanStack Query/Router，以及自动生成的客户端/SDK 🎨

基于 GitHub Actions 的持续集成与持续部署 🤖

测试覆盖率超过 90% ✅

### 功能

* ✨ 引入 SQLModel，创建并开始使用模型。 PR [#559](https://github.com/tiangolo/full-stack-fastapi-template/pull/559)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✨ 使用新 SQLModel 模型升级 Item 路由，简化逻辑并采用 FastAPI Annotated 依赖。 PR [#560](https://github.com/tiangolo/full-stack-fastapi-template/pull/560)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✨ 从 pgAdmin 迁移至 Adminer。 PR [#692](https://github.com/tiangolo/full-stack-fastapi-template/pull/692)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✨ 支持设置 `POSTGRES_PORT`。 PR [#333](https://github.com/tiangolo/full-stack-fastapi-template/pull/333)，作者：[@uepoch](https://github.com/uepoch)。
* ⬆ 升级 Flower 版本与命令。 PR [#447](https://github.com/tiangolo/full-stack-fastapi-template/pull/447)，作者：[@maurob](https://github.com/maurob)。
* 🎨 改进样式。 PR [#673](https://github.com/tiangolo/full-stack-fastapi-template/pull/673)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🎨 更新主题。 PR [#666](https://github.com/tiangolo/full-stack-fastapi-template/pull/666)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷 添加持续部署及相关重构。 PR [#667](https://github.com/tiangolo/full-stack-fastapi-template/pull/667)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✨ 添加展示密码找回邮件内容的接口并更新邮件模板。 PR [#664](https://github.com/tiangolo/full-stack-fastapi-template/pull/664)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🎨 使用 Prettier 格式化。 PR [#646](https://github.com/tiangolo/full-stack-fastapi-template/pull/646)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✅ 添加测试，使覆盖率达到至少 90%，并修复密码找回逻辑。 PR [#632](https://github.com/tiangolo/full-stack-fastapi-template/pull/632)，作者：[@estebanx64](https://github.com/estebanx64)。
* ⚙️ 添加 Prettier、ESLint 及提交前检查配置。 PR [#640](https://github.com/tiangolo/full-stack-fastapi-template/pull/640)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷 在 CI 中添加 Smokeshow 覆盖率报告与徽章。 PR [#638](https://github.com/tiangolo/full-stack-fastapi-template/pull/638)，作者：[@estebanx64](https://github.com/estebanx64)。
* ✨ 迁移至 TanStack Query（React Query）和 TanStack Router。 PR [#637](https://github.com/tiangolo/full-stack-fastapi-template/pull/637)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✅ 添加测试数据库的初始化与清理。 PR [#626](https://github.com/tiangolo/full-stack-fastapi-template/pull/626)，作者：[@estebanx64](https://github.com/estebanx64)。
* ✨ 更新 new-frontend 客户端。 PR [#625](https://github.com/tiangolo/full-stack-fastapi-template/pull/625)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加密码重置功能。 PR [#624](https://github.com/tiangolo/full-stack-fastapi-template/pull/624)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加私有与公开路由。 PR [#621](https://github.com/tiangolo/full-stack-fastapi-template/pull/621)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 添加 VS Code 调试配置。 PR [#620](https://github.com/tiangolo/full-stack-fastapi-template/pull/620)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✨ 添加 `Not Found` 页面。 PR [#595](https://github.com/tiangolo/full-stack-fastapi-template/pull/595)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加页面、组件、面板、弹窗和主题，并重构改进现有组件。 PR [#593](https://github.com/tiangolo/full-stack-fastapi-template/pull/593)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 支持删除自己的账号并进行其他微调。 PR [#614](https://github.com/tiangolo/full-stack-fastapi-template/pull/614)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 调整目录结构，支持编辑用户和 Item，并进行其他重构改进。 PR [#603](https://github.com/tiangolo/full-stack-fastapi-template/pull/603)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 引入 Copier 替代 Cookiecutter，同时支持直接使用、fork 或克隆项目。 PR [#612](https://github.com/tiangolo/full-stack-fastapi-template/pull/612)，作者：[@tiangolo](https://github.com/tiangolo)。
* ➕ 使用 Ruff 替代 black、isort、flake8、autoflake，并升级 mypy。 PR [#610](https://github.com/tiangolo/full-stack-fastapi-template/pull/610)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻ 重构 Item 与服务接口，使其返回 count 和 data，并添加 CI 测试。 PR [#599](https://github.com/tiangolo/full-stack-fastapi-template/pull/599)，作者：[@estebanx64](https://github.com/estebanx64)。
* ✨ 支持更新 Item，将 SQLModel 升级至支持模型对象更新的 0.0.16。 PR [#601](https://github.com/tiangolo/full-stack-fastapi-template/pull/601)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✨ 为新前端添加深色模式及按条件显示的侧边栏菜单。 PR [#600](https://github.com/tiangolo/full-stack-fastapi-template/pull/600)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 迁移至 RouterProvider 并进行其他重构。 PR [#598](https://github.com/tiangolo/full-stack-fastapi-template/pull/598)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 添加 delete_user，重构 delete_item。 PR [#594](https://github.com/tiangolo/full-stack-fastapi-template/pull/594)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 为新前端添加状态存储。 PR [#592](https://github.com/tiangolo/full-stack-fastapi-template/pull/592)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 为管理员、Item 和登录页面添加表单校验。 PR [#616](https://github.com/tiangolo/full-stack-fastapi-template/pull/616)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 为新前端添加侧边栏。 PR [#587](https://github.com/tiangolo/full-stack-fastapi-template/pull/587)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 为新前端添加登录功能。 PR [#585](https://github.com/tiangolo/full-stack-fastapi-template/pull/585)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 在生成的前端客户端中包含模式定义。 PR [#584](https://github.com/tiangolo/full-stack-fastapi-template/pull/584)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 根据近期修改重新生成前端客户端。 PR [#575](https://github.com/tiangolo/full-stack-fastapi-template/pull/575)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构 `utils.py` 中的 API。 PR [#573](https://github.com/tiangolo/full-stack-fastapi-template/pull/573)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 更新登录 API 代码。 PR [#571](https://github.com/tiangolo/full-stack-fastapi-template/pull/571)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✨ 添加前端客户端及生成流程。 PR [#569](https://github.com/tiangolo/full-stack-fastapi-template/pull/569)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐳 为 new-frontend 配置 Docker。 PR [#564](https://github.com/tiangolo/full-stack-fastapi-template/pull/564)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 使用 Vite、TypeScript 和 React 创建新前端。 PR [#563](https://github.com/tiangolo/full-stack-fastapi-template/pull/563)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📌 添加 NodeJS 版本管理及说明。 PR [#551](https://github.com/tiangolo/full-stack-fastapi-template/pull/551)，作者：[@alejsdev](https://github.com/alejsdev)。
* 对未设置的环境变量提供一致的错误提示。 PR [#200](https://github.com/tiangolo/full-stack-fastapi-template/pull/200)。
* 将 Traefik 升级至版本 2，与 DockerSwarm.rocks 保持一致。 PR [#199](https://github.com/tiangolo/full-stack-fastapi-template/pull/199)。
* 使用 `TestClient` 运行测试。 PR [#160](https://github.com/tiangolo/full-stack-fastapi-template/pull/160)。

### 修复

* 🐛 修复 Copier 对引号中包含空格的字符串变量的处理。 PR [#631](https://github.com/tiangolo/full-stack-fastapi-template/pull/631)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🐛 修复用户将邮箱更新为原邮箱时的问题。 PR [#696](https://github.com/tiangolo/full-stack-fastapi-template/pull/696)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛 仅在使用时配置 Sentry。 PR [#671](https://github.com/tiangolo/full-stack-fastapi-template/pull/671)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔥 移除不必要的校验。 PR [#662](https://github.com/tiangolo/full-stack-fastapi-template/pull/662)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛 修复编辑当前用户时的问题。 PR [#651](https://github.com/tiangolo/full-stack-fastapi-template/pull/651)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛  为 `SidebarItems` 添加 `onClose`。 PR [#589](https://github.com/tiangolo/full-stack-fastapi-template/pull/589)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛 修复 `init_db.py` 中的位置参数错误。 PR [#562](https://github.com/tiangolo/full-stack-fastapi-template/pull/562)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📌 修复 Flower Docker 镜像并固定版本。 PR [#396](https://github.com/tiangolo/full-stack-fastapi-template/pull/396)，作者：[@sanggusti](https://github.com/sanggusti)。
* 🐛 修复 Celery Worker 命令。 PR [#443](https://github.com/tiangolo/full-stack-fastapi-template/pull/443)，作者：[@bechtold](https://github.com/bechtold)。
* 🐛 修复 Dockerfile 中的 Poetry 安装，并升级 Python 与依赖以解决构建问题。 PR [#480](https://github.com/tiangolo/full-stack-fastapi-template/pull/480)，作者：[@little7Li](https://github.com/little7Li)。

### 重构

* 🔧 添加缺失的 dotenv 变量。 PR [#554](https://github.com/tiangolo/full-stack-fastapi-template/pull/554)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⏪ 撤销“添加 Prettier、ESLint 与提交前检查配置”的修改。 PR [#644](https://github.com/tiangolo/full-stack-fastapi-template/pull/644)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🙈 添加 .prettierignore 并包含客户端目录。 PR [#648](https://github.com/tiangolo/full-stack-fastapi-template/pull/648)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🏷️ 在测试 GitHub Action 中添加 mypy，并修复全项目类型。 PR [#655](https://github.com/tiangolo/full-stack-fastapi-template/pull/655)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🔒️ 确保不会将默认值 changethis 用于部署。 PR [#698](https://github.com/tiangolo/full-stack-fastapi-template/pull/698)，作者：[@tiangolo](https://github.com/tiangolo)。
* ◀ 撤销“将 Dashboard 重命名为 Home 并更新截图”的修改。 PR [#697](https://github.com/tiangolo/full-stack-fastapi-template/pull/697)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📸 将 Dashboard 重命名为 Home 并更新截图。 PR [#693](https://github.com/tiangolo/full-stack-fastapi-template/pull/693)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🐛 修复按用户查询全部 Item 时的计数。 PR [#695](https://github.com/tiangolo/full-stack-fastapi-template/pull/695)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🔥 移除当时未使用且上游不再推荐的 Celery 和 Flower。 PR [#694](https://github.com/tiangolo/full-stack-fastapi-template/pull/694)，作者：[@tiangolo](https://github.com/tiangolo)。
* ✅ 添加无权限删除用户的测试。 PR [#690](https://github.com/tiangolo/full-stack-fastapi-template/pull/690)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构用户更新逻辑。 PR [#689](https://github.com/tiangolo/full-stack-fastapi-template/pull/689)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📌 将 Poetry 锁文件纳入 Git。 PR [#685](https://github.com/tiangolo/full-stack-fastapi-template/pull/685)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🎨 调整颜色与间距。 PR [#684](https://github.com/tiangolo/full-stack-fastapi-template/pull/684)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷 使用 PYTHONDONTWRITEBYTECODE=1 避免生成不必要的 *.pyc 文件。 PR [#677](https://github.com/tiangolo/full-stack-fastapi-template/pull/677)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🔧 为旧 SMTP 服务器添加 `SMTP_SSL` 选项。 PR [#365](https://github.com/tiangolo/full-stack-fastapi-template/pull/365)，作者：[@Metrea](https://github.com/Metrea)。
* ♻️ 重构逻辑，支持本地运行 pytest。 PR [#683](https://github.com/tiangolo/full-stack-fastapi-template/pull/683)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻ 更新错误消息。 PR [#417](https://github.com/tiangolo/full-stack-fastapi-template/pull/417)，作者：[@qu3vipon](https://github.com/qu3vipon)。
* 🔧 添加默认 Flower 密码。 PR [#682](https://github.com/tiangolo/full-stack-fastapi-template/pull/682)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 更新 VS Code 调试配置。 PR [#676](https://github.com/tiangolo/full-stack-fastapi-template/pull/676)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 重构测试代码结构。 PR [#674](https://github.com/tiangolo/full-stack-fastapi-template/pull/674)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 仅在开发模式启用 TanStack Router 开发工具。 PR [#668](https://github.com/tiangolo/full-stack-fastapi-template/pull/668)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构邮件逻辑，支持在测试和开发中复用工具函数。 PR [#663](https://github.com/tiangolo/full-stack-fastapi-template/pull/663)，作者：[@tiangolo](https://github.com/tiangolo)。
* 💬 改进删除账号的说明与确认。 PR [#661](https://github.com/tiangolo/full-stack-fastapi-template/pull/661)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构邮件模板。 PR [#659](https://github.com/tiangolo/full-stack-fastapi-template/pull/659)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 更新部署文件与文档。 PR [#660](https://github.com/tiangolo/full-stack-fastapi-template/pull/660)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔥 移除未使用的模式定义。 PR [#656](https://github.com/tiangolo/full-stack-fastapi-template/pull/656)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔥 移除旧前端。 PR [#649](https://github.com/tiangolo/full-stack-fastapi-template/pull/649)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻ 将源码从 src 移至顶层，并更新 Sentry 依赖。 PR [#630](https://github.com/tiangolo/full-stack-fastapi-template/pull/630)，作者：[@estebanx64](https://github.com/estebanx64)。
* ♻ 重构 Python 目录结构。 PR [#629](https://github.com/tiangolo/full-stack-fastapi-template/pull/629)，作者：[@estebanx64](https://github.com/estebanx64)。
* ♻️ 重构旧 CRUD 工具与测试。 PR [#622](https://github.com/tiangolo/full-stack-fastapi-template/pull/622)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 更新 .env，支持后端本地调试。 PR [#618](https://github.com/tiangolo/full-stack-fastapi-template/pull/618)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 重构并更新 CORS，处理 Pydantic v2 产生的尾部斜杠。 PR [#617](https://github.com/tiangolo/full-stack-fastapi-template/pull/617)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🎨 使用 pre-commit 和 Ruff 格式化文件。 PR [#611](https://github.com/tiangolo/full-stack-fastapi-template/pull/611)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🚚 重构并简化后端文件结构。 PR [#609](https://github.com/tiangolo/full-stack-fastapi-template/pull/609)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔥 清理不再适用的旧文件。 PR [#608](https://github.com/tiangolo/full-stack-fastapi-template/pull/608)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻ 重组 Docker Compose 文件，移除 Docker Swarm 专属逻辑。 PR [#607](https://github.com/tiangolo/full-stack-fastapi-template/pull/607)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 重构更新接口，并为新前端重新生成客户端。 PR [#602](https://github.com/tiangolo/full-stack-fastapi-template/pull/602)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✨ 为应用添加 Layout。 PR [#588](https://github.com/tiangolo/full-stack-fastapi-template/pull/588)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重新启用用户更新路径操作，以生成前端客户端。 PR [#574](https://github.com/tiangolo/full-stack-fastapi-template/pull/574)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 移除类型忽略标记并添加 `response_model`。 PR [#572](https://github.com/tiangolo/full-stack-fastapi-template/pull/572)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构用户 API 及依赖。 PR [#561](https://github.com/tiangolo/full-stack-fastapi-template/pull/561)，作者：[@alejsdev](https://github.com/alejsdev)。
* ♻️ 重构前端 Docker 构建，使用标准 NodeJS 和自定义 Nginx 配置，修复旧 Vue 构建。 PR [#555](https://github.com/tiangolo/full-stack-fastapi-template/pull/555)，作者：[@tiangolo](https://github.com/tiangolo)。
* ♻️ 重构项目生成流程，移除 Cookiecutter，改用普通 Git 克隆或 fork。 PR [#553](https://github.com/tiangolo/full-stack-fastapi-template/pull/553)，作者：[@tiangolo](https://github.com/tiangolo)。
* 重构后端：
    * 简化工具配置与格式，更好地支持编辑器集成。
    * 添加 mypy 配置和插件。
    * 为整个代码库添加类型标注。
    * 通过插件更新 SQLAlchemy 模型类型。
    * 更新并重构 CRUD 工具。
    * 使用带 `yield` 的依赖重构数据库会话。
    * 重构依赖、安全、CRUD、模型和模式定义，简化代码并改善自动补全。
    * 从 PyJWT 改用 Python-JOSE，以支持更多用例。
    * 修复 JWT，使其使用用户邮箱或 ID 作为 `sub` 主体。
    * PR [#158](https://github.com/tiangolo/full-stack-fastapi-template/pull/158)。
* 简化 `docker-compose.*.yml` 文件，重构部署以减少配置文件数量。 PR [#153](https://github.com/tiangolo/full-stack-fastapi-template/pull/153)。
* 简化环境变量文件，合并为一个 `.env`。 PR [#151](https://github.com/tiangolo/full-stack-fastapi-template/pull/151)。

### 升级

* 📌 升级 Poetry 锁定依赖。 PR [#702](https://github.com/tiangolo/full-stack-fastapi-template/pull/702)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆️ 升级 Python 版本及依赖。 PR [#558](https://github.com/tiangolo/full-stack-fastapi-template/pull/558)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆ 将 tiangolo/issue-manager 从 0.2.0 升级至 0.5.0。 PR [#591](https://github.com/tiangolo/full-stack-fastapi-template/pull/591)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 将 follow-redirects 从 1.15.3 升级至 1.15.5（位置或分组：/frontend）。 PR [#654](https://github.com/tiangolo/full-stack-fastapi-template/pull/654)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 将 vite 从 5.0.4 升级至 5.0.12（位置或分组：/frontend）。 PR [#653](https://github.com/tiangolo/full-stack-fastapi-template/pull/653)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 将 fastapi 从 0.104.1 升级至 0.109.1（位置或分组：/backend）。 PR [#687](https://github.com/tiangolo/full-stack-fastapi-template/pull/687)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 将 python-multipart 从 0.0.6 升级至 0.0.7（位置或分组：/backend）。 PR [#686](https://github.com/tiangolo/full-stack-fastapi-template/pull/686)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 添加 `uvicorn[standard]`，引入 `watchgod` 和 `uvloop`。 PR [#438](https://github.com/tiangolo/full-stack-fastapi-template/pull/438)，作者：[@alonme](https://github.com/alonme)。
* ⬆ 升级代码以支持 Pydantic V2。 PR [#615](https://github.com/tiangolo/full-stack-fastapi-template/pull/615)，作者：[@estebanx64](https://github.com/estebanx64)。

### 文档

* 🦇 在 `README.md` 中添加深色模式。 PR [#703](https://github.com/tiangolo/full-stack-fastapi-template/pull/703)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🍱 更新 GitHub 图片。 PR [#701](https://github.com/tiangolo/full-stack-fastapi-template/pull/701)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🍱 添加 GitHub 图片。 PR [#700](https://github.com/tiangolo/full-stack-fastapi-template/pull/700)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🚚 将项目重命名为 Full Stack FastAPI Template。 PR [#699](https://github.com/tiangolo/full-stack-fastapi-template/pull/699)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 更新 `README.md`。 PR [#691](https://github.com/tiangolo/full-stack-fastapi-template/pull/691)，作者：[@alejsdev](https://github.com/alejsdev)。
* ✏ 修复 `development.md` 中的拼写错误。 PR [#309](https://github.com/tiangolo/full-stack-fastapi-template/pull/309)，作者：[@graue70](https://github.com/graue70)。
* 📝 添加通配符域名文档。 PR [#681](https://github.com/tiangolo/full-stack-fastapi-template/pull/681)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 在文档中补充必需的 GitHub Actions 密钥。 PR [#679](https://github.com/tiangolo/full-stack-fastapi-template/pull/679)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 更新 `README.md` 和 `deployment.md`。 PR [#678](https://github.com/tiangolo/full-stack-fastapi-template/pull/678)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 更新前端 `README.md`。 PR [#675](https://github.com/tiangolo/full-stack-fastapi-template/pull/675)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 更新部署文档，为 traefik-public 使用其他目录。 PR [#670](https://github.com/tiangolo/full-stack-fastapi-template/pull/670)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📸 添加新截图。 PR [#657](https://github.com/tiangolo/full-stack-fastapi-template/pull/657)，作者：[@alejsdev](https://github.com/alejsdev)。
* 📝 将 README 拆分为后端、前端、部署和开发的独立文档。 PR [#639](https://github.com/tiangolo/full-stack-fastapi-template/pull/639)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 更新 README。 PR [#628](https://github.com/tiangolo/full-stack-fastapi-template/pull/628)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 更新 latest-changes GitHub Action，并将发布记录移至独立文件。 PR [#619](https://github.com/tiangolo/full-stack-fastapi-template/pull/619)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 更新内部 README 及其引用文件。 PR [#613](https://github.com/tiangolo/full-stack-fastapi-template/pull/613)，作者：[@tiangolo](https://github.com/tiangolo)。
* 📝 在 README 中添加建设中提示。 PR [#552](https://github.com/tiangolo/full-stack-fastapi-template/pull/552)，作者：[@tiangolo](https://github.com/tiangolo)。
* 添加 HTML 测试覆盖率报告说明。 PR [#161](https://github.com/tiangolo/full-stack-fastapi-template/pull/161)。
* 添加移除前端、仅保留 API 的说明。 PR [#156](https://github.com/tiangolo/full-stack-fastapi-template/pull/156)。

### 内部维护

* 👷 在 GitHub Actions 中添加独立于测试的静态检查。 PR [#688](https://github.com/tiangolo/full-stack-fastapi-template/pull/688)，作者：[@tiangolo](https://github.com/tiangolo)。
* ⬆ 将 dawidd6/action-download-artifact 从 2.28.0 升级至 3.1.2。 PR [#643](https://github.com/tiangolo/full-stack-fastapi-template/pull/643)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/upload-artifact 从 3 升级至 4。 PR [#642](https://github.com/tiangolo/full-stack-fastapi-template/pull/642)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* ⬆ 将 actions/setup-python 从 4 升级至 5。 PR [#641](https://github.com/tiangolo/full-stack-fastapi-template/pull/641)，作者：[@dependabot[bot]](https://github.com/apps/dependabot)。
* 👷 调整测试 GitHub Action 名称。 PR [#672](https://github.com/tiangolo/full-stack-fastapi-template/pull/672)，作者：[@tiangolo](https://github.com/tiangolo)。
* 🔧 添加 `.gitattributes`，确保 `.sh` 文件使用 LF 换行。 PR [#658](https://github.com/tiangolo/full-stack-fastapi-template/pull/658)，作者：[@estebanx64](https://github.com/estebanx64)。
* 🚚 将 new-frontend 移至 frontend。 PR [#652](https://github.com/tiangolo/full-stack-fastapi-template/pull/652)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 添加 ESLint 脚本。 PR [#650](https://github.com/tiangolo/full-stack-fastapi-template/pull/650)，作者：[@alejsdev](https://github.com/alejsdev)。
* ⚙️ 添加 Prettier 配置。 PR [#647](https://github.com/tiangolo/full-stack-fastapi-template/pull/647)，作者：[@alejsdev](https://github.com/alejsdev)。
* 🔧 更新提交前检查配置。 PR [#645](https://github.com/tiangolo/full-stack-fastapi-template/pull/645)，作者：[@alejsdev](https://github.com/alejsdev)。
* 👷 添加 Dependabot。 PR [#547](https://github.com/tiangolo/full-stack-fastapi-template/pull/547)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 再次修复 latest-changes GitHub Action 令牌。 PR [#546](https://github.com/tiangolo/full-stack-fastapi-template/pull/546)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 修复 latest-changes GitHub Action 令牌配置。 PR [#545](https://github.com/tiangolo/full-stack-fastapi-template/pull/545)，作者：[@tiangolo](https://github.com/tiangolo)。
* 👷 添加 latest-changes GitHub Action。 PR [#544](https://github.com/tiangolo/full-stack-fastapi-template/pull/544)，作者：[@tiangolo](https://github.com/tiangolo)。
* 更新 issue-manager。 PR [#211](https://github.com/tiangolo/full-stack-fastapi-template/pull/211)。
* 添加 [GitHub Sponsors](https://github.com/sponsors/tiangolo) 按钮。 PR [#201](https://github.com/tiangolo/full-stack-fastapi-template/pull/201)。
* 简化脚本与开发流程，更新文档和配置。 PR [#155](https://github.com/tiangolo/full-stack-fastapi-template/pull/155)。

## 0.5.0 (2020-04-19)

* 参照 DockerSwarm.rocks，将 Traefik 公共网络固定默认为 `traefik-public`，简化项目生成器开发与迭代。 PR [#150](https://github.com/tiangolo/full-stack-fastapi-template/pull/150)。
* 更新至 PostgreSQL 12。 PR [#148](https://github.com/tiangolo/full-stack-fastapi-template/pull/148)，作者：[@RCheese](https://github.com/RCheese)。
* 使用 Poetry 管理包。 初始 PR [#144](https://github.com/tiangolo/full-stack-fastapi-template/pull/144)，作者：[@RCheese](https://github.com/RCheese)。
* 使用 Cookiecutter 钩子修复生成项目后 Shell 脚本的 Windows 换行。 PR [#149](https://github.com/tiangolo/full-stack-fastapi-template/pull/149)。
* 将 Vue CLI 升级至版本 4。 PR [#120](https://github.com/tiangolo/full-stack-fastapi-template/pull/120)，作者：[@br3ndonland](https://github.com/br3ndonland)。
* 移除重复的 `login` 标签。 PR [#135](https://github.com/tiangolo/full-stack-fastapi-template/pull/135)，作者：[@Nonameentered](https://github.com/Nonameentered)。
* 修复未填写姓名时仪表盘显示邮箱的问题。 PR [#129](https://github.com/tiangolo/full-stack-fastapi-template/pull/129)，作者：[@rlonka](https://github.com/rlonka)。
* 使用 Black 和 Flake8 格式化代码。 PR [#121](https://github.com/tiangolo/full-stack-fastapi-template/pull/121)，作者：[@br3ndonland](https://github.com/br3ndonland)。
* 简化 SQLAlchemy Base 类。 PR [#117](https://github.com/tiangolo/full-stack-fastapi-template/pull/117)，作者：[@airibarne](https://github.com/airibarne)。
* 更新用户 CRUD 工具，处理密码哈希。 PR [#106](https://github.com/tiangolo/full-stack-fastapi-template/pull/106)，作者：[@mocsar](https://github.com/mocsar)。
* 使用 `.` 替代 `source`，提高兼容性。 PR [#98](https://github.com/tiangolo/full-stack-fastapi-template/pull/98)，作者：[@gucharbon](https://github.com/gucharbon)。
* 使用 Pydantic 的 `BaseSettings` 管理配置与环境变量。 PR [#87](https://github.com/tiangolo/full-stack-fastapi-template/pull/87)，作者：[@StephenBrown2](https://github.com/StephenBrown2)。
* 移除 `package-lock.json`，让使用者按操作系统等情况自行锁定版本。
* 简化 Traefik 服务标签。 PR [#139](https://github.com/tiangolo/full-stack-fastapi-template/pull/139)。
* 添加邮箱校验。 PR [#40](https://github.com/tiangolo/full-stack-fastapi-template/pull/40)，作者：[@kedod](https://github.com/kedod)。
* 修复 README 拼写错误。 PR [#83](https://github.com/tiangolo/full-stack-fastapi-template/pull/83)，作者：[@ashears](https://github.com/ashears)。
* 修复 README 拼写错误。 PR [#80](https://github.com/tiangolo/full-stack-fastapi-template/pull/80)，作者：[@abjoker](https://github.com/abjoker)。
* 修复 `read_item` 函数名和响应状态码。 PR [#74](https://github.com/tiangolo/full-stack-fastapi-template/pull/74)，作者：[@jcaguirre89](https://github.com/jcaguirre89)。
* 修复注释拼写错误。 PR [#70](https://github.com/tiangolo/full-stack-fastapi-template/pull/70)，作者：[@daniel-butler](https://github.com/daniel-butler)。
* 修复 Flower Docker 配置。 PR [#37](https://github.com/tiangolo/full-stack-fastapi-template/pull/37)，作者：[@dmontagu](https://github.com/dmontagu)。
* 添加基于数据库与 Pydantic 模型的新 CRUD 工具。 初始 PR [#23](https://github.com/tiangolo/full-stack-fastapi-template/pull/23)，作者：[@ebreton](https://github.com/ebreton)。
* 添加普通用户测试的 pytest fixture。 PR [#20](https://github.com/tiangolo/full-stack-fastapi-template/pull/20)，作者：[@ebreton](https://github.com/ebreton)。

## 0.4.0 (2019-05-29)

* 修复密码重置安全问题，通过请求体而非查询参数接收令牌。 PR [#34](https://github.com/tiangolo/full-stack-fastapi-template/pull/34)。

* 修复密码重置安全问题，通过请求体而非查询参数接收数据。 PR [#33](https://github.com/tiangolo/full-stack-fastapi-template/pull/33)，作者：[@dmontagu](https://github.com/dmontagu)。

* 修复 SQLAlchemy 初始化时的类查找。 PR [#29](https://github.com/tiangolo/full-stack-fastapi-template/pull/29)，作者：[@ebreton](https://github.com/ebreton)。

* 修复数据库重启后的 SQLAlchemy 操作错误。 PR [#32](https://github.com/tiangolo/full-stack-fastapi-template/pull/32)，作者：[@ebreton](https://github.com/ebreton)。

* 修复生成的 README 中的脚本位置。 PR [#19](https://github.com/tiangolo/full-stack-fastapi-template/pull/19)，作者：[@ebreton](https://github.com/ebreton)。

* 将脚本参数传递给容器内的 `pytest`。 PR [#17](https://github.com/tiangolo/full-stack-fastapi-template/pull/17)，作者：[@ebreton](https://github.com/ebreton)。

* 更新开发脚本。

* 从环境变量读取 Alembic 配置。 PR <a href="https://github.com/tiangolo/full-stack-fastapi-template/pull/9" target="_blank">#9</a>，作者：<a href="https://github.com/ebreton" target="_blank">@ebreton</a>。

* 使用 Pydantic 模型的全部字段创建数据库 Item 对象。

* 更新 Jupyter Lab 安装方式及本地开发工具脚本、环境变量。

## 0.3.0 (2019-04-19)

* PR <a href="https://github.com/tiangolo/full-stack-fastapi-template/pull/14" target="_blank">#14</a>:
    * 更新 CRUD 工具，改进类型使用。
    * 简化 Pydantic 模型名，例如将 `UserInCreate` 改为 `UserCreate`。
    * 升级依赖包。
    * 添加通用 Item 模型、CRUD 工具、接口与测试，便于复制并适配新功能；这些模型比用户模型更简单通用。
    * 更新接口和路径操作，简化代码，使用新工具以及 include_router 的 prefix 和 tags。
    * 更新测试工具。
    * 更新静态检查规则，放宽 vulture 检查以减少误报。
    * 更新迁移，纳入新的 Item 模型。
    * 在项目 README.md 中添加后端入门提示。

* 将 Python 升级至 3.7，Celery 此时也已兼容。 PR <a href="https://github.com/tiangolo/full-stack-fastapi-template/pull/10" target="_blank">#10</a>，作者：<a href="https://github.com/ebreton" target="_blank">@ebreton</a>。

## 0.2.2 (2019-04-11)

* 修复开发模式下前端拦截 /docs 的问题；使用最新 https://github.com/tiangolo/node-frontend 并在前端配置自定义 Nginx。<a href="https://github.com/tiangolo/full-stack-fastapi-template/pull/6" target="_blank">PR #6</a>。

## 0.2.1 (2019-03-29)

* 修复 FastAPI 中按用户 ID 查询的路径操作文档。<a href="https://github.com/tiangolo/full-stack-fastapi-template/pull/4" target="_blank">PR #4</a>，作者：<a href="https://github.com/mpclarkson" target="_blank">@mpclarkson</a>。

* 默认使用 `/start-reload.sh` 覆盖开发环境启动命令。

* 更新生成的 README。

## 0.2.0 (2019-03-11)

**<a href="https://github.com/tiangolo/full-stack-fastapi-template/pull/2" target="_blank">PR #2</a>**：

* 简化并更新后端 `Dockerfile`。
* 重构并简化后端代码，改进命名、导入、模块及命名空间。
* 改进并简化 Vuex 与 TypeScript 访问器的集成。
* 统一前端组件布局、按钮顺序等。
* 添加用于开发项目生成器本身的本地脚本。
* 为启动模块添加日志，及早发现错误。
* 改进要求管理员权限的 FastAPI 依赖工具，简化并减少代码。

## 0.1.2

* 修复更新当前用户的路径操作，将参数设为请求体。

## 0.1.1

自首次发布以来修复了多项问题，包括：

* 调整用户路径操作的顺序。
* 前端使用正确格式发送登录数据。
* 为 CORS 添加 https://localhost 来源变体。
