# 演示路径与接口索引

## 准备

按 [阶段 6](stage-6.md) 启动后端演示栈，打开 `http://localhost:8000/docs`。初始化会创建 `.env` 指定的管理员以及 DEMO 学校、第一食堂、家常菜档口、主食分类和番茄炒蛋盖饭。不要将真实管理员密码、令牌写入文档或截图。

登录接口提交的是表单 `username`、`password`，不是 JSON；`username` 对应邮箱。在 Swagger 的 Authorize 中输入邮箱和密码即可使用 Access Token。Refresh Token 的轮换与退出需要调用单独接口，当前模板前端没有完成这套校园业务交互。

## 一次完整演示

1. 用 `/api/v1/users/signup` 创建两个演示普通用户，通过管理员的 `PATCH /api/v1/users/{user_id}` 将其中一个设为审核员（`role: reviewer`）。普通用户不能自行指定角色。
2. 浏览学校、食堂和档口，记录档口 ID。普通用户提交菜品，状态为 `pending`；公开详情不能查询到它。
3. 审核员查询待审核列表，调用菜品审核接口，提交 `{"status":"published","review_note":"信息完整"}`。普通用户再次查询，菜品公开。
4. 普通用户创建 `{"rating":5,"content":"份量足，口味不错"}` 的评价；修改为 4 分，查看菜品聚合及榜单。重复创建同用户同菜品评价会冲突。
5. 用另一个普通用户点赞两次，重复 `{"liked":true}` 不会重复加计数；提交 `{"liked":false}` 取消点赞。
6. 另一用户举报评价，审核员处理举报并隐藏评价；查看审计及评分统计。评价隐藏与用户删除是不同状态，用户编辑不能解除审核隐藏。
7. 上传者使用图片上传接口的 `file` 字段上传静态 PNG/JPEG/WebP；查询图片状态，等待 `ready`，申请缩略图 URL 并打开。普通用户不能查看其他人的隐藏评价图片。
8. 查询存活及就绪接口，查看返回头 `X-Request-ID` 和同一 ID 的应用 JSON 日志。

每次修改后使用接口返回的真实 ID，不需要用户手动编造 UUID。演示数据保存在开发库，不使用测试库。若评价已存在，演示修改或恢复，不重复创建。

## 核心接口

以下路径统一以 `/api/v1` 为前缀；完整参数与响应以 OpenAPI 为准。

| 方法与路径 | 用途 | 身份 |
| --- | --- | --- |
| POST `/login/access-token` | 表单登录 | 未登录 |
| POST `/login/refresh`、`/login/logout` | 刷新轮换、撤销刷新令牌 | 持有 Refresh Token |
| GET `/schools`、`/canteens`、`/stalls`、`/categories` | 查询目录 | 公开 |
| POST/PATCH 目录接口 | 维护学校、食堂、档口、分类 | 管理员 |
| POST `/dishes/` | 提交菜品 | 登录用户 |
| GET `/dishes/pending` | 待审核列表 | 审核员、管理员 |
| POST `/dishes/{id}/review` | 通过或拒绝 | 审核员、管理员 |
| GET `/dishes/{id}` | 已发布菜品详情 | 公开 |
| GET/POST `/dishes/{id}/reviews` | 浏览、创建评价 | 浏览公开，创建需登录 |
| PATCH/DELETE `/reviews/{id}` | 修改、软删除 | 评价作者 |
| POST `/reviews/{id}/restore` | 恢复评价 | 评价作者 |
| PUT `/reviews/{id}/like` | 设置点赞目标状态 | 登录用户 |
| POST `/reviews/{id}/reports` | 举报 | 登录用户 |
| GET `/reports`、`/moderation/audits` | 举报队列、审计 | 审核员、管理员 |
| POST `/reports/{id}/resolve` | 处理举报 | 审核员、管理员 |
| PUT `/reviews/{id}/visibility` | 设置隐藏状态 | 审核员、管理员 |
| GET `/rankings/schools/{id}`、`/rankings/canteens/{id}` | 加权榜单 | 公开 |
| POST `/dishes/{id}/images`、`/reviews/{id}/images` | 上传图片 | 登录且满足资源权限 |
| GET `/images/{id}` | 图片状态 | 登录且有查看权限 |
| GET `/images/{id}/original-url`、`/thumbnail-url` | 临时图片链接 | 同上 |
| POST `/images/{id}/retry` | 失败图片重试 | 上传者、审核员、管理员 |
| GET `/image-jobs/failed` | 失败图片列表 | 审核员、管理员 |
| GET `/utils/health-check/`、`/utils/ready/` | 存活、就绪 | 无需登录 |

常见错误：401 为认证失败，403 为权限不足，404 为资源不存在或不公开，409 为状态或唯一约束冲突，422 为输入校验失败，429 为限流，503 为依赖不可用。具体错误码以对应接口实现为准。
