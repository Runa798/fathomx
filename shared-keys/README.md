# 共享 API Keys

本文档说明 `shared-keys/` 目录的用途和结构。实际 key 文件不提交到 git，请通过私密渠道单独分享。

## 目录结构

```
shared-keys/
├── README.md        ← 本文件（已纳入 git）
├── .gitignore       ← 忽略所有 key 文件（已纳入 git）
├── tavily-pool.md   ← Tavily 号池接入信息（不提交，私密分享）
└── grok2api.md      ← Grok2API 接入信息（不提交，私密分享）
```

## 使用方法

1. 通过私密渠道获取 `tavily-pool.md` 和 `grok2api.md`，放入本目录
2. 根据文件内容，将对应 key 填入项目根目录的 `.env` 文件：

```env
GROK_API_URL=https://grok.heyerice33.win/v1
GROK_API_KEY=<从 grok2api.md 获取>

TAVILY_API_URL=https://tavily.heyerice33.win
TAVILY_API_KEY=<从 tavily-pool.md 获取>

EXA_API_KEY=<可选，自行申请>
```

3. 运行 `./install.sh` 安装

## 可用服务

### Tavily 号池

- 详见 [tavily-pool.md](tavily-pool.md)（私密文件，不在 git 中）
- 作用：为 GrokSearch MCP 提供 Tavily 补充搜索能力
- 号池内有 149 个 Tavily API Key，自动轮换，无需担心限速

### Grok2API

- 详见 [grok2api.md](grok2api.md)（私密文件，不在 git 中）
- 作用：提供 Grok 模型访问，供 GrokSearch MCP 调用
- 兼容 OpenAI API 格式，支持 grok-3 等模型

## 注意事项

- 这些 key 是共享资源，**请合理使用，避免滥用**
- 如遇到 rate limit，等待一会儿再试
- **绝对不要** 将 key 提交到任何公开仓库
- `.gitignore` 已配置忽略所有 `*.md`（README.md 除外）和敏感文件
