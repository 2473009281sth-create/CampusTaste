# 性能测试与复现

状态：已实测（2026-10-04），仅对应下述本机只读负载，不代表容量上限。

## 测试场景

使用 Locust 2.46.6，对真实本地 HTTP API 发起只读请求：菜品详情、学校榜单、评价列表的任务权重为 6:3:1。每个用户操作间等待 0.1～0.5 秒；分别运行 10 和 30 个用户，每秒启动 5 个用户，每轮持续 60 秒。持续时间包含升压阶段，第二轮继承第一轮的缓存状态，不用这两轮证明缓存性能提升。

数据库 `campustaste_loadtest`：新增 1 个压测学校、1 个食堂、1 个档口、100 个菜品、100 个普通用户、10000 条评价。初始化还保留原 DEMO 学校等演示数据。每个压测菜品有 100 条评价，分数 1～5 各 20 条，聚合人数为 100、总分为 300。

Redis 使用 DB 14，不清空开发缓存。API 使用单个 Uvicorn 进程；Locust、API 和依赖共享本机。没有评价写入、登录或图片上传负载，不能从结果推断这些路径的容量。

## 运行

```bash
cd backend
uv run --frozen --package app python scripts/run-loadtest.py
```

结果保存于 `backend/loadtests/results/<UTC时间>/`：

- `environment.json`：系统、逻辑 CPU 数、内存、数据规模和负载参数。
- `users-10-summary.json`、`users-30-summary.json`：结束时最终请求数、失败数、RPS、P50/P95。
- `users-10_stats.csv`、`users-30_stats.csv`：定期导出的接口统计快照，可能早于最终统计。
- HTML 报告：各接口结果。
- `api.jsonl`：压测 API 的日志。

## 本次结果

环境为 WSL2 Ubuntu，Linux 6.6.87.2，Intel Core i7-13700H，WSL 可见 20 个逻辑 CPU、约 7.52 GiB 内存。API、压测及依赖共享本机，首轮部分时间还运行了独立数据库上的完整 pytest，属于开发机实测，不是排除背景负载的性能实验。原始报告位于 `backend/loadtests/results/20261004T041327Z/`，采用结束时 summary.json，而非较早 CSV 快照。

缓存沿用了前一次验证负载的状态，未清空；没有做缓存开关对照。每轮配置 `-t 60s`，RPS 使用 Locust 最终统计窗口计算，不能简单用请求数除以配置的 60 秒替代。P50/P95 为 Locust 分桶近似值。

| 用户数 | 持续时间 | 请求数 | 错误率 | RPS | P50 | P95 |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 配置 60 秒 | 1932 | 0%（0 次失败） | 32.85 | 7 ms | 15 ms |
| 30 | 配置 60 秒 | 5591 | 0%（0 次失败） | 96.72 | 7 ms | 17 ms |

Locust 命令语义参考[官方无界面运行文档](https://docs.locust.io/en/stable/running-without-web-ui.html)。本轮没有基线对比，不描述性能提升百分比。
