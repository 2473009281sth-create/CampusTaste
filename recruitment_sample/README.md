# CampusTaste Python 后端招聘代码样例

本样例展示 **Redis 缓存重建与请求限流**：缓存命中时直接返回数据；未命中时用短期互斥锁协调重建；不存在的数据使用短 TTL 的空值缓存；缓存故障时回退到数据源；请求超过固定窗口额度时返回 HTTP 429 和 `Retry-After`。使用 Python、FastAPI、redis-py、Redis Lua、Pydantic Settings、pytest 和 coverage。

## 来源与展示边界

这是从当前 CampusTaste 源码整理的样例，不代表全部项目实现，也不凭此证明个人代码归属。提交招聘方前，请自行确认这些原始代码属于你完成的工作，并符合项目的分享许可。

| 样例文件 | 原项目来源与调整 |
| --- | --- |
| `app/services/cache.py` | 来自 `backend/app/services/cache.py`；保留 `_ttl`、`get_or_build_json` 和锁脚本的原实现，仅移除未使用的 import，以及依赖 SQLModel/菜品模型的排行榜版本与失效函数 |
| `app/services/rate_limit.py` | 完整复制 `backend/app/services/rate_limit.py`，无修改 |
| `app/core/redis.py` | 完整复制 `backend/app/core/redis.py`，无修改 |
| `app/core/config.py` | 新增最小配置适配层；只保留本样例需要的变量，默认值与原项目一致，增加取值范围验证 |
| `app/main.py` | 新增演示入口，使用合成菜品数据，不是原项目生产接口；原限流服务在登录和评论接口中使用 |
| `tests/` | 本次新增的隔离测试和 Fake Redis，不是原项目既有测试 |

未复制原项目数据库、账号、认证、RabbitMQ、Celery、对象存储或生产配置。没有修改原项目业务代码。本样例只展示缓存与限流的独立边界，不宣称展示 PostgreSQL 事务或 Celery。

## 核心设计与限制

- **Cache-aside**：以 `builder` 回调隔离数据源，原项目数据源为 PostgreSQL，演示使用内存合成数据。
- **空值与 TTL 抖动**：`__NULL__` 标记不存在的数据，使用较短 TTL；随机抖动减少同时过期。数据源需返回 JSON 字符串或 `None`，不应将内部空值标记当成普通数据。
- **重建锁**：`SET NX EX` 获取有租期的锁，随机令牌标识持有者，Lua 比较令牌后删除，避免删除其他持有者的锁。获取失败时短暂轮询，超时后自行读取数据源，不写缓存。
- **失败策略**：缓存 Redis 错误回退数据源；限流 Redis 错误返回 503，采取拒绝放行策略。数据源自身错误仍向上传播。演示路由先限流，因此限流服务故障时会直接返回 503，缓存降级通过服务测试验证。
- **原子限流**：Lua 将 INCR、首次 EXPIRE 与 TTL 读取放在一次执行中；计数等于额度仍允许，超出后返回 429，重试时间至少为 1 秒。
- **原实现边界**：租期内未完成重建可能产生重复数据源读取；没有锁续租，也不保证严格单次重建。同步 Redis 调用适用于此处同步 FastAPI 路由。若 `builder` 自身抛 RedisError，原实现某些路径可能重试调用，回调应是无副作用读取。
- 演示接口每 60 秒总计允许 10 次请求，使用全局样例限流键；不包含用户身份认证或生产级多租户限流。

## 目录结构

```text
recruitment_sample/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── redis.py
│   └── services/
│       ├── __init__.py
│       ├── cache.py
│       └── rate_limit.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cache.py
│   ├── test_rate_limit.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── README.md
└── test_log.txt  # 本地生成，Git 忽略，不随仓库上传
```

## 安装

建议使用 Python 3.14（记录的测试环境为 3.14.6）。依赖版本记录在 `requirements.txt`，未锁定全部间接依赖。

```bash
cd recruitment_sample
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

必须从样例目录运行，避免与原项目同名的 `app` 包混用。`.env.example` 只有本机示例 URL 和非敏感数值，不含密码或账号；默认配置即可运行。需要自定义时将其复制为本目录 `.env`；不要提交或打包 `.env`。

## 运行 API

运行 API 需要本地 Redis，测试不需要 Redis。可使用已有本机实例，或启动一次性的本地 Redis：

```bash
docker run --rm --name campustaste-sample-redis -p 127.0.0.1:6379:6379 redis:7-alpine
```

另一个终端在本样例目录激活虚拟环境后执行：

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
curl http://127.0.0.1:8000/dishes/demo-dish
curl http://127.0.0.1:8000/dishes/missing
```

第一条请求返回合成菜品 JSON，第二条返回 404；超过额度返回 429，Redis 不可用返回 503。交互文档位于 `http://127.0.0.1:8000/docs`。Redis 中只使用 `sample:` 前缀样例键（对应锁键另加 `lock:` 前缀）。

## 测试过程与日志

```bash
python -m pytest -vv -p no:cacheprovider
```

本次在项目已有虚拟环境中，从样例目录运行 coverage 包裹的 pytest；未安装额外依赖。本地 `test_log.txt`（不随仓库上传）保存执行时间（Asia/Shanghai）、Python 版本、命令、逐项测试输出、退出码和覆盖率结果。复现并保存日志可执行：

```bash
python -m coverage run --branch --source=app -m pytest -vv -p no:cacheprovider > test_log.txt 2>&1
python -m coverage report -m >> test_log.txt 2>&1
```

测试覆盖：缓存命中/空值命中；重建与 TTL 抖动；短期空值缓存；锁释放与令牌所有权；锁争用等待、超时与等待中故障；读取、加锁、写入、释放锁失败降级；数据源异常；限流边界、键隔离、Retry-After 下限及 503；FastAPI 的 200、404、429、503 响应与重复请求缓存行为。

测试全部使用 Fake Redis 和合成数据，模拟时间避免真实等待。Fake 根据脚本标识模拟效果，不执行 Lua、不模拟真实租期到期，不证明 Redis 实际原子性、网络行为或并发正确性；这些仍需真实 Redis 集成测试。Redis 连接适配器也不在本次外部服务验证范围内。

2026-10-07 本地验证结果（本次文档整理未重跑）：**23 项测试全部通过**，包含分支的总体覆盖率为 **98%**；缓存服务为 98%，限流服务与演示入口为 100%。未覆盖真实 Redis 连接及等待循环的重复轮询分支。存在 1 条 Starlette 对 httpx TestClient 的弃用警告，不影响本次结果。受限沙箱中的 TestClient 测试卡住并被中断，随后在沙箱外完成全部隔离测试；这项环境限制也记入日志。

## 敏感信息与交付

样例未包含原项目 `.env`、真实账号、Cookie、访问令牌、JWT Secret、API Key、真实数据库密码或生产主机配置。锁令牌在运行时随机生成，不是账户凭据。测试输出只含合成数据及文件名。交付时排除本地 `.env`、虚拟环境、缓存与 coverage 数据文件；GitHub 仓库保留上述测试摘要，`test_log.txt` 与重复 ZIP 仅保留在本地。

已检查交付文件与常见私钥、API Key、JWT、带密码的连接 URL 模式，未发现凭据；样例保留的两个完整复制文件已逐字节核对，缓存核心函数已核对 AST 一致。日志含本机工作目录路径，不含账号登录信息；如果不希望暴露本机目录名，可在分享前将路径匿名化。模式扫描不能保证发现所有形式的敏感内容；以后添加数据或配置时应重新检查。
