# 阶段 4：点赞、举报与内容治理闭环

当前状态：已验证（2026-10-01）。

## 实现范围

- `PUT /api/v1/reviews/{review_id}/like` 使用 `liked=true/false` 设置目标状态，不使用重试会反转结果的 toggle。
- `reviewlike` 使用 `(user_id, review_id)` 唯一约束，`Review.like_count` 与关系变化在同一事务内维护。
- 普通用户可以举报公开可见评价；举报人从 Access Token 身份写入，不能由请求体伪造。
- 同一用户对同一评价只允许一条举报，数据库唯一约束负责并发最终防重。
- 审核员和管理员可以读取举报队列，将待处理举报标记为成立或驳回。
- 举报成立时可以在同一事务中隐藏评价、扣减 Dish 评分聚合并写入管理审计。
- 审核员和管理员可以通过目标状态接口直接隐藏或取消隐藏评价；重复设置相同状态不重复修改评分或写审计。
- 用户删除状态与审核隐藏状态保持独立。隐藏期间用户改分不会重新计分，取消隐藏时使用评价当前评分重新加入聚合。
- 治理并发统一按照 `Dish → Review → ReviewReport` 加锁，与评价修改、删除和恢复的既有顺序一致。
- 数据库提交成功后失效菜品详情和全校排行榜缓存。
- 评分聚合修复命令在修复后同步失效相关缓存。

## 数据表和约束

- `review.like_count`：非负点赞聚合。
- `reviewlike`：点赞关系，唯一约束 `uq_review_like_user_review`。
- `reviewreport`：举报原因、状态、处理人和处理时间，唯一约束 `uq_review_report_reporter_review`。
- `moderationaudit`：执行人、动作、评价、可选举报来源、前后隐藏状态和处理说明。

详细字段见 `docs/data-dictionary.md`，关系见 `docs/er-diagram.md`。迁移为 `e3c4d5e6f7a8`。

## 事务和幂等边界

点赞接口表达目标状态：

```text
liked=true  + 已点赞   → 不变
liked=true  + 未点赞   → 创建关系，like_count + 1
liked=false + 已点赞   → 删除本人关系，like_count - 1
liked=false + 未点赞   → 不变
```

隐藏状态变化：

```text
可见且未删除 → 隐藏：评分总和减去当前评分，人数减一
隐藏且未删除 → 取消隐藏：评分总和加回当前评分，人数加一
已软删除评价：隐藏状态可独立变化，但不影响评分聚合
```

举报处理、隐藏状态、Dish 聚合和审计记录使用同一个 PostgreSQL commit。缓存失效发生在 commit 之后，沿用阶段 3 的最终一致性边界。

## 验收命令

```bash
cd /home/david/CampusTaste
sudo docker compose up -d --wait db redis mailpit

cd backend
uv run alembic upgrade head
uv run pytest tests/api/routes/test_stage4_governance.py -v
uv run coverage run -m pytest tests/
uv run coverage report --fail-under=90
```

## 最终验收结果

- 开发库和独立 `campustaste_test` 测试库均升级至 `e3c4d5e6f7a8 (head)`。
- 临时 PostgreSQL 数据库完成从空库升级到 head、降级到 `d2b3c4d5e6f7`、再次升级到 head 的迁移往返。
- `alembic check` 通过，SQLModel 元数据与迁移没有未生成差异。
- 第四阶段专项测试 4 项全部通过，覆盖点赞目标状态幂等、用户点赞归属、并发重复点赞、重复举报、普通用户越权拒绝、举报处理、隐藏与取消隐藏、管理审计、隐藏期间改分和改分/隐藏并发。
- 完整后端 87 项测试全部通过，语句覆盖率 90%。
- Ruff 格式与规则检查、mypy、ty、Compose 配置检查全部通过。
- OpenAPI 共 41 条路径，点赞、举报队列、举报处理、评价可见性和审计查询接口均存在。
- 两项警告分别来自模板的 Starlette TestClient 兼容层和开发模式未构建前端目录，不影响后端验收。
