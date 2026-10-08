# 阶段 2：评价、评分一致性与榜单

当前状态：已验证（2026-09-26）。开发库、独立测试库和临时迁移库均使用真实 PostgreSQL 18.6；迁移、专项并发测试、完整回归测试、覆盖率和静态检查全部通过。

## 实现范围

- 已发布菜品的评价创建、修改、用户软删除和恢复。
- `(user_id, dish_id)` 唯一约束，删除后恢复原记录，不能重复创建。
- 用户删除与审核隐藏两个独立状态；阶段 2 预留隐藏字段，治理接口留到阶段 4。
- Dish 维护 `rating_sum` 和 `rating_count`，平均分按需推导。
- 所有评分写操作统一锁定顺序：先锁 Dish，再锁 Review。
- 评价列表使用 `(created_at, id)` 降序游标分页。
- 学校和食堂加权榜单，学校平均分作为先验均值。
- 评分聚合校验和修复命令。
- 真实 PostgreSQL 并发测试代码覆盖多用户同时评分、同用户并发首次评分和并发改分。

## 事务与加锁

所有写操作使用同一个数据库事务：

```text
锁定 Dish 行
→ 锁定或查询 Review
→ 修改 Review
→ 按差值修改 rating_sum/rating_count
→ commit
```

先锁 Dish 的作用是把同一道菜的聚合修改串行化，避免多个事务同时读取旧聚合后互相覆盖。Review 行锁解决同一评价修改、删除、恢复之间的竞争。唯一约束是并发首次创建的最终防线；服务层的预查询只负责提供更清晰的 409 响应，不能代替约束。

事务失败时不会只保存评价或只保存聚合。接口没有无限重试；唯一冲突直接返回 409。

## 接口

- `GET /api/v1/dishes/{dish_id}/reviews`：公开有效评价，游标分页。
- `POST /api/v1/dishes/{dish_id}/reviews`：当前用户创建评价。
- `PATCH /api/v1/reveiws/{review_id}`：作者修改评价。
- `DELETE /api/v1/reviews/{review_id}`：作者软删除评价。
- `POST /api/v1/reviews/{review_id}/restore`：作者恢复评价。
- `GET /api/v1/rankings/schools/{school_id}`：学校榜单。
- `GET /api/v1/rankings/canteens/{canteen_id}`：食堂榜单。

游标只编码最后一条记录的 `created_at` 和 `id`，不包含用户输入 SQL。游标分页保证稳定排序和避免偏移扫描，但不自动提供快照一致性：翻页期间新增、删除或恢复评价仍会改变后续可见集合。

## 聚合校验与修复

只校验，不一致时退出码为 1：

```bash
cd /home/david/CampusTaste/backend
uv run python -m app.rebuild_rating_stats
```

修复为评价表重新计算的结果：

```bash
uv run python -m app.rebuild_rating_stats --repair
```

命令逐个锁定 Dish，按未删除且未隐藏的评价重算总分和人数。修复模式在事务中写回。

## 验收命令

先由有 Docker 权限的用户启动 PostgreSQL：

```bash
cd /home/david/CampusTaste
sudo docker compose up -d --wait db mailpit
```

然后执行：

```bash
cd /home/david/CampusTaste/backend
uv run --locked alembic upgrade head
uv run --locked alembic current
uv run --locked pytest tests/api/routes/test_reviews_rankings.py -v
uv run --locked bash scripts/test.sh "阶段 2 验收"
uv run --locked coverage report --fail-under=90
uv run --locked ruff format app tests --check
uv run --locked ruff check app tests
uv run --locked mypy app
uv run --locked ty check app
```

还需要在独立临时 PostgreSQL 数据库验证：

```text
upgrade c1a2b3d4e5f6 → upgrade d2b3c4d5e6f7
→ downgrade c1a2b3d4e5f6
→ upgrade d2b3c4d5e6f7
```

不得在开发数据库上运行会清理数据的完整测试。

## 最终验证记录

- 开发数据库升级至 `d2b3c4d5e6f7 (head)`，评分聚合校验为 0 个不一致。
- 独立 `campustaste_test` 数据库完成迁移，阶段 2 专项测试 7 项全部通过。
- 完整后端测试 74 项全部通过，2 个上游警告，耗时 8.55 秒。
- 语句覆盖率 90%，`coverage report --fail-under=90` 通过。
- Ruff、Ruff format、mypy 严格检查、ty 全部通过。
- FastAPI OpenAPI 成功生成 33 条路径，新评价和榜单路径存在。
- 临时 PostgreSQL 数据库完成全量升级、降级至 `c1a2b3d4e5f6`、再次升级至 `d2b3c4d5e6f7`，并确认 `review` 表和 `dish.rating_sum` 存在；临时库随后删除。
- 开发库确认 `uq_review_user_dish`、`ck_review_rating_range` 以及两个评价查询索引存在。
- 并发测试最初发现 SQLAlchemy Session 身份映射复用旧 Review 实体导致评分差值重复的问题。实现改为锁前只读取不可变 ID 标量、锁 Dish 后再加载并锁定 Review 最新行；修复后多用户同时评分、同用户并发首次评分和并发改分均通过。

两项警告分别来自模板的 Starlette TestClient 兼容层和未构建的前端目录，不影响阶段 2 后端验收。阶段 3 未开始。
