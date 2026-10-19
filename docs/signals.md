# Signal definitions

Every signal states its inputs, its formula, when it is checked, and its known blind spots. All examples use made-up
numbers. An implementation records the version of this file it follows and any threshold it set itself.

## Funding dependence

**Inputs (from the cash-flow statement, trailing four quarters):** operating cash flow, capital expenditure, stock
issued, net new debt (including convertibles).

Capital expenditure is taken as a **positive cash outflow**. Some data vendors report it as a negative number; flip the
sign before use, or the formula below adds capital spending instead of subtracting it.

```
free cash flow       = operating cash flow - capital expenditure
cash burn            = max(0, -free cash flow)
external funding     = stock issued + net new debt
funding dependence   = external funding / cash burn      (undefined when cash burn is 0)
```

**Fires (SR-1)** when free cash flow is negative for the trailing four quarters, funding dependence is above 1.0, and the
cash on hand covers less than four quarters of burn.

Example: burn of 400, with 300 of new stock and 200 of new debt, gives funding dependence 1.25.

**Blind spots:** quarterly and lagging; misses a fast fraud or a run on liquidity between filings. Off-balance-sheet
leases and purchase commitments do not appear in it; read them from the commitments note.

## Customer concentration

**Inputs (annual report):** the revenue share of each customer the company discloses as significant. Public companies
generally disclose any customer above 10% of revenue in the segment note. Also read the remaining-performance-obligation
or backlog note for the share of contracted revenue.

```
top-customer share   = revenue from largest customer / total revenue
```

**Flag** when the top-customer share is above 25%, or any single customer is above 25% of backlog. A flagged name must
carry a kill criterion on that customer ([kill-criteria.md](kill-criteria.md), K3 and the concentration pattern), and the
customer is recorded as a node for sizing ([pipeline.md](pipeline.md#sizing-by-loss-budget)).

Example: revenue 1,000, of which 600 from one customer, gives a top-customer share of 60%. Flagged.

**Blind spots:** disclosures are annual, and some companies name the customer only by description. A customer can be
indirect: a company may sell to an intermediary whose own demand comes from one buyer.

## Forensic flags

Checked at each annual filing. Each is a prompt to read the filing, not a verdict.

- **Beneish M-Score.** An earnings-manipulation screen from Beneish, "The Detection of Earnings Manipulation",
  *Financial Analysts Journal* 55(5), 1999. It was estimated on a sample of known manipulators against matched
  companies. An implementation records the exact coefficients and input definitions it uses, and its cutoff with a
  source. Beneish, Lee and Nichols, "Earnings Manipulation and Expected Returns", *Financial Analysts Journal* 69(2), 2013,
  use the eight-variable model with a cutoff of -1.78 and note that the right cutoff depends on the relative cost of the
  two kinds of error. Their paper is mainly about predicting returns, a different question from detection. This method
  also reads a score between -2.22 and -1.78 more closely; that band is this method's choice, not a validated interval.
- **Auditor change** or a **non-reliance / restatement** disclosure.
- **Earnings ahead of cash.** Net income above operating cash flow in two consecutive years, or total accruals to total
  assets rising in two consecutive years, where:

  ```
  total accruals to total assets = (net income from continuing operations - operating cash flow) / total assets
  ```

- **Longer asset lives.** The company lengthens the useful life it depreciates its equipment over (an accounting-policy
  note). This is a change in estimate and applies from its effective date forward. Depreciation falls, so pre-tax profit
  rises, but the change itself brings in no cash. Re-measure the next full year's straight-line depreciation both ways:

  ```
  depreciable base        = carrying amount at the change date - residual value
  depreciation, old basis = depreciable base / old remaining life
  depreciation, new basis = depreciable base / new remaining life
  extra pre-tax profit    = old basis - new basis
  ```

  Example: equipment that cost 1,000, with zero residual value, is two years into a 4-year life, so it carries 500. The
  life is extended to 5 years in total. Next year's depreciation falls from 500 / 2 = 250 to 500 / 3 = about 167, adding
  about 83 of pre-tax profit. A flag to read the filing and the peers' choices, not a verdict: a longer life can be right
  if the equipment really lasts.

**Blind spots:** annual, and every one of these can have an innocent explanation. A flag starts a reading; only SR-2's
written record ends one.

## How a builder gets paid

For companies that build capacity for a new technology, record which of three ways they get paid:

| Type | Gets paid | Main risk |
|---|---|---|
| Paid on order | When capacity is ordered (equipment, components) | Orders slow down |
| Paid on use, with debt | As built capacity is used, having borrowed to build it first | Demand arrives late and the debt does not wait |
| Paid later | By using capacity others overbuilt | Slow to show up |

For "paid on use, with debt", record three things:
- Debt and lease obligations against **contracted** use.
- Who holds the contracts, and whether a larger company guarantees them.
- Whether the contracts run **longer or shorter** than the debt. When the contracts outlast the debt, the borrower (or a
  guarantor, where there is one) may need to refinance before the contracts finish paying; when the debt outlasts the
  contracts, it depends on new demand. Tenor alone does not settle either: read the cash flows and how the debt is
  repaid.

In this method, a builder with net cash ranks ahead of one that borrows ahead of contracts, other stages being equal.

## Collar plus income

An options overlay on a stock already held: sell a covered call a little above the price and buy a protective put below
it, both on the same expiration. It is "collar plus income" when the call premium is larger than the put cost.

```
net credit (conservative) = call bid - put ask
net yield                 = net credit / spot
annualized net            = net yield * 365 / days to expiration      (simple, not compounded)
upside cap                = (call strike + net credit) / spot - 1
downside floor            = (put strike + net credit) / spot - 1
```

The cap and the floor describe the payoff **at expiration, relative to today's price, with the premium kept**. They are
not a total return, not an annual return, and not a guarantee: commissions, early assignment of the call and dividends
change the result.

Rules:
- Use the **bid** for what you sell and the **ask** for what you buy. A missing or zero quote means the leg cannot be
  priced, never that it is free.
- Choose the strike **nearest the requested distance**, within a stated tolerance (for example plus or minus 2.5
  percentage points), and report the requested and the actual distance. Coarse strike spacing can make them differ a lot.
- Rank candidates by **annualized net**, so short and long expirations compare fairly; keep raw net yield as a column.
- Check liquidity on **both** legs (open interest and bid-ask spread).
- Note whether an **earnings date falls inside the window**, with the date and whether it is confirmed or estimated. The
  note informs; it does not change the ranking.

Worked input: a call bid of 2.10 and a put ask of 0.60 give a net credit of 2.10 - 0.60 = 1.50.
