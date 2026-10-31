# Signal definitions

Every signal states its inputs, its formula, when it is checked, and its known blind spots. All examples use made-up
numbers. An implementation records the version of this file it follows and any threshold it set itself.

## Funding dependence

**Inputs (from the cash-flow statement, trailing twelve months):** operating cash flow, stock-based compensation,
capital expenditure, finance-lease principal paid, stock issued, stock repurchased, and net new debt (including
convertibles).

**Trailing twelve months (TTM)** is the sum of the last four fiscal quarters. Quarterly cash-flow statements are usually
year to date, so each quarter is the difference of two year-to-date figures. The fourth quarter is the full year minus
the nine-month year to date. A single quarter is never multiplied by four.

Capital expenditure, finance-lease principal and stock repurchased are taken as **positive cash outflows**. Some data
vendors report them as negative numbers; flip the sign before use, or the formulas below add them instead of
subtracting them.

```
free cash flow       = operating cash flow - stock-based compensation - capital expenditure
                       - finance-lease principal paid
cash burn            = max(0, -free cash flow)
net stock issued     = stock issued - stock repurchased
external funding     = net stock issued + net new debt
funding dependence   = external funding / cash burn
```

Funding dependence is **not applicable** when cash burn is 0 or external funding is 0 or less. It is recorded as "not
applicable", never as 0. A company that burns cash and raises nothing has no dependence ratio; the runway test below
still applies to it.

Why the two deductions:
- **Stock-based compensation** is added back in operating cash flow because it is not paid in cash. It is still a cost:
  the company pays staff in shares instead of cash. Deducting it treats the two the same way.
- **Finance-lease principal.** Under US GAAP (ASC 842), payments on an operating lease sit in operating cash flow, while
  the principal part of a finance-lease payment sits in financing. Deducting finance-lease principal puts a company
  that leases on finance terms on the same basis as one that leases on operating terms or buys.

**IFRS filers.** Under IFRS 16 the principal part of every lease payment is a financing cash flow, and IAS 7 lets a
company show interest paid in operating or in financing. To compare with a US GAAP filer, move lease principal paid, and
any interest paid shown in financing, into operating cash flow before using the formula. Do not then deduct finance-lease
principal a second time. IFRS 18, with its amendments to IAS 7, applies to annual periods beginning on or after
1 January 2027; for most companies it puts interest paid in financing, so the move becomes routine for those periods.
Record the basis (US GAAP or IFRS) and each adjustment made.

**Fires SR-1a (dependent)** when free cash flow is negative for the trailing twelve months and funding dependence is
above 1.0: the burn is paid for from outside, not by the business.

Example: burn of 400, with 350 of stock issued, 50 repurchased and 200 of net new debt, gives external funding of 500
and funding dependence 1.25. SR-1a fires.

### Runway

```
liquidity            = cash + short-term investments + committed undrawn facilities
annual outflow       = operating cash burn + capital expenditure + scheduled debt service + lease payments
runway (quarters)    = 4 * liquidity / annual outflow
```

- **Cash:** cash and cash equivalents, excluding restricted cash.
- **Short-term investments:** marketable securities the company reports as current, excluding any that are pledged or
  restricted.
- **Committed undrawn facilities:** the undrawn part of committed credit lines the company can draw today, with every
  draw condition currently met. An uncommitted line, an at-the-market equity program, or a facility with an unmet
  condition is not counted.
- **Operating cash burn:** max(0, -(TTM operating cash flow + interest paid inside operating cash flow, including the
  interest part of finance-lease payments + operating-lease payments)). Use operating cash flow after the IFRS
  normalization above. This is the burn before financing costs, so interest and leases are not counted twice.
  Stock-based compensation is not deducted here; it is not a cash outflow.
- **Capital expenditure:** the company's stated capital spending for the next twelve months; TTM capital expenditure
  when it states none.
- **Scheduled debt service:** interest and principal due in the next twelve months, from the debt maturity note, excluding lease
  liabilities (counted under lease payments).
- **Lease payments:** all lease payments due in the next twelve months, operating and finance, from the lease maturity
  table.

Runway is unlimited when annual outflow is 0.

**Fires SR-1b (unfunded burn)** when the business burns cash (operating cash burn plus TTM capital expenditure is above
0) and runway is under four quarters, whatever the funding dependence, including "not applicable". The gate is cash, not
free cash flow, so stock-based compensation alone cannot make a cash-generating business read as burning.

Example: burn of 400, no stock or debt raised, so funding dependence is not applicable. Cash 150, short-term investments
50 and no undrawn facility give liquidity of 200. Operating cash burn 250, capital expenditure 150, debt service 60 and
lease payments 40 give an annual outflow of 500. Runway is 4 * 200 / 500 = 1.6 quarters. SR-1b fires.

The same runway is the K2 measure for capital-intensive builders ([kill-criteria.md](kill-criteria.md)). K2 does not
need a burn; heavy debt service alone can fire it.

**Blind spots:** quarterly and lagging; misses a fast fraud or a run on liquidity between filings. Runway uses the
company's stated plans, which can change. Purchase commitments do not appear in it; read them from the commitments note.

## Customer concentration

**Inputs (annual report):** the revenue share of each customer the company discloses as significant. Under US GAAP a
company discloses the revenue from each customer that is 10% or more of its revenue, and the segments that report it
(ASC 280-10-50-42). It need not name the customer. A group of companies under common control counts as one customer.
The federal government counts as one customer; so do a state government, a local government and a foreign government,
each in its own right. Also read the remaining-performance-obligation or backlog note for the share of contracted
revenue.

```
top-customer share   = revenue from largest customer / total revenue
backlog share        = backlog from largest customer / total backlog
```

**Backlog share is rarely disclosed by customer.** When it is not, use the customer's revenue share in its place, and
mark the backlog share **unverified** with that reason. The fallback can be wrong either way: a new contract can make a
customer's backlog share far larger than its revenue share.

**Flag** when the top-customer share is above 25%, or any single customer is above 25% of backlog (disclosed or
fallback). A flagged name must carry a kill criterion on that customer ([kill-criteria.md](kill-criteria.md), K3 and the
concentration pattern), and the customer is recorded as a node for sizing ([pipeline.md](pipeline.md#sizing-by-loss-budget)).

Example: revenue 1,000, of which 600 from one customer, gives a top-customer share of 60%. Flagged.

**Blind spots:** disclosures are annual, and some companies name the customer only by description. A customer can be
indirect: a company may sell to an intermediary whose own demand comes from one buyer.

## Forensic flags

Each flag is a prompt to read the filing, not a verdict. There are two kinds, checked on different schedules:

- **Score-based flags** (the M-Score, earnings ahead of cash, longer asset lives) need a full year of figures. They are
  checked at each annual filing.
- **Event flags** (an auditor change, a non-reliance notice, a restatement) are checked **on receipt**. A US company
  reports an auditor change under Item 4.01 of a current report (Form 8-K), and a finding that past financial
  statements can no longer be relied on under Item 4.02. Neither waits for the annual filing.

- **Beneish M-Score.** An earnings-manipulation screen from Beneish, "The Detection of Earnings Manipulation",
  *Financial Analysts Journal* 55(5), 1999. It was estimated on a sample of known manipulators against matched
  companies. An implementation records the exact coefficients and input definitions it uses, and its cutoff with a
  source. Beneish, Lee and Nichols, "Earnings Manipulation and Expected Returns", *Financial Analysts Journal* 69(2), 2013,
  use the eight-variable model with a cutoff of -1.78 and note that the right cutoff depends on the relative cost of the
  two kinds of error. Their paper is mainly about predicting returns, a different question from detection. This method
  also reads a score between -2.22 and -1.78 more closely; that band is this method's choice, not a validated interval.
- **Auditor change** (Item 4.01) or a **non-reliance / restatement** disclosure (Item 4.02). An event flag.
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

**Blind spots:** the score-based flags are annual, and every one of these can have an innocent explanation. A flag
starts a reading; only SR-2's written record ends one.

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

In this method, net cash is a tie-break within a conviction tier: between two builders in the same tier, other stages
being equal, the one with net cash is sized first. It does not move a name to a higher tier.

## Collar plus income

An options overlay on a stock already held: sell a covered call a little above the price and buy a protective put below
it, both on the same expiration. It is "collar plus income" when the call premium is larger than the put cost.

```
net credit (conservative) = call bid - put ask
net yield                 = net credit / spot
annualized net            = net yield * 365 / days to expiration      (simple, not compounded; days >= 1)
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
- **Days to expiration** are calendar days from the pricing date to the expiration date. A candidate with fewer than 1
  day is excluded, never annualized; the formula would divide by zero.
- Rank candidates by **annualized net**, so short and long expirations compare fairly; keep raw net yield as a column.
- Check liquidity on **both** legs (open interest and bid-ask spread).
- Note whether an **earnings date falls inside the window**, with the date and whether it is confirmed or estimated. The
  note informs; it does not change the ranking.

Worked input: a call bid of 2.10 and a put ask of 0.60 give a net credit of 2.10 - 0.60 = 1.50.

### Tax interaction

In a taxable account a collar can change the tax treatment of the stock under it. The checks below are this method's
summary of the rules it screens for, with the Internal Revenue Code sections cited. It is a rule summary, not tax
advice; the treatment depends on the investor, and an adopter confirms it with its own tax adviser. A tax-advantaged account does not need
this block.

Before a collar is opened on a lot in a taxable account, record:

1. **Holding period.** Whether the lot has been held more than one year (section 1222). Buying a put on stock held one
   year or less is treated like a short sale: the holding period is wiped out and starts again when the put is
   exercised, sold or expires (section 1233(b)). A stock and a protective put are also a straddle; for a lot that was
   not long-term when the straddle began, the holding period starts again when the straddle ends (section 1092 and
   Treasury Regulation 1.1092(b)-2T). Either way, a collar on a short-term lot works against the rule that a trim
   waits until the lot is long-term ([portfolio-process.md](portfolio-process.md#taxable-and-retirement-accounts-are-run-differently)).
2. **Qualified covered call.** Whether the call alone would be a qualified covered call: exchange-traded, more than 30
   days to expiration when written, and not deep in the money (section 1092(c)(4)). A qualified covered call written by
   itself escapes the straddle rules. In a collar it does not help, because the put already makes a straddle. A
   qualified covered call that is in the money still suspends the stock's holding period while it is open
   (section 1092(f)).
3. **Loss deferral.** A loss on one leg of a straddle is deferred to the extent of unrecognized gain in the offsetting
   position (section 1092(a)). A collared lot is therefore a poor candidate for an SR-4 loss harvest: record any
   deferred loss, and unwind the collar before the harvest is planned.
4. **Constructive sale.** Whether the collar, on an appreciated lot, removes substantially all of both the risk of loss
   and the chance of gain. If it does, the lot may be treated as sold, and the gain taxed, when the collar is opened
   (section 1259). Treasury has not issued the regulations section 1259(c)(1)(E) authorizes, so there is no
   bright-line band; this method records the put and call strikes as a share of spot and the reason the band is wide
   enough. A collar closed on or before the 30th day after the end of the tax year in which it was opened, with the
   stock then held for 60 days without any position that reduces its risk of loss, falls under the closed-transaction
   exception (section 1259(c)(3)). The exception removes the constructive sale; it does not lift the straddle rules.

**Rule:** no collar on a short-term lot in a taxable account, unless the written record states the holding-period
effect and why the collar is still wanted.
