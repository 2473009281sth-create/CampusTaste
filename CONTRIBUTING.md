# 贡献指南

本文为 Full Stack FastAPI Template 上游贡献规范的中文说明。它描述向上游提交贡献的要求，不代表 CampusTaste 当前阶段已授权提交 PR 或发布代码。

## 重大修改先讨论

涉及新功能、架构调整或较大重构时，请先发起 [GitHub Discussion](https://github.com/fastapi/full-stack-fastapi-template/discussions)，让社区和维护者在投入大量实现工作前评估方案。

以下小型、明确的修改可以直接提交 PR：

- 拼写与语法修正。
- 小范围且可复现的问题修复。
- 静态检查警告或类型错误修复。
- 删除未使用代码等轻量改进。

上游不允许非团队成员通过 PR 修改 `pyproject.toml` 或 `uv.lock`，以降低供应链风险。需要新增依赖时，请先发起 [Discussion](https://github.com/fastapi/full-stack-fastapi-template/discussions) 说明原因。

## 开发环境

环境配置、服务启动、静态检查和提交前钩子等说明见[开发指南](development.md)。

## 提交 PR

1. 提交前确保测试通过。
2. 一个 PR 聚焦一项修改。
3. 修改功能时同步更新测试。
4. 在 PR 描述中引用相关问题。

## 自动化代码与 AI

上游允许使用包括 AI/大语言模型在内的工具，但贡献必须包含有意义的人工判断、理解与审核。

如果贡献者投入的人工工作（例如编写提示词）少于维护者审核该 PR 所需的工作，请不要提交。维护者本身也能运行自动化工具，直接使用工具可能比审核低质量的外部提交更省时。

### 自动生成的 PR 与评论

上游可能标记并关闭看起来由 AI 或类似自动化工具生成、缺乏人工参与的 PR。评论和描述同样适用，请不要直接粘贴大语言模型生成的内容。

### 避免消耗维护者精力

用极少的自动化成本批量提交需要仔细审查的 PR 或评论，会造成类似[拒绝服务攻击](https://en.wikipedia.org/wiki/Denial-of-service_attack)的人工负担。请勿这样做；反复发送此类内容的账号可能被封禁。

### 合理使用工具

借用本叔叔的话：

> ~~能力~~ **工具**越强，责任越大。

请审慎使用工具，避免无意中造成伤害，使贡献对项目有所帮助。

## 提问

有关向上游贡献的问题，请发起 [GitHub Discussion](https://github.com/fastapi/full-stack-fastapi-template/discussions)。
