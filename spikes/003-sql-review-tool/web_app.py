"""
SQLGuard — AI SQL Review Tool Web MVP
FastAPI + uvicorn, zero external JS dependencies.
"""

from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from analyzer import analyze_sql
import uvicorn

app = FastAPI(title="SQLGuard", version="1.0.0")


class ReviewRequest(BaseModel):
    sql: str

# ── Inline HTML ──────────────────────────────────────────────────────────────

HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SQLGuard — AI SQL 审核工具</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
       background: #0f1117; color: #e2e8f0; min-height: 100vh; }
.container { max-width: 860px; margin: 0 auto; padding: 40px 20px; }

/* Header */
.header { text-align: center; margin-bottom: 40px; }
.logo { font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.tagline { color: #64748b; margin-top: 8px; font-size: 0.95rem; }

/* Editor */
.editor-wrap { background: #1e2330; border: 1px solid #2d3748; border-radius: 12px; overflow: hidden; margin-bottom: 20px; }
.toolbar { background: #161b27; padding: 10px 16px; border-bottom: 1px solid #2d3748;
           display: flex; align-items: center; gap: 8px; }
.toolbar span { color: #64748b; font-size: 0.8rem; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot-red { background: #ff5f57; }
.dot-yellow { background: #febc2e; }
.dot-green { background: #28c840; }
textarea { width: 100%; min-height: 200px; background: transparent; border: none;
           color: #e2e8f0; font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
           font-size: 0.9rem; padding: 16px; resize: vertical; outline: none; line-height: 1.6; }
textarea::placeholder { color: #475569; }

/* Buttons */
.btn-row { display: flex; gap: 12px; margin-bottom: 28px; }
.btn { flex: 1; padding: 12px 20px; border-radius: 8px; border: none; cursor: pointer;
       font-size: 0.95rem; font-weight: 600; transition: all 0.2s; }
.btn-primary { background: linear-gradient(135deg, #60a5fa, #a78bfa); color: #fff; }
.btn-primary:hover { opacity: 0.88; transform: translateY(-1px); }
.btn-secondary { background: #1e2330; color: #94a3b8; border: 1px solid #2d3748; }
.btn-secondary:hover { border-color: #60a5fa; color: #e2e8f0; }

/* Report */
.report { display: none; background: #1e2330; border: 1px solid #2d3748; border-radius: 12px; overflow: hidden; }
.report.show { display: block; }
.report-header { background: #161b27; padding: 14px 20px; border-bottom: 1px solid #2d3748;
                 display: flex; align-items: center; justify-content: space-between; }
.report-title { font-weight: 700; font-size: 1rem; }
.score-badge { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
.score-high { background: #7f1d1d; color: #fca5a5; }
.score-medium { background: #78350f; color: #fdba74; }
.score-low { background: #14532d; color: #86efac; }
.score-good { background: #0f3d2e; color: #6ee7b7; }

/* Issue list */
.issue-list { padding: 0; }
.issue-item { padding: 14px 20px; border-bottom: 1px solid #1e2330; display: flex; gap: 12px; align-items: flex-start; }
.issue-item:last-child { border-bottom: none; }
.severity { min-width: 90px; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-align: center; }
.sev-high { background: #7f1d1d; color: #fca5a5; }
.sev-medium { background: #78350f; color: #fdba74; }
.sev-low { background: #14532d; color: #86efac; }
.sev-good { background: #0f3d2e; color: #6ee7b7; }
.issue-body { flex: 1; }
.issue-id { font-size: 0.75rem; color: #475569; margin-bottom: 4px; font-family: monospace; }
.issue-msg { font-size: 0.9rem; line-height: 1.5; }
.empty-state { padding: 40px 20px; text-align: center; color: #475569; }

/* Recommendation bar */
.rec-bar { padding: 14px 20px; background: #161b27; border-top: 1px solid #2d3748;
           font-size: 0.9rem; font-weight: 600; }

/* Stats row */
.stats { display: flex; gap: 16px; margin-bottom: 20px; }
.stat-card { flex: 1; background: #1e2330; border: 1px solid #2d3748; border-radius: 10px;
             padding: 16px; text-align: center; }
.stat-num { font-size: 2rem; font-weight: 800; }
.stat-label { font-size: 0.8rem; color: #64748b; margin-top: 4px; }
.stat-high .stat-num { color: #fca5a5; }
.stat-medium .stat-num { color: #fdba74; }
.stat-low .stat-num { color: #86efac; }

/* Footer */
.footer { text-align: center; margin-top: 40px; color: #475569; font-size: 0.8rem; }
.footer a { color: #60a5fa; text-decoration: none; }
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <div class="logo">SQLGuard</div>
    <div class="tagline">粘贴 SQL，即时获取风险分析报告 · 永久免费</div>
  </div>

  <div class="editor-wrap">
    <div class="toolbar">
      <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
      <span style="margin-left:8px">SQL Editor</span>
    </div>
    <textarea id="sql-input" placeholder="粘贴你的 SQL 语句，例如：

SELECT * FROM orders WHERE created_at > '2025-01-01';

UPDATE employees SET salary = salary * 1.1;

DELETE FROM sessions WHERE last_login < '2024-01-01';""></textarea>
  </div>

  <div class="btn-row">
    <button class="btn btn-primary" onclick="runReview()">🔍 审核 SQL</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑 清空</button>
  </div>

  <div id="report" class="report"></div>

  <div class="footer">
    SQLGuard v1.0 · 基于规则引擎的 SQL 风险检测 · 无需数据库连接
  </div>
</div>

<script>
async function runReview() {
  const sql = document.getElementById('sql-input').value.trim();
  if (!sql) { alert('请先输入 SQL 语句'); return; }

  const btn = document.querySelector('.btn-primary');
  btn.textContent = '⏳ 分析中...';
  btn.disabled = true;

  try {
    const resp = await fetch('/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sql })
    });
    const data = await resp.json();
    renderReport(data);
  } catch (e) {
    alert('请求失败: ' + e.message);
  } finally {
    btn.textContent = '🔍 审核 SQL';
    btn.disabled = false;
  }
}

function renderReport(data) {
  const el = document.getElementById('report');
  if (!data.total_issues && data.risk_score === 0) {
    el.classList.add('show');
    el.innerHTML = `
      <div class="report-header">
        <span class="report-title">📋 审核报告</span>
        <span class="score-badge score-good">✅ 通过</span>
      </div>
      <div class="empty-state">未检测到风险项，SQL 可以部署到生产环境。</div>
    `;
    return;
  }

  const sevClass = data.high.length ? 'score-high' : data.medium.length ? 'score-medium' : 'score-low';
  const sevLabel = data.high.length ? '🔴 高风险' : data.medium.length ? '🟡 中风险' : '🟢 低风险';

  let html = `
  <div class="report-header">
    <span class="report-title">📋 审核报告</span>
    <span class="score-badge ${sevClass}">${sevLabel} · ${data.total_issues} 个问题</span>
  </div>

  <div class="stats">
    <div class="stat-card stat-high"><div class="stat-num">${data.high.length}</div><div class="stat-label">高风险</div></div>
    <div class="stat-card stat-medium"><div class="stat-num">${data.medium.length}</div><div class="stat-label">中风险</div></div>
    <div class="stat-card stat-low"><div class="stat-num">${data.low.length}</div><div class="stat-label">低风险</div></div>
  </div>

  <div class="issue-list">`;

  const all = [...data.high, ...data.medium, ...data.low];
  for (const [rule_id, severity, msg] of all) {
    const sevClass = severity.includes('HIGH') ? 'sev-high' : severity.includes('MEDIUM') ? 'sev-medium' : 'sev-low';
    const sevLabel = severity.includes('HIGH') ? '🔴 HIGH' : severity.includes('MEDIUM') ? '🟡 MEDIUM' : '🟢 LOW';
    html += `<div class="issue-item">
      <span class="severity ${sevClass}">${sevLabel}</span>
      <div class="issue-body">
        <div class="issue-id">${rule_id}</div>
        <div class="issue-msg">${msg}</div>
      </div>
    </div>`;
  }

  html += `</div>
  <div class="rec-bar">${data.recommendation}</div>`;

  el.innerHTML = html;
  el.classList.add('show');
}

function clearAll() {
  document.getElementById('sql-input').value = '';
  document.getElementById('report').classList.remove('show');
}
</script>
</body>
</html>
"""


# ── API Endpoint ─────────────────────────────────────────────────────────────

@app.post("/review")
async def review(req: ReviewRequest) -> dict:
    """Analyze SQL and return structured report."""
    return analyze_sql(req.sql)


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the SPA."""
    return HTML


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting SQLGuard on http://localhost:18765")
    uvicorn.run(app, host="0.0.0.0", port=18765)
