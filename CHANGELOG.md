# Changelog

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

## v0.1

First release: principles, pipeline, sell rules, signals, data quality, portfolio process.
