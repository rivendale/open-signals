# Hold, and the four sell rules

## Why selling is asymmetric

This method's **working assumption**: selling a winner early forfeits an open-ended upside, while holding a loser costs
at most a position that sizing already capped. That is a premise about payoffs, not a cited finding. So the rules are
deliberately lopsided:

- **Hold is the default.** A sell needs a written reason; a hold does not.
- **Loss control lives in sizing, not in selling.**
- **Nothing ever fires because a position went up.**
- **A sell rule must clear a higher bar than the buy that created the position.** In one large study of institutional
  portfolio managers, their buys added value while their sells did worse than a random choice of what to sell. The study
  motivates the bar; it does not prove these particular rules. (Akepanidtaworn, Di Mascio, Imas and Schmidt,
  "Selling Fast and Buying Slow: Heuristics and Trading Performance of Institutional Investors", *Journal of Finance*
  78(6), 2023, https://doi.org/10.1111/jofi.13271.)

## The four sell rules

1. **SR-1 Funding.** Two tests, checked at each quarterly filing (see [signals.md](signals.md#funding-dependence)):
   - **SR-1a Dependent.** The business burns cash and funds the burn by issuing stock or debt: funding dependence above
     1.0.
   - **SR-1b Unfunded burn.** The business burns cash and its runway is under four quarters, whether or not it is
     raising money ([signals.md](signals.md#runway)).

   Neither test is applied to the speculative sleeve, where burn and outside funding are the profile. There the kill
   criteria carry that risk, including K2 for builders.
2. **SR-2 Forensic flag.** Two kinds (see [signals.md](signals.md#forensic-flags)). A score-based flag is checked at
   each annual filing. An event flag (an auditor change, a non-reliance notice or a restatement) is checked on receipt of
   the filing that discloses it. A flag leads to a reading; the sell needs the reading to confirm it.
3. **SR-3 Kill criterion fires.** The name's own pre-written kill criterion crosses its threshold (see
   [kill-criteria.md](kill-criteria.md)).
4. **SR-4 Tax.** Harvest a loss and keep the exposure through a similar but not substantially identical holding, observing
   the wash-sale rule across all of the investor's accounts
   ([portfolio-process.md](portfolio-process.md#placement) lists the ways a replacement can be acquired). SR-4 is a
   **lot swap**, not an exit: the exposure stays, and only the tax lot changes. An unrealized loss makes the swap
   possible; it never decides whether the exposure is held. That is why it does not conflict with the rule that price
   never triggers a sell. A collared lot needs the straddle check first ([signals.md](signals.md#tax-interaction)).

A **risk trim** is not a sell rule: it happens only when a sizing budget is breached, and adding elsewhere is preferred to
trimming. It applies in taxable accounts too, in the order set in
[portfolio-process.md](portfolio-process.md#taxable-and-retirement-accounts-are-run-differently).

## Before any sell, in writing

1. The named observable and the threshold it crossed.
2. The filing or report, with its date, where it surfaced.
3. Which rule it is (SR-1a, SR-1b, SR-2, SR-3 or SR-4).
4. Confirmation that none of the items below was the reason.

## What never triggers a sell

What a kill criterion may never contain is listed once, in
[kill-criteria.md](kill-criteria.md#what-a-kill-criterion-never-contains); none of the items below may trigger a sell
either.

- **Price level or drawdown depth.** Neither is a fact about the business; the kill criteria are.
- **Valuation multiple.**
- **A narrative "thesis break"** that is not one of the written kill criteria.
- **Headlines or sentiment.**
- **A guidance trim or an opportunity cost.** A company guiding a little lower, or a better idea elsewhere, is a reason to
  review at the next filing, not to sell. Missing the company's **own** target by the margin a kill criterion names is
  different, and is SR-3.

## Other instruments

- **Funds:** sell only when the proxy fails (it stops tracking its own index, or its holdings change character), never
  because the price fell.
- **Private positions:** there is usually no sell decision; the whole decision is at the buy.
- **Themes:** a theme does not sell; it expires on a date set when it was opened.
- **Capital-intensive builders:** decided at their filings, with SR-1a, SR-1b and the kill criteria measured, never on a
  price move between filings.
