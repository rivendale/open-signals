# Data quality checks

A signal is only as good as its inputs. Every data pull passes these checks before any signal uses it. A failed check
marks the item **unverified** with a reason. It is never silently dropped, and never silently filled.

## Prices and instruments

| Check | Rule |
|---|---|
| Missing quote | A missing bid or ask, a zero bid, or a crossed market (ask below bid) means "cannot price", never zero cost |
| Source disagreement | When two sources disagree on a price by more than 3%, flag the item and do not use either until resolved |
| Staleness | Data older than the last trading day is flagged stale; holidays are accounted for |
| Instrument type | Confirm the instrument is the type the step expects, and refuse anything else (below) |
| Empty versus failed | A source that returns nothing is distinguished from a source that failed; a quiet day is not an outage |
| Duplicates | Share-class spellings of one company (for example a dot and a hyphen variant) collapse to one record |
| Unavailable source | A source refusing a request (not permitted on the plan, rate limited) marks that section unavailable, never empty |

**The expected instrument type depends on the step:**
- Pipeline and holdings: common stock or a fund.
- The collar: listed equity options on the held stock, with the contract size, exercise style and expiration
  confirmed. An adjusted contract (after a split or a merger) is flagged, because its deliverable may no longer be 100
  shares.
- Stage S2, the capital stack: preferred stock and convertible securities are expected here and are read, not refused.
  Record each one's ranking, conversion terms and maturity.
- A depositary receipt (ADR) is accepted as the stock it represents only when the ratio of receipts to shares is
  recorded, and per-share figures are converted with it.

## Fundamentals

| Check | Rule |
|---|---|
| Point in time | A signal tested on past dates uses figures **as first reported**, with the filing date, not today's restated figures. A restated figure was not known on the earlier date; using it is look-ahead |
| Restatement diff | When a figure is restated, keep both versions and record the difference and the filing that changed it. A restatement is also an event flag ([signals.md](signals.md#forensic-flags)) |
| Units, scale and sign | Confirm the unit (thousands or millions), the share count basis (basic or diluted), and the sign convention, for example capital expenditure as a positive outflow ([signals.md](signals.md#funding-dependence)) |
| Currency and basis | Record the reporting currency and the accounting basis (US GAAP or IFRS). Convert at a stated rate and date. Never mix bases in one ratio without the normalization in [signals.md](signals.md#funding-dependence) |
| Calculation consistency | Totals tie to their parts (for example the three cash-flow sections, plus the exchange-rate effect, sum to the change in cash, cash equivalents and restricted cash), using the filing's XBRL calculation relationships where they exist. A break is flagged, not forced to tie |
| Fiscal-year mismatch | Estimates keyed by fiscal year are never compared as calendar years; record the fiscal year end |
| Fundamental-source disagreement | When two sources give different values for the same reported line, the filing decides. Until it is read, the item is unverified |
| Survivorship | A screen run on past dates includes companies that were later delisted, acquired or went bankrupt. A list built from today's names only is flagged |

## Testing

Each check has a test that fails when the check is removed, run on small made-up samples. A check that cannot fail is not
a check.
