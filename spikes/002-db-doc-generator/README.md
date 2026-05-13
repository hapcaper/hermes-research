# Spike 002: Database Documentation Generator

## Spike Question
Given a Chinese developer who needs to document their MySQL/PostgreSQL database, when they look for a tool, then will they pay for a hosted documentation service (vs. using free open-source tools)?

## Status: PARTIAL — Validated with caveats

**Core finding**: There IS a market (DBML ecosystem proves $8-60/month), but the "database schema → hosted docs" SaaS has a specific gap that may or may not be fillable by a solo developer.

---

## What We Found

### Competitive Landscape

| Tool | Type | Stars | Pricing | Analysis |
|------|------|-------|---------|----------|
| **SchemaSpy** | CLI → HTML | 2700+ | Free | Java CLI, outputs static HTML. Needs local Java + manual hosting |
| **SchemaCrawler** | CLI → HTML | 1300+ | Free | Java-based, richer output than SchemaSpy |
| **DBML** | DSL | 7000+ | Free | Language for defining DB schemas. Not a doc generator |
| **dbdocs.io** | Cloud SaaS | — | $8-20/mo | From DBML team. Define schema in DBML DSL → hosted docs |
| **dbdiagram.io** | Cloud SaaS | — | $8-75/mo | ER diagram tool from same team |

**Key insight**: The DBML team (holistics) owns this space. They have dbdocs.io ($8-20/mo) and dbdiagram.io ($8-75/mo). They are the dominant players.

### The Gap in the Market

**SchemaSpy problem**: It works, but:
1. Requires local Java installation
2. Outputs static HTML files you must host yourself
3. No cloud sync, no team sharing, no versioning
4. You run it locally every time you want fresh docs

**dbdocs.io problem**: It requires you to write DBML code by hand (or import SQL). It doesn't connect directly to your live database.

**The potential gap**: A tool that connects directly to MySQL/PostgreSQL → generates hosted documentation automatically, without requiring DBML syntax knowledge.

### Pricing Validation

| Product | Price | Target |
|---------|-------|--------|
| dbdocs Personal Pro | $8/mo ($20/mo monthly) | Individuals |
| dbdocs Team | $60/mo | Teams |
| dbdiagram Personal Pro | $8/mo | Individuals |
| dbdiagram Team | $75/mo | Teams |

**Proof**: People pay $8-75/month for database documentation tools. The market exists.

### Target User Pain

**Who would pay for this?**

1. **Small dev teams (2-10 people)** at Chinese internet companies
   - Need to share DB docs with team
   - Don't want to maintain SchemaSpy output manually
   - Will pay $99-299/month for convenience

2. **Freelance developers**
   - Need to hand over DB docs to clients
   - Don't want to teach clients to run SchemaSpy

3. **Startups**
   - Onboarding new devs quickly
   - DB docs as part of the workflow

### Risks and Challenges

1. **DBML team is already here**: They have brand recognition, large GitHub community (7000+ stars), and a paid product. Any new entrant competes with them.

2. **SchemaSpy is "good enough"**: Developers who know about it can use it for free. The paying segment is specifically people who want hosted/sharing features.

3. **Low technical barrier**: The core functionality (connect to DB, generate HTML) is not hard to build. The barrier is distribution, not technology.

4. **MySQL Workbench and Navicat**: Many developers already use these tools which have built-in documentation features.

### The Real Question

**Can a solo developer compete with DBML team?**

**Arguments YES**:
- DBML requires learning their DSL. Direct-connect (no DSL) is a different UX.
- Chinese market may prefer Chinese-language docs and support
- Niche: specifically "auto-connect and generate" without manual steps
- Could target smaller teams that dbdiagram's $75/mo team plan is too expensive for

**Arguments NO**:
- DBML team has 7000+ GitHub stars and brand trust
- Their free tier is already generous
- Any successful SaaS will face competition from them
- Building a hosted doc tool requires ongoing server costs and maintenance

---

## Verdict: PARTIAL — Market exists but crowded by well-funded incumbent

### What worked
- Pricing is validated: $8-60/month for DB docs is real (dbdocs/dbdigram)
- Pain is real: SchemaSpy is clunky, requires manual hosting
- Target user exists: small dev teams who want hosted docs

### What didn't work / Critical risks
- **Incumbent threat**: DBML team (holistics) already has dbdocs.io with $8-20/mo pricing
- **Low tech barrier**: The core functionality isn't hard to replicate
- **Distribution is the real challenge**: Getting users to pay requires marketing effort
- **"Good enough" competition**: SchemaSpy + static hosting is free and works

### Surprises
- The DBML ecosystem is much more mature than expected (7000+ stars, multiple paid products)
- There's actually a China-based team (Holistics) doing this well
- The pricing proves willingness to pay, but the market may already be served

### Recommendation for the real build

**If building this anyway**, the only viable differentiation:

1. **Language/UX**: Target Chinese developers specifically with Chinese UI and support
2. **One-click connect**: Direct MySQL/PostgreSQL connection (vs DBML's manual DSL approach)
3. **Pricing**: Go lower than $8/mo for solo devs, compete on price
4. **Integration**: Better GitHub/GitLab integration than dbdocs

**MVP scope if proceeding**:
- Input: MySQL connection string
- Output: Hosted HTML docs (like SchemaSpy output, but hosted)
- Free tier: 1 project, public sharing
- Paid tier: $9/month, unlimited projects, private sharing

**Or**: Abandon in favor of a less crowded developer tool niche.

---

## Next Action

**Decision point for 李梓浩**:

If you still want to build a developer tool, the DB documentation direction has a proven market but strong incumbent. You would need to commit to either:

1. **Compete on price/UX** with DBML team
2. **Find a different tool niche** with less competition

The original question ("日常开发痛点") still stands — without knowing your specific pain points, we can't be sure DB docs is the right tool to build.
