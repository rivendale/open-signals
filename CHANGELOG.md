# Changelog

## v0.3

Added:
- Runway, defined term by term, shared by SR-1b and K2.
- SR-1 split into two tests: SR-1a "dependent" (funding dependence above 1.0) and SR-1b "unfunded burn" (runway under
  four quarters, whatever the dependence).
- Collar tax interaction: holding-period check, qualified-covered-call test, loss deferral, constructive-sale check, and
  no collar on a short-term taxable lot without a written reason (sections 1092, 1233(b), 1259).
- One sizing precedence rule, in % of the portfolio, with the binding constraint recorded.
- Data quality: point in time, restatement diff, units and sign, currency and basis, XBRL calculation consistency,
  fundamental-source disagreement, survivorship; the instrument check now depends on the step.
- Wash-sale vectors: the 61-day window, a spouse's account, dividend reinvestment, options.
- README: a copy or citation may not imply endorsement.

Fixed (from the second read of v0.2):
- K2 counted capital spending and debt service but not operating burn. It now uses runway.
- A company that burned cash and could not raise had dependence below 1.0, so SR-1 never fired. SR-1b catches it.
  Funding dependence is "not applicable" when external funding is 0 or less.
- TTM is the sum of four quarters, with Q4 = full year - nine-month year to date. Cash excludes restricted cash.
- Free cash flow is net of stock-based compensation and finance-lease principal; issuance is net of buybacks; IFRS
  filers are normalized before comparison, with IFRS 18 noted from 1 January 2027.
- Sizing: loss budget, "equal weight within a tier" and the 2% to 8% limits contradicted each other. A tier is now a
  ceiling, and the floor applies at entry only, so it no longer conflicts with the drift bands.
- Taxable accounts: the size ceiling binds new cash only; the loss budget and risk trims apply, in a stated order.
- SR-4 is a lot swap that keeps the exposure, so it does not conflict with "price never triggers a sell".
- Forensic flags: score-based flags are annual; event flags (Form 8-K Items 4.01 and 4.02) are checked on receipt.
- One canonical list of what a kill criterion never contains, in kill-criteria.md. The financing terms a company accepts
  are separated from a market spread.
- Annualized net guards against zero days to expiration; days are calendar days.
- Backlog share by customer falls back to revenue share, marked unverified; ASC 280-10-50-42 cited for the 10% rule.
- Portfolio process: "a method for running portfolios", with a cadence the adopter sets, not a trade calendar.
- Uncited claims in principles.md and sell-rules.md are labeled working assumptions (guardrail 8).
- A fund skips S1-S4, not "to sizing". Net cash is a tie-break within a conviction tier.

## v0.2

Added:
- [docs/kill-criteria.md](docs/kill-criteria.md): the shape of a kill criterion, shared criteria for capital-intensive
  builders, patterns for name-specific criteria, the policy-reversal check, and how to learn from other people's sells.
- Customer concentration signal, with a 25% flag and a required kill criterion.
- Forensic flags: longer asset lives (with a re-measurement formula) and a defined "earnings ahead of cash" check.
- "How a builder gets paid" now records contract tenor against debt tenor.
- Sell rules: a guidance trim or opportunity cost is not a sell; builders are decided at filings.
- Portfolio process: cross-sleeve concentration, written exceptions, wash-sale across retirement accounts (Revenue
  Ruling 2008-5), and the split between who proposes and who changes a portfolio.

Fixed (from an independent second read of v0.1):
- The collar example stopped at a yield and return figures, which conflicted with guardrail 3. It now shows the
  arithmetic only, and the formulas state what the cap and floor do and do not mean.
- Settings are framed as this method's choices, not as advice. New guardrail 8.
- The adoption-curve claim is labeled a working assumption; the drawdown claim and the institutional-manager study are
  stated within what the evidence shows.
- M-Score: the implementation must state its model form and cutoff; detection (1999) is separated from return prediction
  (2013).
- Funding dependence: capital expenditure is a positive outflow; flip a vendor's negative sign.

Fixed (from the second read of the v0.2 draft):
- Asset-life formula re-measures prospectively, on carrying amount and remaining lives.
- Kill-criterion patterns are templates that must name a metric, a dated baseline and a threshold; K3 uses the customer's
  share before the event.
- SR-2 and SR-4 still apply in the speculative sleeve.
- M-Score: exact coefficients required; the -2.22 to -1.78 band is this method's choice.
- Wash-sale scope matches Revenue Ruling 2008-5; contract-versus-debt tenor locates refinancing risk at the borrower.

## v0.1

First release: principles, pipeline, sell rules, signals, data quality, portfolio process.
