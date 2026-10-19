# Signal definitions

Every signal states its inputs, its formula, when it is checked, and its known blind spots. All examples use made-up
numbers.

## Funding dependence

**Inputs (from the cash-flow statement, trailing four quarters):** operating cash flow, capital expenditure, stock
issued, net new debt (including convertibles).

```
free cash flow       = operating cash flow - capital expenditure
cash burn            = max(0, -free cash flow)
external funding     = stock issued + net new debt
funding dependence   = external funding / cash burn      (undefined when cash burn is 0)
```

**Fires (SR-1)** when free cash flow is negative for the trailing four quarters, funding dependence is above 1.0, and the
cash on hand covers less than four quarters of burn.

Example: burn of 400, with 300 of new stock and 200 of new debt, gives funding dependence 1.25.

**Blind spots:** quarterly and lagging; misses a fast fraud or a run on liquidity between filings.

## Forensic flags

Checked at each annual filing:
- **Beneish M-Score** above its published threshold, an earnings-manipulation screen (Beneish, "The Detection of
  Earnings Manipulation", *Financial Analysts Journal* 55(5), 1999; Beneish, Lee and Nichols, "Earnings Manipulation and
  Expected Returns", *Financial Analysts Journal* 69(2), 2013). Strong in its authors' tests; treat it as a flag to read
  the filing, not a verdict.
- **Auditor change** or a **non-reliance / restatement** disclosure.
- **Accruals** growing much faster than revenue.

## How a builder gets paid

For companies that build capacity for a new technology, record which of three ways they get paid:

| Type | Gets paid | Main risk |
|---|---|---|
| Paid on order | When capacity is ordered (equipment, components) | Orders slow down |
| Paid on use, with debt | As built capacity is used, having borrowed to build it first | Demand arrives late and the debt does not wait |
| Paid later | By using capacity others overbuilt | Slow to show up |

For "paid on use, with debt", check debt and lease obligations against **contracted** use, and who holds the contracts.
Prefer builders with net cash over builders that borrow ahead of contracts.

## Collar plus income

An options overlay on a stock already held: sell a covered call a little above the price and buy a protective put below
it, both on the same expiration. It is "collar plus income" when the call premium is larger than the put cost.

```
net credit (conservative) = call bid - put ask
net yield                 = net credit / spot
annualized net            = net yield * 365 / days to expiration
upside cap                = (call strike + net credit) / spot - 1
downside floor            = (put strike + net credit) / spot - 1
```

Rules:
- Use the **bid** for what you sell and the **ask** for what you buy. A missing or zero quote means the leg cannot be
  priced, never that it is free.
- Choose the strike **nearest the requested distance**, within a stated tolerance (for example plus or minus 2.5
  percentage points), and report the requested and the actual distance. Coarse strike spacing can make them differ a lot.
- Rank candidates by **annualized net**, so short and long expirations compare fairly; keep raw net yield as a column.
- Check liquidity on **both** legs (open interest and bid-ask spread).
- Note whether an **earnings date falls inside the window**, with the date and whether it is confirmed or estimated. The
  note informs; it does not change the ranking.

Example: spot 100, 30 days, call 102 bid 2.10, put 85 ask 0.60. Net credit 1.50, net yield 1.5%, annualized about
18.3%, upside cap +3.5%, downside floor -13.5%.
