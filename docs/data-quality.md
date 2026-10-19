# Data quality checks

A signal is only as good as its inputs. Every data pull passes these checks before any signal uses it. A failed check
marks the item **unverified** with a reason. It is never silently dropped, and never silently filled.

| Check | Rule |
|---|---|
| Missing quote | A missing bid or ask, a zero bid, or a crossed market (ask below bid) means "cannot price", never zero cost |
| Source disagreement | When two sources disagree on a price by more than 3%, flag the item and do not use either until resolved |
| Fiscal-year mismatch | Estimates keyed by fiscal year are never compared as calendar years; record the fiscal year end |
| Staleness | Data older than the last trading day is flagged stale; holidays are accounted for |
| Instrument type | Confirm the instrument is the type expected (common stock or fund); refuse anything else |
| Empty versus failed | A source that returns nothing is distinguished from a source that failed; a quiet day is not an outage |
| Duplicates | Share-class spellings of one company (for example a dot and a hyphen variant) collapse to one record |
| Unavailable source | A source refusing a request (not permitted on the plan, rate limited) marks that section unavailable, never empty |

## Testing

Each check has a test that fails when the check is removed, run on small made-up samples. A check that cannot fail is not
a check.
