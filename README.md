# open-signals

An open rulebook for long-horizon equity research: the signals, rules and procedures, written down so they can be
reviewed, versioned and tested. It shares the **method**, never positions.

**Educational material only. Not investment advice, not an offer of advisory services, and not a recommendation to buy
or sell any security.** Nothing here describes what anyone holds, what any model contains, or how any strategy performed.
See [COMPLIANCE.md](COMPLIANCE.md).

## What is in it

| File | What it covers |
|---|---|
| [docs/principles.md](docs/principles.md) | The research stance: a barbell of real assets and high-growth technology, themes plus best ideas |
| [docs/pipeline.md](docs/pipeline.md) | The stages a name passes before it can be held, ending in sizing by loss budget |
| [docs/sell-rules.md](docs/sell-rules.md) | Hold is the default; the four sell rules; what never triggers a sell |
| [docs/signals.md](docs/signals.md) | Signal definitions with formulas: funding dependence, forensic flags, how a business gets paid, the collar-plus-income math |
| [docs/data-quality.md](docs/data-quality.md) | Checks every data pull must pass before a signal is trusted |
| [docs/portfolio-process.md](docs/portfolio-process.md) | Cadence, drift bands, size limits, and how taxable and retirement accounts are handled differently |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How changes are proposed, reviewed and versioned |

## How it is meant to be used

Each user pulls its own market data, from its own vendors, and implements these rules its own way. What is shared is
the rulebook. Cite a tagged version ("open-signals v0.1") so two implementations can say they follow the same rules.

## What never goes in

Tickers or company names used as examples of what to buy or sell, holdings, model weights, performance or back-tested
results, client information, text from paid research services, and anything that would let a reader anticipate a
specific trade.

## License

Text: [CC BY 4.0](LICENSE). Any code added later: MIT.
