# Spike 004: SQL Review Tool - Market Research

## Spike Question

**Given a developer tool market in China, when validating SQL review tools as a side business, then: (1) do real paid products exist? (2) what pricing works? (3) can a solo developer compete?**

## Status: COMPLETED

---

## Brief

SQL review tools detect performance anti-patterns in SQL before they hit production. Spike 003 validated the technical approach (regex-based, no DB needed). This spike validates the market: are there real paid products? What do they charge? Can 李梓浩 compete?

---

## Research Findings

### 1. Competitive Landscape

#### Open Source SQL Review Tools (China)

| Product | Stars | License | Last Push | Type | Commercial? |
|---------|-------|---------|-----------|------|-------------|
| **Yearning** (cookieY/Yearning) | **8,943** | AGPL-3.0 | 2025-10-13 | Web platform (DBA-focused) | ❌ Free, self-hosted |
| sqlfluff (sqlfluff/sqlfluff) | **9,700** | MIT | 2026-05-13 | CLI linter (English) | ❌ Free |
| archery | ~2,000 | ? | ? | Web platform | ❌ Free |

**Yearning** is the dominant Chinese SQL review platform:
- Full web UI with approval workflows
- LDAP/钉钉/邮件 notifications
- DDL/DML execution + automatic rollback
- Fine-grained permission control
- Requires MySQL database to run
- Self-hosted, AGPL-3.0 license (requires source disclosure)
- Henry Yee (individual developer) maintains it

#### What Yearning IS NOT
- ❌ NOT a SaaS (no hosted version)
- ❌ NOT targeting individual developers
- ❌ NOT fast/lightweight (it's a full platform for DBA teams)

#### What Yearning IS
- ✅ Target: DBA teams at companies with 10+ DBAs
- ✅ Features: Approval workflows, SQL execution, LDAP integration
- ✅ Cost: Free (self-host your own)

---

### 2. The Gap: Developer-Focused SQL Review

| Dimension | Yearning | sqlfluff | Spike 003 MVP |
|-----------|----------|----------|---------------|
| Target user | DBA teams | Developers (English) | Individual devs (China) |
| Interface | Web platform | CLI | CLI |
| Price | Free (self-host) | Free | Planned: 199/月 |
| Language | Chinese | English | Chinese |
| IDE integration | ❌ | ❌ | Planned |
| Git hook/CI | ⚠️ Manual | ✅ | Planned |
| Speed | Slow (full platform) | Fast | Fast (static analysis) |
| Setup complexity | High (needs MySQL) | Low | Very low (single script) |

**The gap**: No Chinese developer-focused SQL lint/review tool that is:
1. Fast (CLI, no DB connection needed)
2. Chinese language
3. IDE/Git hook integration
4. Paid SaaS with hosted option

---

### 3. Pricing Benchmarks (from adjacent products)

| Product | Type | Pricing | Relevance |
|---------|------|---------|-----------|
| ShowDoc | API docs SaaS | 199-999/人/月 | ✅ Chinese dev tool |
| dbdiagram.io | DB docs SaaS | $8-75/月 | ✅ Developer tool |
| Apifox | API management | 199-999/人/月 | ✅ Developer tool |
| 阿里云SQL审查 | SQL API | 按次计费 | ⚠️ Enterprise API |

**Comparable pricing for a developer SQL tool**:
- CLI tool: Free (GitHub stars builder)
- Web dashboard: 99-199/月 (solo dev)
- Team features: 199-399/月 per team
- AI optimization: +99/月 premium

---

### 4. Key Market Insights

#### ✅ What validates the market:
1. Yearning has 8,943 GitHub stars — proves Chinese developers care about SQL review
2. sqlfluff has 9,700 stars globally — proves SQL linting is a real developer need
3. ShowDoc (12821 stars) proves Chinese devs pay for documentation tools at 199+/月
4. DBA teams at companies use Yearning, but individual developers have no good option

#### ❌ What makes this hard:
1. **Yearning is free and good enough** for teams that know about it
2. **sqlfluff is English but free** — for developers who know English, it's already solved
3. **No commercial SQL review SaaS exists** — the market may not materialize at 199/月
4. **GitHub stars ≠ paying customers** — many developers use free tools forever

---

## Verdict: PARTIAL — Validated with constraints

### What worked
- Market proof: Yearning's 8,943 stars validates that Chinese developers care about SQL review
- Technical: Spike 003 proved regex-based SQL analysis works without DB dependency
- Gap exists: Yearning is for DBA teams; no tool targets individual developers with fast CLI + Chinese UX
- Pricing precedent: ShowDoc/Apifox at 199/月 proves Chinese devs pay for developer tools

### What didn't work / Critical risks
- **No commercial SQL review SaaS exists** — this is a signal, not just an observation
- **Yearning is free and full-featured** — developers who find it don't need another tool
- **sqlfluff fills the English developer niche** — for English-fluent devs, already solved
- **GitHub stars ≠ paying customers** — Yearning has 9k stars but is maintained by one person with no SaaS revenue
- **Execution is the moat** — the idea is obvious; getting users to pay is the hard part

### Surprises
- **Yearning's maintainer (Henry Yee) has zero commercial version** — after 8,943 stars, still just open source
- **No one has tried SQL review SaaS in China** — every competitor is either open source or enterprise-only
- **The gap is real but the barrier is distribution**, not product

### Recommendation for the real build

**MVP if proceeding (1-week):**
1. Python CLI tool (same as Spike 003 rules)
2. Publish to GitHub + PyPI
3. Add GitHub Actions CI integration
4. Land 100 GitHub stars before even thinking about monetization

**Pivot from "SQL review SaaS" to "SQL lint tool for Chinese devs":**
- Don't try to be a SaaS from day 1
- Start as a CLI tool, build stars, then add paid features
- Monetization: freemium CLI (GitHub stars) + paid web dashboard + team features
- Target: Chinese developers who want fast SQL linting in their IDE without English barriers

**Pricing validation path:**
1. Land 100 GitHub stars (free)
2. Add optional web dashboard at 99/月
3. Add team features at 199/月 per team
4. Add AI optimization at +99/月

**Alternative**: If GitHub stars plateau at <50 after 2 weeks, this direction is too crowded. Pivot to API Change Log Tracker (Spike 005) instead.

---

## Head-to-Head: SQL Review vs API Change Log Tracker

| Dimension | SQL Review (this spike) | API Change Log Tracker |
|-----------|------------------------|------------------------|
| Technical complexity | Low (Spike 003 done) | Medium |
| Market validation | Yearning proves interest, no paid SaaS | New concept, no direct competitor |
| Differentiation | Chinese language + fast CLI | Specific niche (API changes) |
| Competition | sqlfluff (English, free) | Lower |
| Monetization path | Stars → paid features | Direct to paid |
| Recommendation | 🟡 Proceed with caution | 🟢 Preferred |

---

## Next Steps

1. [ ] **Build CLI and publish to GitHub** (same day as Spike 003 rules)
2. [ ] **Post to V2EX/掘金** to test initial traction
3. [ ] **Land 50+ stars in 2 weeks** — if yes, proceed with paid features; if no, pivot to API Change Log Tracker
4. [ ] If pivoting: Spike 005 (API Change Log Tracker) is ready to run
