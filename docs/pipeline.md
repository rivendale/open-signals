# The research pipeline

A single stock passes these stages, in order, before it can be held. A fund skips to sizing (it is a proxy, see
[principles.md](principles.md)). There is no composite score: each stage either passes or stops the name.

| Stage | Question | Passes when |
|---|---|---|
| S0 Access | Can the account actually buy it? | It trades on a venue the account can reach |
| S1 Segment map | What does the company actually sell, and to whom? | Revenue is mapped to segments and customers from filings |
| S2 Capital stack | What sits ahead of the shareholder? | Debt, leases, preferred and convertibles are listed with maturities |
| S3 Hazard spec | What would prove the case wrong? | At least one **kill criterion** is written: an observable, a threshold, and where it would surface first |
| S4 Valuation gate | Is the price supported by things that can be observed? | Valuation is checked against reported figures, not narratives |
| S5 Factor and node map | What does it move with? | Its exposures (rates, a single customer, a commodity, a theme) are recorded |
| S6 Sizing | How much? | Sized by loss budget (below) |

**The hard gate is S3: no kill criterion, no position.** A kill criterion may not contain price, a valuation multiple or a
drawdown; it must be something the business does or reports.

## Sizing by loss budget

```
size = min(bucket budget, node budget) / stressed loss per dollar
```

- A **loss budget** is set in advance for each factor bucket and each node (a shared customer, supplier or theme).
- **Stressed loss per dollar** is how much a position would lose in a bad but plausible case.
- Conviction is used in **tiers, equal weight within a tier**; there is no continuous conviction score.
- A position is sized smaller when its parameters are uncertain, even if its kill criterion is crisp.

## Speculative sleeve

Early-stage names with negative free cash flow and heavy outside funding belong in a separate speculative sleeve. Each
is sized to be lost in full, and the funding-dependence sell rule does not apply there, because that profile is the
thesis, not a defect.
