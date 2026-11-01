# Threshold provenance

Every number this method uses as a threshold, where it is defined, and where it comes from. The linked section owns the
number and its meaning; this table only says where each one comes from. A source is either a citation already given in
the linked doc, or **this method's setting (working assumption)**: a choice made by the method's author, not an
empirical finding and not advice to any reader ([COMPLIANCE.md](../COMPLIANCE.md), guardrail 8). An adopter sets its
own values and records them.

The ID column names the threshold in [spec/signals.json](../spec/signals.json), where there is one.

## Signals, sell rules and kill criteria

| ID | Threshold | Value | Defined in | Source |
|---|---|---|---|---|
| `funding_dependence_max` | SR-1a fires when funding dependence is above | 1.0 | [signals.md](signals.md#funding-dependence) | This method's setting (working assumption) |
| `runway_min_quarters` | SR-1b and K2 fire when runway is under | 4 quarters (12 months) | [signals.md](signals.md#runway), [kill-criteria.md](kill-criteria.md#shared-criteria-for-capital-intensive-builders) | This method's setting (working assumption) |
| none | Trailing twelve months | Last 4 fiscal quarters | [signals.md](signals.md#funding-dependence) | Definition used by this method |
| `concentration_max_share` | Customer concentration flag: top-customer share, or any customer's backlog share, above | 25% | [signals.md](signals.md#customer-concentration) | This method's setting (working assumption) |
| none | Customer revenue a US GAAP filer must disclose | 10% or more of revenue | [signals.md](signals.md#customer-concentration) | ASC 280-10-50-42, as cited in signals.md |
| `k3_backlog_share_min` | K3 anchor customer: share of backlog at the last filing before the event above | 25% | [kill-criteria.md](kill-criteria.md#shared-criteria-for-capital-intensive-builders) | This method's setting (working assumption) |
| `k3_contract_cut_min` | K3: cut in contract value above | 25% | [kill-criteria.md](kill-criteria.md#shared-criteria-for-capital-intensive-builders) | This method's setting (working assumption) |
| none | Beneish M-Score cutoff | -1.78 | [signals.md](signals.md#forensic-flags) | Beneish, Lee and Nichols, *Financial Analysts Journal* 69(2), 2013, as cited in signals.md. The method does not fix a cutoff; an implementation records its own, with a source |
| `mscore_read_closely_lower` | M-Score band read more closely | -2.22 to -1.78 | [signals.md](signals.md#forensic-flags) | This method's setting (working assumption); not a validated interval |
| `earnings_ahead_of_cash_years` | Earnings ahead of cash: consecutive years | 2 | [signals.md](signals.md#forensic-flags) | This method's setting (working assumption) |
| `collar_min_days_to_expiration` | Collar candidate excluded below | 1 calendar day | [signals.md](signals.md#collar-plus-income) | This method's setting: the annualizing formula divides by days |
| none | Annualizing basis for a collar | 365 days, simple | [signals.md](signals.md#collar-plus-income) | This method's setting (working assumption) |
| none | Strike tolerance around the requested distance | plus or minus 2.5 percentage points | [signals.md](signals.md#collar-plus-income) | An example in the doc, not a setting; the implementation states its own |

## Portfolio process and sizing

| ID | Threshold | Value | Defined in | Source |
|---|---|---|---|---|
| `size_ceiling_share_of_sleeve` | Size ceiling for a single stock | 8% of its sleeve | [portfolio-process.md](portfolio-process.md#limits) | This method's setting (working assumption) |
| `speculative_ceiling_share_of_sleeve` | Size ceiling in the speculative sleeve | 5% of the sleeve | [portfolio-process.md](portfolio-process.md#limits) | This method's setting (working assumption) |
| `entry_floor_share_of_sleeve` | Entry floor, at entry only | 2% of its sleeve | [portfolio-process.md](portfolio-process.md#limits) | This method's setting (working assumption) |
| `speculative_stressed_loss_per_dollar` | Stressed loss per dollar in the speculative sleeve | 1.0 | [pipeline.md](pipeline.md#sizing-by-loss-budget) | This method's setting: each name is sized to be lost in full |
| `drift_band_relative` | Rebalance when a weight moves away from its target by more than | 25% of the target | [portfolio-process.md](portfolio-process.md#limits) | This method's setting (working assumption) |

## Tax

These are rule summaries, not tax advice; an adopter confirms them with its own tax adviser.

| ID | Threshold | Value | Defined in | Source |
|---|---|---|---|---|
| `wash_sale_days_each_side` | Wash-sale window | 30 days before the sale, the sale day, 30 days after (61 days) | [portfolio-process.md](portfolio-process.md#placement) | Internal Revenue Code section 1091, as cited in portfolio-process.md |
| none | Long-term holding period | More than one year | [portfolio-process.md](portfolio-process.md#placement), [signals.md](signals.md#tax-interaction) | Internal Revenue Code section 1222, as cited in both |
| none | Qualified covered call: time to expiration when written | More than 30 days | [signals.md](signals.md#tax-interaction) | Internal Revenue Code section 1092(c)(4), as cited in signals.md |
| none | Constructive-sale closed-transaction exception | Closed by the 30th day after the tax year ends; stock then held 60 days without a position that reduces its risk of loss | [signals.md](signals.md#tax-interaction) | Internal Revenue Code section 1259(c)(3), as cited in signals.md |

## Data quality

| ID | Threshold | Value | Defined in | Source |
|---|---|---|---|---|
| none | Two price sources disagree by more than | 3% | [data-quality.md](data-quality.md#prices-and-instruments) | This method's setting (working assumption) |
| none | Stale data | Older than the last trading day | [data-quality.md](data-quality.md#prices-and-instruments) | This method's setting (working assumption) |

## Principles

| ID | Threshold | Value | Defined in | Source |
|---|---|---|---|---|
| none | Adoption level after which the curve is taken to move faster | About 5%, toward about 50% | [principles.md](principles.md#adoption-curves-not-price) | Working assumption, stated as such in principles.md |

Numbers inside the made-up examples of kill-criterion patterns ([kill-criteria.md](kill-criteria.md#patterns-for-name-specific-criteria))
are illustrations, not settings, and are not listed.
