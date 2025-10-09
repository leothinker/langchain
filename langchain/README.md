1. 上周二说的 langgraph 子图使用 Send api 收尾工作
2. 上周：新的 annexx 部署在 eiq 服务器（docker 和非 dockers 版本）
3. 一些其他 bug 的修复，以及从 technical-dd 分支合并过来的改动
4. 讨论客服 agent 的需求

# sfd

1. 调研 openapisearch 从 openapi 文档映射到 mcp 的工具，使用 mcp-adapter（已跑通，方便将来使用）
2. 放弃 openapisearch ，使用 openai 官方 openapi agent，一个文档作为一整个 tool（已跑通）
3. 定制 tool，一个文档中的每个 endpoint 作为一个 tool（已跑通）
4. 该功能集成到 客服 agent 中（进行中）
