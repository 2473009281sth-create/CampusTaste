# 阶段 2 数据字典

本文对应迁移 `d2b3c4d5e6f7`。所有主键使用 UUID，时间存储为带时区的 UTC 时间；金额使用 `NUMERIC(10, 2)`。

## 用户角色

`user.role` 使用枚举：

| 值 | 权限 |
| --- | --- |
| `USER` | 浏览公开数据、提交菜品、管理自己待审核的菜品 |
| `REVIEWER` | 普通用户能力，加上查看待审核列表以及通过、拒绝菜品 |
| `ADMIN` | 维护学校、食堂、档口、分类、菜品和用户角色；直接创建公开菜品 |

模板原有 `is_superuser` 暂时保留。管理员满足 `role=ADMIN` 或 `is_superuser=true`；初始化和用户管理逻辑会让新管理员同时满足两者，兼容模板已有接口。后续若移除兼容字段，需要单独迁移和调整前端。

## `school` 学校

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `name` | VARCHAR(100) | 非空，学校名称 |
| `code` | VARCHAR(32) | 非空，全局唯一的稳定代码 |
| `is_active` | BOOLEAN | 非空；停用后不出现在公开列表 |
| `created_at` | TIMESTAMPTZ | 非空，创建时间 |

## `canteen` 食堂

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `school_id` | UUID | 非空，外键指向 `school.id` |
| `name` | VARCHAR(100) | 非空；同一学校内唯一 |
| `address` | VARCHAR(255) | 可空，校内地址 |
| `is_active` | BOOLEAN | 非空，公开状态 |
| `created_at` | TIMESTAMPTZ | 非空，创建时间 |

索引 `ix_canteen_school_active(school_id, is_active)` 支持按学校查询可用食堂。

## `stall` 档口

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `canteen_id` | UUID | 非空，外键指向 `canteen.id` |
| `name` | VARCHAR(100) | 非空；同一食堂内唯一 |
| `floor` | VARCHAR(32) | 可空，例如 `1F` |
| `location` | VARCHAR(255) | 可空，档口位置说明 |
| `is_active` | BOOLEAN | 非空；停用档口不能接收新菜品 |
| `created_at` | TIMESTAMPTZ | 非空，创建时间 |

索引 `ix_stall_canteen_active(canteen_id, is_active)` 支持按食堂查询可用档口。

## `category` 菜品分类

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `name` | VARCHAR(50) | 非空，全局唯一 |
| `is_active` | BOOLEAN | 非空；停用分类不能用于新菜品 |
| `created_at` | TIMESTAMPTZ | 非空，创建时间 |

分类独立于学校，便于跨学校统一筛选。菜品引用分类时允许为空；删除分类时数据库将菜品 `category_id` 置空。

## `dish` 菜品

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `stall_id` | UUID | 非空，外键指向所属档口 |
| `category_id` | UUID | 可空，外键指向分类，删除分类时置空 |
| `submitted_by_id` | UUID | 非空，外键指向提交用户，由服务端填写 |
| `name` | VARCHAR(100) | 非空，菜品名称 |
| `description` | VARCHAR(1000) | 可空，菜品说明 |
| `price` | NUMERIC(10,2) | 非空，检查约束 `price >= 0` |
| `status` | `dishstatus` | 非空，审核状态 |
| `review_note` | VARCHAR(500) | 可空；拒绝时必须由服务层提供原因 |
| `reviewed_by_id` | UUID | 可空，外键指向审核人；删除审核人时置空 |
| `reviewed_at` | TIMESTAMPTZ | 可空，审核时间 |
| `published_at` | TIMESTAMPTZ | 可空，公开时间 |
| `created_at` | TIMESTAMPTZ | 非空，创建时间 |
| `updated_at` | TIMESTAMPTZ | 非空，最后修改时间 |
| `rating_sum` | INTEGER | 非空且不小于 0，有效评分总和 |
| `rating_count` | INTEGER | 非空且不小于 0，有效评分人数 |

状态枚举：

| 值 | 含义 |
| --- | --- |
| `PENDING` | 普通用户提交，等待审核 |
| `PUBLISHED` | 审核通过或管理员直接创建，可公开查询 |
| `REJECTED` | 审核拒绝，不公开 |

索引：

- `ix_dish_stall_status_created(stall_id, status, created_at)`：按档口查询公开菜品。
- `ix_dish_submitter_status(submitted_by_id, status)`：查询用户提交记录。
- `ix_dish_status(status)`：待审核列表。

阶段 1 只允许 `PENDING → PUBLISHED` 或 `PENDING → REJECTED`。已审核菜品不能再次审核；普通用户只能修改本人仍处于 `PENDING` 的菜品。

## `review` 评价

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `user_id` | UUID | 非空，外键指向评价作者 |
| `dish_id` | UUID | 非空，外键指向已发布菜品 |
| `rating` | INTEGER | 非空，数据库检查范围 1～5 |
| `content` | VARCHAR(2000) | 可空，评价正文 |
| `is_deleted` | BOOLEAN | 非空，用户软删除状态 |
| `is_hidden` | BOOLEAN | 非空，审核隐藏状态；阶段 4 接入治理接口 |
| `like_count` | INTEGER | 非空且不得小于 0，当前有效点赞数 |
| `deleted_at` | TIMESTAMPTZ | 可空，用户删除时间 |
| `created_at` | TIMESTAMPTZ | 非空，创建时间，也是游标第一排序键 |
| `updated_at` | TIMESTAMPTZ | 非空，最后修改时间 |

约束与索引：

- `uq_review_user_dish(user_id, dish_id)`：同一用户对同一菜品只保留一条记录；删除后通过恢复复用原记录。
- `ck_review_rating_range`：数据库最终保证评分处于 1～5。
- `ck_review_like_count_nonnegative`：点赞聚合不得小于 0。
- `ix_review_dish_visible_created(dish_id, is_deleted, is_hidden, created_at, id)`：支持公开评价过滤和稳定游标分页。
- `ix_review_user_created(user_id, created_at)`：支持后续个人评价查询。

只有 `is_deleted=false AND is_hidden=false` 的评价计入 `dish.rating_sum` 和 `dish.rating_count`。两个状态相互独立：用户恢复软删除记录不会解除审核隐藏，编辑隐藏评价也不会重新计分。

## `reviewlike` 评价点赞

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `user_id` | UUID | 非空，外键指向点赞用户 |
| `review_id` | UUID | 非空，外键指向评价 |
| `created_at` | TIMESTAMPTZ | 非空，点赞创建时间 |

- `uq_review_like_user_review(user_id, review_id)`：同一用户对同一评价最多一条点赞关系，是并发防重的最终保障。
- `ix_review_like_review_created(review_id, created_at)`：支持按评价查询点赞。
- 点赞接口接收目标状态 `liked=true/false`；重复设置相同状态不会重复增减 `review.like_count`。

## `reviewreport` 评价举报

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `reporter_id` | UUID | 非空，外键指向举报用户，由服务端从当前身份写入 |
| `review_id` | UUID | 非空，外键指向被举报评价 |
| `reason` | ENUM | `SPAM`、`ABUSE`、`FALSE_INFORMATION`、`OTHER` |
| `details` | VARCHAR(1000) | 可空，举报补充说明 |
| `status` | ENUM | `PENDING`、`RESOLVED`、`DISMISSED` |
| `resolution_note` | VARCHAR(1000) | 可空，处理说明 |
| `handled_by_id` | UUID | 可空，外键指向处理人；用户删除时置空 |
| `handled_at` | TIMESTAMPTZ | 可空，处理时间 |
| `created_at` | TIMESTAMPTZ | 非空，举报时间 |

- `uq_review_report_reporter_review(reporter_id, review_id)`：同一用户不能重复举报同一评价。
- `ix_review_report_status_created(status, created_at, id)`：支持审核队列。
- 举报处理只能从 `PENDING` 进入 `RESOLVED` 或 `DISMISSED`；重复处理返回冲突。

## `moderationaudit` 管理审计

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键 |
| `actor_id` | UUID | 可空，外键指向审核员或管理员；用户删除后审计仍保留 |
| `action` | ENUM | 隐藏、取消隐藏、举报成立或举报驳回 |
| `review_id` | UUID | 非空，被治理评价 |
| `report_id` | UUID | 可空，关联举报；举报删除后置空 |
| `previous_hidden` | BOOLEAN | 操作前隐藏状态 |
| `new_hidden` | BOOLEAN | 操作后隐藏状态 |
| `note` | VARCHAR(1000) | 可空，处理说明 |
| `created_at` | TIMESTAMPTZ | 非空，审计时间 |

举报处理、评价可见性、评分聚合和审计记录在同一个 PostgreSQL 事务中提交。所有治理写操作统一按照 `Dish → Review → ReviewReport` 顺序加行锁，避免与用户改分、删除或恢复产生聚合偏差。

## `imageasset` 图片资源

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键，同时用于生成服务端对象名 |
| `owner_id` | UUID | 非空，外键指向上传用户，由 Access Token 身份写入 |
| `dish_id` | UUID | 可空，关联菜品 |
| `review_id` | UUID | 可空，关联评价 |
| `original_object_key` | VARCHAR(500) | 非空且唯一，MinIO 原图对象名 |
| `thumbnail_object_key` | VARCHAR(500) | 可空，缩略图成功后填写 |
| `content_type` | VARCHAR(100) | 根据实际解码格式确定，不信任文件名和请求头 |
| `byte_size` | INTEGER | 非空且大于 0，原图字节数 |
| `width`、`height` | INTEGER | 非空且大于 0，解码后的原图尺寸 |
| `status` | ENUM | `PENDING`、`PROCESSING`、`READY`、`FAILED` |
| `error_message` | VARCHAR(1000) | 可空，处理失败原因 |
| `created_at`、`updated_at` | TIMESTAMPTZ | 创建时间和最后状态更新时间 |

检查约束 `ck_image_asset_one_target` 要求 `dish_id` 与 `review_id` 恰好填写一个，防止图片没有归属或同时绑定两个资源。对象桶保持私有，接口只在资源可见或当前用户具有所有者、审核权限时签发短时 GET URL。

## `imageprocessingjob` 图片处理任务

| 字段 | 类型 | 约束与含义 |
| --- | --- | --- |
| `id` | UUID | 主键，也是 Celery 任务参数 |
| `image_id` | UUID | 非空且唯一，外键指向图片，图片物理删除时级联删除任务 |
| `status` | ENUM | `PENDING`、`PROCESSING`、`SUCCEEDED`、`FAILED` |
| `attempts` | INTEGER | 非空且不小于 0，实际开始处理的次数 |
| `next_attempt_at` | TIMESTAMPTZ | 下次允许补偿投递的时间 |
| `dispatched_at` | TIMESTAMPTZ | 最近成功投递 RabbitMQ 的时间 |
| `finished_at` | TIMESTAMPTZ | 成功或永久失败时间 |
| `last_error` | VARCHAR(1000) | 可空，最近一次错误摘要 |
| `created_at`、`updated_at` | TIMESTAMPTZ | 创建时间和最后状态更新时间 |

任务记录先与图片记录一起提交，再尝试投递 RabbitMQ。投递失败时记录仍保持 `PENDING`，Celery Beat 定期扫描并补偿投递；缩略图使用固定对象名，重复执行只会覆盖同一对象并返回已完成状态。

## 评分和榜单规则

平均分按 `rating_sum / rating_count` 推导，零评分菜品平均分显示为 0。学校或食堂榜单使用：

```text
score = v / (v + m) × R + m / (v + m) × C
```

- `R`：菜品平均分。
- `v`：菜品有效评分人数。
- `C`：菜品所属学校全部有效评分的平均值；食堂榜单也使用所属学校的 `C`。
- `m`：配置 `RANKING_PRIOR_WEIGHT`，默认 10，不是准入门槛。
- 学校无任何有效评分时 `C=0`；零评分菜品在 `m>0` 时加权分等于 `C`。
- 并列时依次按有效评分人数、平均分降序，再按菜品 UUID 升序，保证结果稳定。
