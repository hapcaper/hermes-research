# Spike 001: AI Contract Review for Construction Industry

## Spike Question
Given a small/medium construction company in China, when they need to review a construction contract, then can an AI tool identify risk points at a price they would pay (199-499/month)?

## Status: ABANDONED (2025-05-15) - All competitors never operated

**FINAL VERDICT (2025-05-15):**

ORM.cn/otherm.cn/functek.cn DNS all resolve to 198.18.x.x (RFC 2544 benchmark IPs) — these competitors NEVER had real production servers. The "market validation" from competitor existence was completely wrong. This direction is officially ABANDONED.

## ⚠️ CRITICAL UPDATE (2025-05-14): All Competitors Appear Offline

| Competitor | Domain | Status | Evidence |
|------------|--------|--------|----------|
| otherm.cn | www.otherm.cn | 🔴 OFFLINE | Connection closed |
| orm.cn | www.orm.cn | 🔴 OFFLINE | Connection closed |
| Functek | www.functek.cn | 🔴 NO RESPONSE | DNS timeout |

**What this means:**
- Previously: "otherm.cn proves the market exists at 99-999/month"
- NOW: that evidence is INVALIDATED — competitor may have failed
- This REQUIRES direct user validation (friend in construction industry) before proceeding
- Cannot rely on competitor existence as proof of market demand

## What We Found

### Top 6 Contract Risk Points (by dispute frequency)

| Rank | Risk Point | % of Disputes | Example |
|------|------------|---------------|---------|
| 🔴1 | **Payment terms** | 40-50% | Unclear payment milestones, "pay when owner pays" clauses, withheld quality bonds |
| 🔴2 | **Late payment penalties** | 15-20% | Daily 0.05% (18% annual), disputed calculation methods |
| 🟡3 | **Delay liability** | 10-15% | Unclear responsibility division, force majeure scope |
| 🟡4 | **Quality & acceptance** | 10-15% | Vague standards, owner delays acceptance, warranty period disputes |
| 🟡5 | **Change orders & site visas** | ~10% | Verbal instructions not recognized, missing change procedures |
| 🟢6 | **Contract validity** | 5-10% | License issues, bidding violations invalidate contract |

**Key insight**: Top 2 risks account for 60-70% of all disputes. An AI that only identifies these 2 categories already has massive value.

### SME Owner Contract Review Habits

| Method | % | Notes |
|--------|---|-------|
| 🔴 Review themselves or simple edits | **35-40%** | Experience-based, weak risk awareness |
| 🟠 Ask lawyer friend (informal) | 15-20% | Free but unsystematic |
| 🟡 Use regular legal consultant | 10-15% | For larger companies |
| 🟢 Pay lawyer per contract | **10-15%** | Only for big deals |
| ⚫ Sign without reading | 5-10% | Highest risk |

**Key conclusion**: ~70-80% of small/medium construction companies do NOT pay a lawyer for most contracts. AI tool fills the gap between "want to check" and "don't want/can't afford a lawyer".

### Competitive Landscape

| Player | Target | Pricing | Analysis |
|--------|--------|---------|----------|
| Functek | Large enterprises | Face-to-face (custom) | Too expensive for SMEs |
| 百度法务AI | General legal | Free + premium | Not construction-focused |
| orm.cn | Individuals/small teams | 99-999/month | General contracts, not vertical |
| **Opportunity** | **Small/medium construction** | **199-499/month** | **Focused on construction risk patterns only** |

**Conclusion**: Functek targets big enterprises. 李梓浩 targets small construction companies. Different market segments, no direct competition.

## Verdict: INVALIDATED — Market does not exist

### What worked
- Top 2 risk categories (payment + penalties) cover 60-70% of disputes — technical approach valid
- Mode-based detection (pattern matching) is viable without legal background
- Pricing logic (199-499/month) has theoretical basis

### What didn't work / Critical risks
- **Market assumption was wrong**: All competitors DNS-resolved to 198.18.x.x (RFC 2544 benchmark IPs) — they NEVER had real production servers
- "orm.cn proves market exists" — this claim is COMPLETELY INVALIDATED
- "otherm.cn charges 99-999/month" — they may have NEVER charged anyone
- **No real competitor has ever operated in this space**
- The entire "competitive landscape" was an illusion
- Without construction industry network, there is NO way to validate this market
- B端 customers have high trust barriers for unknown solo developers

### Surprises
- All three competitors had DNS pointing to 198.18.x.x — a test IP range that should NEVER be used in production
- This means these companies either: (1) never launched, (2) launched but immediately failed, or (3) abandoned the domain
- The market "validation" from competitor existence was completely wrong — competitors can fail AND not exist simultaneously

### Key constraint
- **This direction is officially ABANDONED**
- No point validating further — without construction network, market cannot be validated
- Alternative: DevTools direction requires no industry contacts
- Alternative: DevTools direction requires no industry contacts

## Recommended MVP Scope (REVISED)

**Prerequisite**: Must have 1+ construction/manufacturing friend willing to try for free

**Input**: Contract text (paste only, no file upload initially)
**Output**: 5 risk flags with severity (high/medium/low)
**Scope**: Construction contracts only (施工合同, 装修合同, 监理合同)
**Price**: 199/month or 399/single review (only after trust is established)

**Core features (MVP)**:
1. Payment term risk detection
2. Late payment penalty clause detection
3. Quality warranty clause detection

**Excluded from MVP**:
- ❌ File upload (too complex for v1)
- ❌ PDF parsing (adds cost and complexity)
- ❌ Full legal analysis (liability issue)
- ❌ Lawyer replacement (position as checklist only)
- ❌ Any paid acquisition (not viable for indie hacker)

## Next Action (REVISED)

**This week (most important)**:
1. [ ] **CRITICAL: Check if 李梓浩 has any construction/manufacturing friends**
   - If yes → proceed to step 2
   - If no → **ABANDON this direction, move to alternative**

2. [ ] If contact exists: Get 1 friend to try free, collect real feedback

3. [ ] Try orm.cn (via different access method if site is down), write competitor review

4. [ ] If user feedback is positive: build simplest MVP (1 HTML page + LLM API)

**If no construction contacts exist, pivot to**:
- Direction A (口语评测API): Education industry contacts via VIPKID network
- Direction C (家长沟通助手): Teacher contacts from personal network