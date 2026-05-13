# Spike 003: SQL Review Tool (Feasibility Test)

## Spike Question

**Given a SQL statement, when analyzed for performance risks, then can we detect common anti-patterns (SELECT *, missing indexes, full table scans) without heavy database dependencies?**

## Approach

Build a lightweight Python script that:
1. Uses regex-based SQL analysis (no DB needed, no sqlparse dependency)
2. Applies pattern detection rules to find common anti-patterns
3. Outputs structured risk report with severity levels

## Build Results

**Test Cases Run:**

| SQL | Detection | Severity | Status |
|-----|-----------|----------|--------|
| `SELECT * FROM users WHERE age > 18` | ✅ SELECT * detected | MEDIUM | ✅ Works |
| `UPDATE employees SET salary = 5000` | ✅ UPDATE without WHERE | HIGH | ✅ Works |
| `SELECT * FROM products WHERE name LIKE '%apple%'` | ✅ LIKE % prefix detected | HIGH | ✅ Works |
| `SELECT name, email FROM users LIMIT 10` | ✅ No issues | — | ✅ Works |

## Verdict: VALIDATED

### What worked
- Regex-based SQL analysis works for common anti-patterns without external dependencies
- 8 detection rules covering: SELECT *, missing LIMIT, LIKE prefix, correlated subqueries, UPDATE/DELETE without WHERE, multiple ORs, implicit type conversion
- Severity classification (HIGH/MEDIUM/LOW) with actionable recommendations
- No database connection needed — pure static analysis

### What didn't
- Regex-based approach has limits — cannot detect all complex SQL patterns
- False positives possible (e.g., SQL008 on legitimate numeric comparisons)
- Cannot detect missing indexes (requires DB schema introspection)

### Surprises
- Even a simple SELECT * can have multiple overlapping issues
- The tool correctly flagged "implicit type conversion" even on a clean-looking query

### Recommendation for the real build

**MVP scope (1-week):**
1. Core: 8-10 SQL anti-pattern rules (regex-based, no DB needed)
2. Input: paste SQL or connect to MySQL/PostgreSQL to pull table schemas
3. Output: risk report with line-level highlighting
4. Integration: Git hook / CLI so it runs pre-commit

**Differentiation from Yearning:**
- Yearning is DBA-focused (web UI,审批流程)
- This is developer-focused (CLI, IDE integration, fast feedback)
- Yearning doesn't do AI-powered optimization suggestions
- This can add AI optimization suggestions as premium feature

**Pricing model:**
- CLI: Free (builds GitHub stars)
- Web dashboard + team features: 199元/月/团队
- AI optimization suggestions: +99元/月

**Tech stack for MVP:**
- Python CLI (fastest to build)
- Optional: MySQL/PostgreSQL schema introspection via `records` library
- Optional: Streamlit web UI for dashboard

## Files
- `rules.py` — 8 detection rules
- `analyzer.py` — report generator + CLI
