# The research pipeline

A single stock passes these stages, in order, before it can be held. A fund skips S1-S4 (it is a proxy, see
[principles.md](principles.md)). There is no composite score: each stage either passes or stops the name.

| Stage | Question | Passes when |
|---|---|---|
| S0 Access | Can the account actually buy it? | It trades on a venue the account can reach |
| S1 Segment map | What does the company actually sell, and to whom? | Revenue is mapped to segments and customers from filings, with the top-customer share ([signals.md](signals.md#customer-concentration)) |
| S2 Capital stack | What sits ahead of the shareholder? | Debt, leases, preferred and convertibles are listed with maturities |
| S3 Hazard spec | What would prove the case wrong? | At least one **kill criterion** is written ([kill-criteria.md](kill-criteria.md)), and the policy-reversal check is answered |
| S4 Valuation gate | Is the price supported by things that can be observed? | Valuation is checked against reported figures, not narratives |
| S5 Factor and node map | What does it move with? | Its exposures (rates, a single customer, a commodity, a theme) are recorded |
| S6 Sizing | How much? | Sized by loss budget (below) |

**The hard gate is S3: no kill criterion, no position.** A kill criterion must be something the business does or
reports. What it may never contain is listed once, in
[kill-criteria.md](kill-criteria.md#what-a-kill-criterion-never-contains). If the thesis depends on a government
decision, S3 also asks what happens if that policy reverses ([kill-criteria.md](kill-criteria.md#the-policy-reversal-check)).

## Sizing by loss budget

One precedence rule sets every size. All budgets, sizes and limits are in **% of the portfolio**.

```
budget size = min(remaining bucket budget, min over linked nodes of remaining node budget) / stressed loss per dollar
size        = min(budget size, tier ceiling, sleeve limit)
```

1. **Loss budget first.** A loss budget is set in advance for each factor bucket and each node (a shared customer,
   supplier or theme). "Remaining" means the budget less the stressed loss already used by names held against it. A
   name linked to several nodes takes the smallest remaining node budget. Two names that depend on the same large
   customer share that customer's node budget.
2. **Then the caps.** The budget size is capped by the name's conviction tier and by the size limits in
   [portfolio-process.md](portfolio-process.md#limits). A limit stated as a share of a sleeve is converted to % of the
   portfolio by multiplying it by the sleeve's weight.
3. **Record which constraint binds:** the bucket, the named node, the tier, or the sleeve limit.
4. **The floor applies at entry only.** If the result is below the sleeve's minimum size, the name is not bought; the
   size is never rounded up past its loss budget. After entry the drift bands govern, so a held weight can sit below
   the floor without a breach.

- **Stressed loss per dollar** is how much a position would lose in a bad but plausible case. In the speculative sleeve
  it is 1.0, because each name is sized to be lost in full.
- Conviction is used in **tiers**. A tier sets a ceiling on size, not a size; there is no continuous conviction score.
- A position is sized smaller when its parameters are uncertain, even if its kill criterion is crisp.

## Speculative sleeve

Early-stage names with negative free cash flow and heavy outside funding belong in a separate speculative sleeve. Each
is sized to be lost in full, and the funding sell rule (SR-1a and SR-1b) does not apply there, because that profile is
the thesis, not a defect.
