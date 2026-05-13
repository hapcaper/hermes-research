# AI Contract Review - Quick Market Research
> Date: 2025-05-13
> Status: In Progress

## Known Players

### Global
- **LawGeex** (US/Israel) - contract review automation
- **Kira Systems** (Canada) - machine learning for contracts
- **Leverton** (acquired) - contract abstraction

### China
- **Functek** - construction contracts, enterprise pricing
- **幂律智能** - legal AI for enterprises, unclear pricing
- **otherm.cn** - 99-999/month, individual/small team focus
- **百度法务AI** - free + premium features
- **阿里云智能法务** - API-based, per-call pricing

### GitHub Open Source
- **wangxupeng/2019Legal-AI-Challenge** - Chinese legal AI competition solution
- **zubair-trabzada/ai-legal-claude** - Claude skill for contract review
- **kevin** (willchen96) - OSS AI Legal Platform, 2889 stars

## Key Questions to Answer

1. **Do construction company owners actually review contracts themselves?**
   - Or do they always use a lawyer?
   - If always lawyer, AI tool is dead on arrival

2. **What's their current process?**
   - Excel checklist? Lawyer? Gut feeling?
   - If lawyer, would they pay extra for AI pre-screening?

3. **What specific risk points cause the most problems?**
   - Payment terms?
   - Liability caps?
   - Late delivery penalties?
   - Scope creep clauses?

4. **Price sensitivity**
   - 99/month (cheap) vs 999/month (expensive) for their business
   - What would they compare it to?

## 李梓浩's Position
- **Strengths**: Java backend, can build data pipeline, can integrate APIs
- **Weaknesses**: No legal background, no existing network in construction
- **Opportunity**: Build tool WITHOUT legal background (template-based risk detection)

## Hypothesis
The tool should NOT try to "understand law" - it should be a checklist automation:
1. Upload contract → extract key clauses
2. Run through known risk patterns (payment delays, liability gaps, auto-renew)
3. Flag anything unusual
4. Suggest "review this with a lawyer"

This lowers the trust barrier because it's not replacing the lawyer, just pre-screening.

## Decision Tree
```
If construction owners review contracts themselves → VALIDATED (build MVP)
If they always use lawyers → CHECK if AI helps lawyer (B2B2C)
If they don't care about risk → INVALIDATED
```
