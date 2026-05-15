# SQLGuard — AI SQL Review Tool

**Web MVP Built 2026-05-15** · 技术 VALIDATED · 商业部署待完成

## 产品说明

SQLGuard 是一个基于规则引擎的 SQL 风险审核工具，帮助开发者发现 SQL 中的性能问题和安全风险。

**核心功能：**
- 粘贴 SQL → 即时获取风险报告（无需数据库连接）
- 8 条审核规则覆盖常见反模式
- 风险分级（🔴 HIGH / 🟡 MEDIUM / 🟢 LOW）
- 永久免费基础版

**技术栈：**
- 后端：FastAPI + Python（无外部依赖）
- 前端：纯 HTML/CSS/JS（无框架）
- 部署：Railway（`railway.toml` 已配置）

## 快速体验

```bash
# 本地运行
cd 003-sql-review-tool
python web_app.py
# 打开 http://localhost:18765
```

## 审核规则

| 规则 | 类型 | 说明 |
|------|------|------|
| SQL001 | 🟡 MEDIUM | SELECT * 检测 |
| SQL002 | 🟡 MEDIUM | SELECT 无 LIMIT |
| SQL003 | 🔴 HIGH | LIKE 前通配符（无法使用索引）|
| SQL004 | 🔴 HIGH | 相关子查询 |
| SQL005 | 🔴 HIGH | UPDATE/DELETE 无 WHERE |
| SQL006 | 🟡 MEDIUM | 多个 OR 条件 |
| SQL007 | 🟡 MEDIUM | 隐式类型转换 |
| SQL008 | 🟢 LOW | 全表扫描风险 |

## 定价

| 方案 | 价格 | 说明 |
|------|------|------|
| Free | 永久免费 | 基础审核功能 |
| Pro | 99元/人/月 | 无限次审核 + AI 优化建议 |
| Team | 299元/人/月 | 团队协作 + Git 集成 |

## 部署状态

| 项目 | 状态 |
|------|------|
| 本地运行 | ✅ 已验证（2026-05-15）|
| Railway 配置 | ✅ `railway.toml` 已就绪 |
| GitHub 仓库 | ⏳ 待创建 |
| 正式部署 | ⏳ 待李梓浩完成 OAuth |

## 部署步骤（李梓浩操作，5分钟）

### 方案 A：Railway Dashboard（推荐）
1. 打开 https://railway.app
2. Login with GitHub
3. New Project → Deploy from GitHub → 选择 `sql-review-tool`
4. 等待 2 分钟，获得 `*.railway.app` URL

### 方案 B：获取 Railway API Token
1. 打开 https://railway.app/account
2. New Token → 复制 Token（格式：`rail_xxx`）
3. 把 Token 发给 Hermes → 我执行 `railway up` 完成部署

## 竞品对比

| 产品 | 定价 | Web界面 | AI优化建议 | 中文支持 |
|------|------|---------|-----------|---------|
| Yearning | 免费 | ✅ | ❌ | ✅ |
| DataGrip | 16元/月 | ❌ | ❌ | ❌ |
| 阿里云SQL优化 | 企业询价 | ✅ | ✅ | ✅ |
| **SQLGuard** | 免费/99元/月 | ✅ | ⏳ | ✅ |

## 下一步

1. [ ] 李梓浩完成 Railway OAuth 部署
2. [ ] 发布到掘金/V2EX 获取第一批用户
3. [ ] 验证付费意愿
4. [ ] 开发 Pro 版 AI 优化建议功能

## Verdict: READY TO SHIP

技术验证完成，MVP 已就绪。唯一阻塞：部署授权。
