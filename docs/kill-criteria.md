# Kill criteria

A kill criterion is the written condition that ends a position (sell rule SR-3). The pipeline will not admit a name
without one ([pipeline.md](pipeline.md), stage S3). In the speculative sleeve the funding-dependence rule (SR-1) does not
apply, so the kill criteria carry most of the weight there. The forensic rule (SR-2) and the tax rule (SR-4) still apply
in every sleeve.

## The shape of a kill criterion

Every kill criterion has three parts:

1. **An observable**: something the business does or reports.
2. **A threshold**: a number or an event that can be checked without judgment.
3. **Where it surfaces first**: the filing, report or call where it would appear.

It never contains price, drawdown, a valuation multiple, a credit-spread level or an analyst's rating change. A kill
criterion is written **before** the buy and changed only through the same review that admitted the name.

## Shared criteria for capital-intensive builders

These apply to any name that borrows or raises money to build capacity. Any one fires.

| Code | Observable | Threshold | Surfaces first |
|---|---|---|---|
| K1 | Distress language | A going-concern paragraph, a covenant breach, or a lender waiver or forbearance | Quarterly report notes; a current report for a triggering event |
| K2 | Liquidity runway | Cash plus committed, undrawn financing covers less than 12 months of the company's own stated capital spending and debt service | Quarterly report, liquidity section |
| K3 | Anchor customer lost | A disclosed termination, default, or a cut of more than 25% in contract value by a customer that was more than 25% of backlog **at the last filing before the event** | Current report; quarterly backlog or remaining performance obligations |

## Patterns for name-specific criteria

Each name gets one or two criteria of its own. The patterns below are **templates, not finished criteria**. A pattern
passes stage S3 only once it names the metric, the baseline and its date, and the exact event or number that fires it.
For example, "cuts spend materially" becomes "cuts its contracted annual spend by more than 25% from the level in the
last annual report".

| Pattern | Write it as | Example (made-up) |
|---|---|---|
| Customer concentration | The largest customer cuts spend by more than a stated percentage from a dated baseline, or leaves | "The customer that was 60% of revenue in the last annual report cuts contracted spend by more than 25%, per a filing" |
| Own-guidance miss | The company misses a target it set itself, by a stated margin, measured on a stated date | "Capacity in service at year end, as reported in the annual report, is more than 25% below the target the company gave at the start of the year" |
| Schedule slip | A project slips past the company's own schedule by a stated time | "Energization slips more than two quarters past the stated date" |
| Distressed financing | New money only on distressed terms | "A new raise priced as secured debt at 12% or more, or equity with warrants" |
| Share loss | Revenue falls while the market it serves grows | "Two quarters of revenue decline while industry spending rises" |
| Accounting or regulatory | A restatement, an auditor change, or a named regulatory event | "Another restatement, or a disclosed enforcement action or settlement in the inquiry named in the last annual report" |
| Policy reversal | The government decision the thesis depends on is reversed | "The price floor or subsidy the thesis depends on is withdrawn or cut" (see below) |

## The policy-reversal check

At stage S3, ask of every thesis: **does it depend on a government decision?** Examples are a price floor, a subsidy, a
tariff, a mandate, a license or a government contract. If it does, ask what happens if that policy reverses. If the
answer is that the thesis does not survive, the reversal is written down as a kill criterion before the buy. A thesis
that rests only on a policy is a bet on the policy, and is sized as one.

## Learning from other people's sells

When a published research service or a fund explains why it exited a name, sort the reason into one of two kinds:

- **A thesis reason**: missed own guidance, a lost customer, a moat that eroded, a policy dependence, a timeline that
  moved out. These are candidates for new kill-criterion patterns.
- **A price reason**: valuation, guidance that was only a little lower, opportunity cost. These are not kill criteria
  under these rules ([sell-rules.md](sell-rules.md#what-never-triggers-a-sell)).

Credit the idea; never copy a paid source's text ([COMPLIANCE.md](../COMPLIANCE.md), guardrail 6).

## When they are checked

- At every quarterly and annual filing.
- On every current report (an unscheduled filing of a material event).
- On the earnings calls of the name's largest customers, when concentration is part of the case.

A fired criterion goes to the review that day, with the written record that [sell-rules.md](sell-rules.md#before-any-sell-in-writing)
requires.

**Blind spots:** a criterion only sees what is disclosed. A customer can wind down a contract without saying so for a
quarter. Disclosure timing is the lag.
