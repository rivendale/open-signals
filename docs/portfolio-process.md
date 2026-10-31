# Portfolio process

This is a method for running portfolios. The numbers below are the method's settings, chosen by its author; an adopter
sets its own and records them.

## When portfolios change

- **At a scheduled review** that follows the filings the method reads. The adopter sets its own review cadence and
  records it.
- **When a written sell rule or kill criterion fires.**
- A price move alone is not a reason to review.
- Kill criteria are checked at every filing and current report in between ([kill-criteria.md](kill-criteria.md#when-they-are-checked));
  checking is continuous, changing is not.

## How portfolios are organized

- **Each sleeve has one job**: broad market exposure; a defensive sleeve that holds all the hedges; profitable growth
  companies; a speculative sleeve where each name is small and sized to be lost; and a sleeve for market infrastructure
  (exchanges, brokers, custody, settlement).
- **One home per name**: a stock or theme lives in one sleeve only, so its total exposure is visible.
- **The hedge level of a portfolio is its defensive weight**, instead of hedges spread across sleeves. A fund that
  hedges lives in the defensive sleeve only, even if it also fits elsewhere.
- **Concentration is checked across sleeves**, not just within one: two names that sell to the same customer are one
  exposure to that customer.

## Limits

Sizes are set by the precedence rule in [pipeline.md](pipeline.md#sizing-by-loss-budget). The limits below are its caps.

- **Size ceiling:** no single stock above 8% of its sleeve. Names in the speculative sleeve stay at 5% of the sleeve or
  less. A ceiling applies to the target; a held weight is then governed by its drift band.
- **Entry floor:** a new name enters at 2% of its sleeve or more, or not at all. The floor applies at entry only.
- **Drift:** rebalance a weight only when it moves more than 25% away from its target (a 4% target: below 3% or above
  5%), checked at the scheduled review.
- **Loss budget:** applies to every held position, at every review. A breach is a risk trim
  ([sell-rules.md](sell-rules.md#the-four-sell-rules)).
- **Cash:** no standing reserve; additions are funded at the review.
- **Exceptions are written down.** A weight outside a limit is either fixed at the next review or recorded as an
  exception with its reason and an end date.

## Taxable and retirement accounts are run differently

| | Retirement accounts | Taxable accounts |
|---|---|---|
| Drift bands | Applied at each review | Not applied |
| Size ceiling | Applies to targets and to new cash | Applies to new cash only: no buy takes a name above its ceiling, and a name above it is not sold down for that reason alone |
| Loss budget | Applies; a breach is a risk trim | Applies; a breach is a risk trim (below) |
| What changes holdings | The scheduled review and the sell rules | The sell rules, tax-loss harvesting, risk trims, small position updates, and new cash |
| New cash | Follows the targets | Buys toward the sleeve's underweights |
| Selling | Sell rules, risk trims and rebalancing | A sell rule firing, a risk trim, or a loss harvest; never drift or a size ceiling alone |
| Holding period | Not a factor | A trim of a position held under a year waits until it is long-term, unless a sell rule fires, a loss budget is breached, or it is a loss harvest. A collar can restart the holding period, so a short-term lot is not collared without a written reason ([signals.md](signals.md#tax-interaction)) |

A taxable account reflects when it was opened and what it started with; the target is a guide for new money, not
something to force it back to.

A **risk trim in a taxable account** comes last. First, add elsewhere so the budget is restored. Next, trim the same
exposure where it is held in a retirement account. Only then sell in the taxable account, choosing the lots that realize
the least short-term gain, and record the choice.

## Placement

The method's placement settings follow. Tax treatment depends on the investor; this is not tax advice.

- Overlapping funds are consolidated inside tax-advantaged accounts, never by selling at a gain in taxable accounts.
- Holdings whose income is taxed as ordinary income, such as most real-estate investment trust dividends, are placed in
  tax-advantaged accounts when there is room.
- Losses are harvested in taxable accounts first. The 30-day wash-sale rule is observed across every account, including
  retirement accounts. The IRS has ruled that buying substantially identical securities in an IRA or Roth IRA within 30
  days before or after a loss sale in a taxable account disallows the loss, and the IRA's basis is not increased
  (Revenue Ruling 2008-5). The ruling does not cover every kind of retirement plan; this method treats them all the same
  way.
- **The wash-sale window is 61 days:** the 30 days before the sale, the day of the sale, and the 30 days after
  (Internal Revenue Code section 1091). Before a harvest, check every way a replacement can be acquired in that window:
  - a purchase in any of the investor's own accounts, taxable or retirement;
  - a purchase in a spouse's account (IRS Publication 550 treats a spouse's purchase as a wash sale);
  - a dividend reinvestment in any of those accounts, which is a purchase like any other; turn reinvestment off for the
    window;
  - a contract or option to acquire substantially identical stock, such as a bought call (section 1091(a)); Publication
    550 also warns that selling a put deep in the money can count.
- A long-term holding period means more than one year (Internal Revenue Code section 1222).

## Who does what

- **Research proposes; the person accountable for the account changes it.** A portfolio change is written as a proposal
  with its reason and the rule behind it. The edit is made by whoever is accountable for the portfolio, in their own
  system, and recorded there.
- **A change and its check are separate.** The rule that fired, the proposal and the record of the change are kept as
  three entries, so a later review can see each one.
