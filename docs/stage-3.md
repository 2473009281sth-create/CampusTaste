# 阶段 3：Redis 缓存、原子限流与登录增强

当前状态：已验证（2026-09-28）。阶段 3 不修改 PostgreSQL 表结构，因此没有新增 Alembic 迁移。

## 实现范围

- Compose 增加 Redis 8.2、健康检查、持久卷和后端依赖。
- 菜品公开详情使用 Cache Aside，支持短 TTL 空值缓存和随机抖动。
- 缓存未命中时使用带唯一令牌的 Redis 互斥锁重建，Lua 比较令牌后安全释放。
- 未取得重建锁的请求有界等待；超时后直接查询 PostgreSQL。
- 学校和食堂榜单缓存使用学校版本号统一失效。
- 登录按 IP、评价写操作按用户使用 Redis Lua 原子限流。
- Access Token 默认有效期调整为 15 分钟。
- Refresh Token 默认有效期 30 天，使用 JWT `jti` 和 family，Redis 只保存 SHA-256 摘要。
- Refresh Token 每次使用后轮换；旧 Token 重用会撤销整个 family。
- 退出登录撤销 Refresh Token family；已签发 Access Token 不立即撤销，继续有效至 15 分钟过期。
- 缓存查询在 Redis 故障时回源 PostgreSQL；限流、刷新、退出和登录签发在 Redis 故障时返回 503，不静默放行。

## Cache Aside 流程

```text
读取缓存
├── 命中：返回缓存
└── 未命中：尝试取得重建锁
    ├── 成功：查询 PostgreSQL → 写缓存 → 安全释放锁
    └── 失败：有界等待缓存 → 超时后直接查询 PostgreSQL
```

菜品不存在时写入短 TTL 的 `__NULL__` 标记，降低重复查询不存在 ID 造成的缓存穿透。正常值和空值 TTL 都增加随机抖动，减少大量键同时过期。

锁通过 `SET key token NX EX ttl` 获取。释放时 Lua 脚本只在 Redis 中的 token 等于当前持有者 token 时删除，防止旧请求删除已经过期并由其他请求重新获得的锁。锁有租约且等待有上限，因此进程崩溃不会形成永久锁，请求也不会无限等待。

## 缓存一致性边界

评价事务先提交 PostgreSQL，成功后再失效缓存：

```text
Review 与 Dish 聚合 commit
→ 删除菜品详情缓存
→ 递增所属学校 ranking version
```

榜单缓存键包含学校版本：

```text
cache:ranking:school:{school_id}:v{version}:limit:{limit}
cache:ranking:canteen:{canteen_id}:v{version}:limit:{limit}
```

学校任意菜品评分变化都会改变学校平均分 `C`，因此递增学校版本会同时让学校榜单和该校全部食堂榜单的旧键不可达。旧值依赖 TTL 自动清理，不需要扫描删除所有食堂键。

这是提交后失效的最终一致方案，仍存在短窗口：数据库已经提交但 Redis 失效失败时，旧缓存会保留至 TTL 到期。代码记录警告但不回滚已成功的业务事务。阶段 3 的保证是“数据库为真实来源，缓存有界陈旧”，不是强一致。

## Redis 故障策略

| 功能 | Redis 故障行为 | 原因 |
| --- | --- | --- |
| 菜品详情、榜单 | 回源 PostgreSQL | 可用性优先，数据库仍是权威数据源 |
| 缓存失效 | 记录警告，依赖 TTL 收敛 | 业务事务已经提交，不能因缓存故障伪装失败 |
| 登录限流、评价写限流 | 返回 503 | 不能在限流不可判定时静默放行 |
| Refresh 签发、轮换、退出 | 返回 503 | 无法确认令牌状态时必须失败关闭 |

## Refresh Token 轮换

登录返回 `access_token`、`refresh_token` 和 `token_type`。Refresh JWT 包含用户 UUID、`type=refresh`、唯一 `jti`、family、签发时间和过期时间。

Redis 的 `auth:refresh:{jti}` 只保存 Token SHA-256 摘要、用户、family 和状态，不保存完整 Token。轮换由单个 Lua 脚本原子完成：检查旧 Token 摘要和 active 状态、把旧 Token 标记为 rotated、创建唯一后继。两个请求并发刷新时只有一个能从 active 变为 rotated；另一个检测到重用并撤销 family，因此不会得到两个有效后继。

接口：

- `POST /api/v1/login/access-token`：登录并签发 Access/Refresh。
- `POST /api/v1/login/refresh`：使用旧 Refresh 换取新的 Access/Refresh。
- `POST /api/v1/login/logout`：撤销当前 Refresh family。

退出后，Refresh 立即不可用；Access Token 是无状态 JWT，没有 Redis 黑名单，因此最多继续有效 15 分钟。这一语义与实现保持一致。

## 原子限流

Lua 脚本在 Redis 内一次完成 `INCR` 和首次 `EXPIRE`：

```text
计数 <= limit：允许
计数 > limit：返回 429 和 Retry-After
Redis 不可用：返回 503
```

登录键按客户端 IP，评价写键按用户 UUID。当前采用固定 60 秒窗口，边界处允许相邻窗口突发；它不是滑动窗口。

## 验收步骤

先启动依赖：

```bash
cd /home/david/CampusTaste
sudo docker compose up -d --wait db redis mailpit
```

在独立 PostgreSQL 测试库执行：

```bash
cd /home/david/CampusTaste/backend
uv run --locked pytest tests/api/routes/test_stage3_redis_auth.py -v
uv run --locked bash scripts/test.sh "阶段 3 验收"
uv run --locked coverage report --fail-under=90
uv run --locked ruff format app tests --check
uv run --locked ruff check app tests
uv run --locked mypy app
uv run --locked ty check app
```

## 最终验收结果

- 独立 `campustaste_test` PostgreSQL 数据库已升级到 Alembic head。
- 第三阶段专项测试 9 项全部通过，覆盖 Refresh Token 轮换、旧令牌重用撤销、明文不落 Redis、并发刷新、退出语义、缓存命中、Redis 故障回源、空值缓存、热点互斥锁、排行榜失效和原子限流。
- 完整后端测试 83 项全部通过，语句覆盖率 90%。
- Ruff 格式与规则检查、mypy、ty、Compose 配置检查全部通过。
- OpenAPI 共 35 条路径，包含 `/api/v1/login/refresh` 和 `/api/v1/login/logout`。
- 两项警告分别来自模板的 Starlette TestClient 兼容层和开发模式未构建前端目录，不影响本阶段后端验收。
