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
| [docs/sell-rules.md](docs/sell-rules.md) | Hold is the default; the four sell rules (SR-1 has two tests); what never triggers a sell |
| [docs/kill-criteria.md](docs/kill-criteria.md) | How to write the condition that ends a position; shared criteria for builders; the policy-reversal check |
| [docs/signals.md](docs/signals.md) | Signal definitions with formulas: funding dependence and runway, customer concentration, forensic flags (including longer asset lives), how a builder gets paid, the collar-plus-income math and its tax interaction |
| [docs/data-quality.md](docs/data-quality.md) | Checks every data pull must pass before a signal is trusted |
| [docs/portfolio-process.md](docs/portfolio-process.md) | Cadence, drift bands, size limits, and how taxable and retirement accounts are handled differently |
| [docs/thresholds.md](docs/thresholds.md) | Every numeric threshold, where it is defined, and its source |
| [spec/](spec/) | The machine-readable spec and its synthetic test vectors (below) |
| [reference/](reference/) | A small reference implementation that checks the vectors |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How changes are proposed, reviewed and versioned |
| [CHANGELOG.md](CHANGELOG.md) | What changed in each version |

## How it is meant to be used

Each user pulls its own market data, from its own vendors, and implements these rules its own way. What is shared is
the rulebook: how a method reasons, which checks it runs and when. The settings it gives (size limits, drift bands,
placement) are the author's choices, shown so the method is complete; they are not a recommendation for any reader's
portfolio. Cite a tagged version ("open-signals v0.3") so two implementations can say they follow the same rules.

## Machine-readable spec

[spec/signals.json](spec/signals.json) encodes every computable rule in the docs (TTM, funding dependence, SR-1a,
runway, SR-1b, K1 to K3, customer concentration, the forensic flags, collar pricing, sizing precedence, drift bands and
the wash-sale window). For each rule it gives the inputs with unit and sign, the formula, the thresholds, the rule ID and
a link to the doc section. The docs own the meaning; where the spec and a doc disagree, the doc wins. Where a doc does
not settle a case, the rule is marked `ambiguous` with a note instead of a guess.

[spec/vectors/](spec/vectors/) holds synthetic test vectors: made-up companies and numbers only, each with its inputs,
expected outputs and the doc section it tests. [reference/open_signals/](reference/open_signals/) is a stdlib-only
Python implementation (MIT) that computes the spec. From the repository root:

```
PYTHONPATH=reference python3 -m open_signals.check spec/vectors
PYTHONPATH=reference python3 -m unittest discover -s reference/tests
```

The spec is JSON, not YAML, so that any implementation, and this one, can read it with a standard library parser and
no dependency. An implementation that passes every vector can say so for the tagged version it follows.

## What never goes in

Tickers or company names used as examples of what to buy or sell, holdings, model weights, performance or back-tested
results, client information, text from paid research services, and anything that would let a reader anticipate a
specific trade.

## License

Text: [CC BY 4.0](LICENSE). Code in [reference/](reference/): MIT ([reference/LICENSE](reference/LICENSE)).

A copy, adaptation or citation of this material may not suggest that the author endorses it, its user, or any portfolio
it is used for (CC BY 4.0, section 2(a)(6)).
