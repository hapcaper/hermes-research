#!/usr/bin/env python3
"""
Spike 008b: Data Cleaning Web Tool
FastAPI-based CSV upload → issue detection → cleaned CSV download
"""

import io
import sys
import csv
import re
from datetime import datetime
from typing import List, Dict, Tuple

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# ─── Data Cleaner (from data_cleaner.py) ────────────────────────────────────

class DataCleaner:
    def __init__(self, rows: List[Dict], headers: List[str]):
        self.rows = rows
        self.headers = headers
        self.issues = []
        self.original_count = len(rows)
    
    def detect_all_issues(self) -> List[Dict]:
        self.issues = []
        
        # 1. Empty cells
        for col in self.headers:
            total_missing = sum(1 for row in self.rows 
                               if not str(row.get(col, '')).strip())
            if total_missing > 0:
                pct = total_missing / len(self.rows) * 100
                self.issues.append({
                    'type': 'empty_cells',
                    'column': col,
                    'count': total_missing,
                    'percentage': round(pct, 1),
                    'severity': 'HIGH' if pct > 20 else 'MEDIUM' if pct > 5 else 'LOW',
                    'suggestion': f'Fill {total_missing} missing values or remove rows'
                })
        
        # 2. Phone format inconsistency
        for col in self.headers:
            samples = [str(row.get(col, '')).strip() for row in self.rows[:10] if row.get(col)]
            formats_found = set()
            for val in samples:
                for pattern, _ in [
                    (r'^\d{11}$', '13812345678'),
                    (r'^\d{3}-\d{4}-\d{4}$', '138-1234-5678'),
                    (r'^\d{3}\s\d{4}\s\d{4}$', '138 1234 5678'),
                    (r'^\+86\s?\d{11}$', '+86 13812345678'),
                ]:
                    if re.match(pattern, val):
                        formats_found.add(pattern)
            if len(formats_found) > 1:
                self.issues.append({
                    'type': 'inconsistent_format',
                    'column': col,
                    'count': 'multiple formats',
                    'severity': 'MEDIUM',
                    'suggestion': 'Standardize phone format to 11 digits'
                })
        
        # 3. Date format inconsistency
        date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%Y%m%d']
        for col in self.headers:
            samples = [str(row.get(col, '')).strip() for row in self.rows[:10] if row.get(col)]
            formats_found = set()
            for val in samples:
                for fmt in date_formats:
                    try:
                        datetime.strptime(val, fmt)
                        formats_found.add(fmt)
                        break
                    except:
                        pass
            if len(formats_found) > 1:
                self.issues.append({
                    'type': 'inconsistent_date',
                    'column': col,
                    'count': 'multiple formats',
                    'severity': 'HIGH',
                    'suggestion': 'Standardize date format to YYYY-MM-DD'
                })
        
        # 4. Duplicates
        seen = []
        dup_indices = []
        for i, row in enumerate(self.rows):
            row_key = tuple(sorted(row.items()))
            if row_key in seen:
                dup_indices.append(i)
            else:
                seen.append(row_key)
        if dup_indices:
            self.issues.append({
                'type': 'duplicates',
                'column': 'ALL',
                'count': len(dup_indices),
                'percentage': round(len(dup_indices) / len(self.rows) * 100, 1),
                'severity': 'HIGH',
                'suggestion': f'Remove {len(dup_indices)} duplicate rows'
            })
        
        # 5. Whitespace
        for col in self.headers:
            whitespace_count = sum(1 for row in self.rows 
                                 if isinstance(row.get(col), str) 
                                 and (row[col].startswith(' ') or row[col].endswith(' ')))
            if whitespace_count > 0:
                self.issues.append({
                    'type': 'whitespace',
                    'column': col,
                    'count': whitespace_count,
                    'severity': 'LOW',
                    'suggestion': 'Strip leading/trailing whitespace'
                })
        
        return self.issues
    
    def clean(self) -> List[Dict]:
        rows = [row.copy() for row in self.rows]
        issue_types_fixed = {i['type'] for i in self.issues}
        
        if 'duplicates' in issue_types_fixed:
            seen = []
            unique_rows = []
            for row in rows:
                row_key = tuple(sorted(row.items()))
                if row_key not in seen:
                    seen.append(row_key)
                    unique_rows.append(row)
            rows = unique_rows
        
        for issue in self.issues:
            col = issue['column']
            
            if issue['type'] == 'empty_cells':
                for row in rows:
                    if not str(row.get(col, '')).strip():
                        row[col] = 'Unknown'
            
            elif issue['type'] == 'whitespace':
                for row in rows:
                    if isinstance(row.get(col), str):
                        row[col] = row[col].strip()
            
            elif issue['type'] == 'inconsistent_format':
                def standardize_phone(val):
                    val = re.sub(r'[\s\-\(\)]', '', str(val))
                    if val.startswith('+86'):
                        val = val[3:]
                    return val
                for row in rows:
                    if col in row and row[col]:
                        row[col] = standardize_phone(row[col])
            
            elif issue['type'] == 'inconsistent_date':
                def standardize_date(val):
                    val = str(val).strip()
                    for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%Y%m%d']:
                        try:
                            return datetime.strptime(val, fmt).strftime('%Y-%m-%d')
                        except:
                            pass
                    return val
                for row in rows:
                    if col in row and row[col]:
                        row[col] = standardize_date(row[col])
        
        return rows
    
    def generate_report(self) -> Dict:
        total_cells = len(self.rows) * len(self.headers)
        issue_count = sum(i['count'] if isinstance(i['count'], (int, float)) else 0 for i in self.issues)
        return {
            'original_rows': self.original_count,
            'cleaned_rows': len(self.rows),
            'total_columns': len(self.headers),
            'issue_count': len(self.issues),
            'cells_affected': issue_count,
            'quality_score': max(0, 100 - round(issue_count / max(total_cells, 1) * 100, 1)),
            'issues': self.issues
        }


def parse_csv(content: bytes) -> Tuple[List[Dict], List[str]]:
    text = content.decode('utf-8', errors='replace')
    reader = csv.DictReader(io.StringIO(text))
    headers = reader.fieldnames or []
    rows = list(reader)
    return rows, headers


def rows_to_csv(rows: List[Dict], headers: List[str]) -> bytes:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode('utf-8')


# ─── FastAPI App ────────────────────────────────────────────────────────────

app = FastAPI(title="Data Cleaner Pro")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Data Cleaner Pro — CSV数据清洗工具</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e6edf3; min-height: 100vh; }
.container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
header { text-align: center; margin-bottom: 40px; }
h1 { font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #58a6ff, #a371f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { color: #8b949e; margin-top: 8px; font-size: 0.95rem; }
.upload-zone { border: 2px dashed #30363d; border-radius: 12px; padding: 60px 20px; text-align: center; cursor: pointer; transition: all 0.2s; margin-bottom: 24px; }
.upload-zone:hover, .upload-zone.dragover { border-color: #58a6ff; background: rgba(88,166,255,0.05); }
.upload-zone input { display: none; }
.upload-icon { font-size: 3rem; margin-bottom: 16px; }
.upload-text { font-size: 1.1rem; color: #8b949e; }
.upload-text span { color: #58a6ff; }
.upload-hint { font-size: 0.8rem; color: #484f58; margin-top: 8px; }
.btn { display: inline-flex; align-items: center; gap: 8px; background: #238636; color: #fff; border: none; border-radius: 8px; padding: 12px 24px; font-size: 1rem; cursor: pointer; transition: background 0.2s; }
.btn:hover { background: #2ea043; }
.btn:disabled { background: #484f58; cursor: not-allowed; }
.btn-outline { background: transparent; border: 1px solid #30363d; color: #8b949e; }
.hidden { display: none; }
.results { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 24px; margin-top: 24px; }
.section-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 16px; color: #e6edf3; }
.issue-card { background: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin-bottom: 12px; display: flex; align-items: flex-start; gap: 12px; }
.severity-badge { font-size: 0.7rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; flex-shrink: 0; }
.severity-HIGH { background: rgba(248,81,73,0.15); color: #f85149; }
.severity-MEDIUM { background: rgba(210,153,34,0.15); color: #d29922; }
.severity-LOW { background: rgba(88,166,255,0.15); color: #58a6ff; }
.issue-info { flex: 1; }
.issue-type { font-weight: 600; font-size: 0.95rem; }
.issue-detail { color: #8b949e; font-size: 0.85rem; margin-top: 4px; }
.issue-suggestion { color: #a371f7; font-size: 0.85rem; margin-top: 6px; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }
.stat { background: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 16px; text-align: center; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: #58a6ff; }
.stat-label { font-size: 0.75rem; color: #8b949e; margin-top: 4px; }
.quality-bar { height: 8px; background: #30363d; border-radius: 4px; overflow: hidden; margin-top: 8px; }
.quality-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
.quality-good { background: #238636; }
.quality-medium { background: #d29922; }
.quality-bad { background: #f85149; }
.preview-table { width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 0.8rem; }
.preview-table th { background: #1c2128; padding: 8px 12px; text-align: left; border-bottom: 1px solid #30363d; color: #8b949e; font-weight: 600; }
.preview-table td { padding: 8px 12px; border-bottom: 1px solid #21262d; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.preview-table tr:hover td { background: rgba(88,166,255,0.05); }
.filename { color: #58a6ff; font-weight: 600; }
.footer { text-align: center; margin-top: 40px; color: #484f58; font-size: 0.8rem; }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>🧹 Data Cleaner Pro</h1>
    <p class="subtitle">上传 CSV 文件，自动检测并修复数据质量问题</p>
  </header>

  <div id="uploadZone" class="upload-zone">
    <input type="file" id="fileInput" accept=".csv">
    <div class="upload-icon">📂</div>
    <p class="upload-text">拖放 CSV 文件，或 <span>点击选择</span></p>
    <p class="upload-hint">支持 UTF-8/GBK 编码，最大 10MB</p>
  </div>

  <button id="cleanBtn" class="btn hidden" onclick="cleanFile()">
    <span>✨</span> 一键清洗
  </button>

  <div id="results" class="results hidden">
    <h2 class="section-title">📊 数据质量报告</h2>
    <div class="stats" id="stats"></div>
    
    <div id="qualitySection" class="hidden">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.9rem; color:#8b949e;">数据质量评分</span>
        <span id="qualityScore" style="font-weight:700;"></span>
      </div>
      <div class="quality-bar"><div id="qualityFill" class="quality-fill" style="width:0%"></div></div>
    </div>

    <h3 class="section-title" style="margin-top:24px;">🐛 发现的问题</h3>
    <div id="issuesList"></div>

    <h3 class="section-title" style="margin-top:24px;">📋 清洗后数据预览（前10行）</h3>
    <div style="overflow-x:auto;" id="previewTable"></div>

    <div style="margin-top:24px; display:flex; gap:12px; flex-wrap:wrap;">
      <button class="btn" onclick="downloadCleaned()">
        <span>⬇️</span> 下载清洗后的 CSV
      </button>
      <button class="btn btn-outline" onclick="resetAll()">
        <span>🔄</span> 重新上传
      </button>
    </div>
  </div>
</div>

<div class="footer">
  Data Cleaner Pro · 纯 Python 实现，无需上传到服务器
</div>

<script>
let currentFile = null;
let cleanedData = null;
let originalFilename = '';

const zone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const cleanBtn = document.getElementById('cleanBtn');
const results = document.getElementById('results');

zone.addEventListener('click', () => fileInput.click());
zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
zone.addEventListener('drop', e => {
  e.preventDefault();
  zone.classList.remove('dragover');
  const f = e.dataTransfer.files[0];
  if (f) handleFile(f);
});
fileInput.addEventListener('change', e => { if (e.target.files[0]) handleFile(e.target.files[0]); });

function handleFile(f) {
  if (!f.name.endsWith('.csv')) { alert('请选择 CSV 文件'); return; }
  if (f.size > 10 * 1024 * 1024) { alert('文件大小不能超过 10MB'); return; }
  currentFile = f;
  originalFilename = f.name.replace('.csv', '_cleaned.csv');
  zone.classList.add('hidden');
  cleanBtn.classList.remove('hidden');
  results.classList.add('hidden');
}

async function cleanFile() {
  if (!currentFile) return;
  cleanBtn.disabled = true;
  cleanBtn.innerHTML = '<span>⏳</span> 处理中...';
  
  const formData = new FormData();
  formData.append('file', currentFile);
  
  try {
    const resp = await fetch('/clean', { method: 'POST', body: formData });
    const data = await resp.json();
    
    if (data.error) { alert('错误: ' + data.error); return; }
    
    cleanedData = data;
    showResults(data);
  } catch (err) {
    alert('请求失败: ' + err.message);
  } finally {
    cleanBtn.disabled = false;
    cleanBtn.innerHTML = '<span>✨</span> 一键清洗';
  }
}

function showResults(data) {
  results.classList.remove('hidden');
  cleanBtn.classList.add('hidden');
  
  // Stats
  const stats = document.getElementById('stats');
  stats.innerHTML = `
    <div class="stat"><div class="stat-value">${data.original_rows}</div><div class="stat-label">原始行数</div></div>
    <div class="stat"><div class="stat-value">${data.cleaned_rows}</div><div class="stat-label">清洗后行数</div></div>
    <div class="stat"><div class="stat-value">${data.issue_count}</div><div class="stat-label">发现问题</div></div>
    <div class="stat"><div class="stat-value">${data.total_columns}</div><div class="stat-label">列数</div></div>
  `;
  
  // Quality score
  const qs = data.quality_score;
  const qFill = document.getElementById('qualityFill');
  const qClass = qs >= 80 ? 'quality-good' : qs >= 50 ? 'quality-medium' : 'quality-bad';
  qFill.className = 'quality-fill ' + qClass;
  qFill.style.width = qs + '%';
  document.getElementById('qualityScore').textContent = qs + '/100';
  document.getElementById('qualityScore').style.color = qs >= 80 ? '#238636' : qs >= 50 ? '#d29922' : '#f85149';
  
  // Issues
  const issuesList = document.getElementById('issuesList');
  if (data.issues && data.issues.length > 0) {
    issuesList.innerHTML = data.issues.map(issue => `
      <div class="issue-card">
        <span class="severity-badge severity-${issue.severity}">${issue.severity}</span>
        <div class="issue-info">
          <div class="issue-type">${issue.type === 'empty_cells' ? '🟨 空单元格' : 
            issue.type === 'inconsistent_format' ? '📱 格式不一致' :
            issue.type === 'inconsistent_date' ? '📅 日期格式混乱' :
            issue.type === 'duplicates' ? '📋 重复行' :
            issue.type === 'whitespace' ? '✂️ 首尾空格' : issue.type}</div>
          <div class="issue-detail">列: <strong>${issue.column}</strong>${issue.count !== 'multiple formats' ? ' · 数量: ' + issue.count : ''} · ${issue.percentage ? issue.percentage + '%' : ''}</div>
          <div class="issue-suggestion">💡 ${issue.suggestion}</div>
        </div>
      </div>
    `).join('');
  } else {
    issuesList.innerHTML = '<p style="color:#8b949e;text-align:center;padding:20px;">🎉 没有发现数据质量问题！</p>';
  }
  
  // Preview table
  const previewTable = document.getElementById('previewTable');
  if (data.preview && data.preview.length > 0) {
    const headers = Object.keys(data.preview[0]);
    previewTable.innerHTML = `
      <table class="preview-table">
        <thead><tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr></thead>
        <tbody>
          ${data.preview.map(row => `<tr>${headers.map(h => `<td>${row[h] ?? ''}</td>`).join('')}</tr>`).join('')}
        </tbody>
      </table>
    `;
  }
}

function downloadCleaned() {
  if (!cleanedData || !cleanedData.csv_content) return;
  const blob = new Blob([cleanedData.csv_content], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = originalFilename;
  a.click();
  URL.revokeObjectURL(url);
}

function resetAll() {
  currentFile = null;
  cleanedData = null;
  zone.classList.remove('hidden');
  cleanBtn.classList.add('hidden');
  results.classList.add('hidden');
  fileInput.value = '';
}
</script>
</body>
</html>"""


@app.get("/")
async def root():
    return HTMLResponse(content=HTML_TEMPLATE)


@app.post("/clean")
async def clean_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
    try:
        rows, headers = parse_csv(content)
        if not rows:
            raise HTTPException(status_code=400, detail="Empty CSV file")
        
        cleaner = DataCleaner(rows, headers)
        cleaner.detect_all_issues()
        cleaned_rows = cleaner.clean()
        report = cleaner.generate_report()
        csv_content = rows_to_csv(cleaned_rows, headers)
        
        # Preview: first 10 rows
        preview = cleaned_rows[:10]
        
        return {
            "original_rows": report['original_rows'],
            "cleaned_rows": report['cleaned_rows'],
            "total_columns": report['total_columns'],
            "issue_count": report['issue_count'],
            "quality_score": report['quality_score'],
            "issues": report['issues'],
            "csv_content": csv_content.decode('utf-8'),
            "preview": preview
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("🚀 Data Cleaner Pro starting on http://localhost:18765")
    uvicorn.run(app, host="0.0.0.0", port=18765, log_level="warning")
