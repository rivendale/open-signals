"""Reference implementation of the computable rules in spec/signals.json.

The docs in docs/*.md own the meaning of every rule. This module only does the
arithmetic, so that two implementations can compare results on the same
synthetic vectors. Every function takes a dict of inputs and returns a dict of
outputs. Amounts are in one currency and one scale per call; outflows that the
docs call "positive cash outflows" are positive numbers.
"""

import datetime

# Mirrors the "thresholds" block of spec/signals.json. A test checks they agree.
THRESHOLDS = {
    "funding_dependence_max": 1.0,
    "runway_min_quarters": 4.0,
    "concentration_max_share": 0.25,
    "k3_backlog_share_min": 0.25,
    "k3_contract_cut_min": 0.25,
    "mscore_read_closely_lower": -2.22,
    "mscore_read_closely_upper": -1.78,
    "earnings_ahead_of_cash_years": 2,
    "size_ceiling_share_of_sleeve": 0.08,
    "speculative_ceiling_share_of_sleeve": 0.05,
    "entry_floor_share_of_sleeve": 0.02,
    "speculative_stressed_loss_per_dollar": 1.0,
    "drift_band_relative": 0.25,
    "wash_sale_days_each_side": 30,
    "collar_min_days_to_expiration": 1,
}

NOT_APPLICABLE = "not_applicable"
NOT_APPLIED = "not_applied"
UNLIMITED = "unlimited"
AMBIGUOUS = "ambiguous"
EPS = 1e-12  # tolerance for float equality at an inclusive boundary


def _num(inputs, key, default=None):
    value = inputs.get(key, default)
    if value is None:
        raise ValueError("missing input: %s" % key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("input %s must be a number" % key)
    return float(value)


def _outflow(inputs, key, convention):
    """Read a positive-outflow input, flipping a vendor's negative convention."""
    value = _num(inputs, key, 0.0)
    if convention == "negative":
        value = -value
    elif convention != "positive":
        raise ValueError("outflow_sign_convention must be 'positive' or 'negative'")
    if value < 0:
        raise ValueError("sign: %s must be a positive outflow after normalization" % key)
    return value


# --- Trailing twelve months -------------------------------------------------

def ttm(inputs):
    """Discrete quarters from year-to-date figures; TTM is the last four summed."""
    keys = ("ytd_3m", "ytd_6m", "ytd_9m", "ytd_12m")
    years = inputs["fiscal_years"]
    quarters = []
    for index, year in enumerate(years):
        present = [year.get(key) is not None for key in keys]
        if index < len(years) - 1 and not all(present):
            raise ValueError("fiscal year %d is not the latest and lacks a year-to-date value" % index)
        if present != sorted(present, reverse=True):
            raise ValueError("fiscal year %d has a gap in its year-to-date values" % index)
        previous = 0.0
        for key in keys[:sum(present)]:
            quarters.append(float(year[key]) - previous)
            previous = float(year[key])
    if len(quarters) < 4:
        raise ValueError("TTM needs four quarters; a quarter is never multiplied by four")
    return {"quarters": quarters, "ttm": sum(quarters[-4:])}


# --- Funding dependence and SR-1a -------------------------------------------

def funding_dependence(inputs):
    conv = inputs.get("outflow_sign_convention", "positive")
    basis = inputs.get("basis", "US_GAAP")
    ocf = _num(inputs, "operating_cash_flow")
    flp = _outflow(inputs, "finance_lease_principal_paid", conv)
    if basis == "IFRS":
        if flp:
            raise ValueError("IFRS: lease principal is moved into operating cash flow, "
                             "never deducted a second time as finance-lease principal")
        ocf -= _outflow(inputs, "ifrs_lease_principal_paid", conv)
        ocf -= _outflow(inputs, "ifrs_interest_paid_in_financing", conv)
    elif basis != "US_GAAP":
        raise ValueError("basis must be 'US_GAAP' or 'IFRS'")
    sbc = _num(inputs, "stock_based_compensation", 0.0)
    if sbc < 0:
        raise ValueError("sign: stock_based_compensation must be non-negative")
    capex = _outflow(inputs, "capital_expenditure", conv)
    repurchased = _outflow(inputs, "stock_repurchased", conv)
    issued = _num(inputs, "stock_issued", 0.0)
    if issued < 0:
        raise ValueError("sign: stock_issued must be a non-negative inflow")
    fcf = ocf - sbc - capex - flp
    burn = max(0.0, -fcf)
    net_stock = issued - repurchased
    external = net_stock + _num(inputs, "net_new_debt", 0.0)
    if burn == 0 or external <= 0:
        dependence = NOT_APPLICABLE
    else:
        dependence = external / burn
    return {
        "operating_cash_flow_normalized": ocf,
        "free_cash_flow": fcf,
        "cash_burn": burn,
        "net_stock_issued": net_stock,
        "external_funding": external,
        "funding_dependence": dependence,
    }


def _speculative(inputs):
    return inputs.get("sleeve") == "speculative"


def sr1a(inputs):
    out = funding_dependence(inputs)
    if _speculative(inputs):
        out["fires"] = NOT_APPLIED
        return out
    fd = out["funding_dependence"]
    out["fires"] = (out["free_cash_flow"] < 0 and fd != NOT_APPLICABLE
                    and fd > THRESHOLDS["funding_dependence_max"])
    return out


# --- Runway, SR-1b and K2 ---------------------------------------------------

def _capex_ttm(inputs):
    return _outflow(inputs, "capital_expenditure_ttm",
                    inputs.get("outflow_sign_convention", "positive"))


def runway(inputs):
    cash = _num(inputs, "cash_and_cash_equivalents", 0.0)
    sti = _num(inputs, "short_term_investments", 0.0)
    # restricted_cash and pledged_or_restricted_investments are read and never added.
    _num(inputs, "restricted_cash", 0.0)
    _num(inputs, "pledged_or_restricted_investments", 0.0)
    facilities = 0.0
    for f in inputs.get("facilities", []):
        if f.get("kind") == "credit_line" and f.get("committed") and f.get("conditions_met"):
            facilities += float(f["undrawn"])
    liquidity = cash + sti + facilities
    conv = inputs.get("outflow_sign_convention", "positive")
    ocf = _num(inputs, "operating_cash_flow_ttm")
    interest = _outflow(inputs, "interest_paid_in_ocf", conv)
    op_leases = _outflow(inputs, "operating_lease_payments_in_ocf", conv)
    op_burn = max(0.0, -(ocf + interest + op_leases))
    capex_ttm = _capex_ttm(inputs)
    if inputs.get("capital_expenditure_planned_next_12m") is None:
        capex = capex_ttm
    else:
        capex = _outflow(inputs, "capital_expenditure_planned_next_12m", conv)
    debt_service = _outflow(inputs, "scheduled_debt_service_next_12m", conv)
    leases = _outflow(inputs, "lease_payments_next_12m", conv)
    outflow = op_burn + capex + debt_service + leases
    quarters = UNLIMITED if outflow == 0 else 4.0 * liquidity / outflow
    return {
        "liquidity": liquidity,
        "operating_cash_burn": op_burn,
        "capital_expenditure_used": capex,
        "annual_outflow": outflow,
        "runway_quarters": quarters,
    }


def _short_runway(quarters):
    return quarters != UNLIMITED and quarters < THRESHOLDS["runway_min_quarters"]


def sr1b(inputs):
    out = runway(inputs)
    if _speculative(inputs):
        out["fires"] = NOT_APPLIED
        return out
    burns = out["operating_cash_burn"] + _capex_ttm(inputs) > 0
    out["burns_cash"] = burns
    out["fires"] = burns and _short_runway(out["runway_quarters"])
    return out


def k2(inputs):
    out = runway(inputs)
    if not inputs.get("capital_intensive_builder"):
        out["fires"] = NOT_APPLICABLE
        return out
    out["fires"] = _short_runway(out["runway_quarters"])
    return out


# --- K1 and K3 --------------------------------------------------------------

def k1(inputs):
    keys = ("going_concern", "covenant_breach", "lender_waiver_or_forbearance")
    return {"fires": any(bool(inputs.get(k)) for k in keys)}


def k3(inputs):
    backlog = inputs.get("backlog_share_at_last_filing")
    unverified = backlog is None
    share = _num(inputs, "revenue_share_at_last_filing") if unverified else float(backlog)
    event = inputs.get("event", "none")
    if event in ("termination", "default"):
        hit = True
    elif event == "contract_value_cut":
        hit = _num(inputs, "contract_value_cut_fraction") > THRESHOLDS["k3_contract_cut_min"]
    elif event == "none":
        hit = False
    else:
        raise ValueError("event must be termination, default, contract_value_cut or none")
    anchor = share > THRESHOLDS["k3_backlog_share_min"]
    return {"share_used": share, "share_unverified": unverified,
            "anchor_customer": anchor, "fires": anchor and hit}


# --- Customer concentration -------------------------------------------------

def customer_concentration(inputs):
    total_revenue = _num(inputs, "total_revenue")
    total_backlog = inputs.get("total_backlog")
    customers = inputs["customers"]
    top = max(c["revenue"] for c in customers) / total_revenue
    unverified = False
    backlog_max = 0.0
    for c in customers:
        if c.get("backlog") is None or total_backlog in (None, 0):
            unverified = True
            share = c["revenue"] / total_revenue
        else:
            share = c["backlog"] / float(total_backlog)
        backlog_max = max(backlog_max, share)
    limit = THRESHOLDS["concentration_max_share"]
    return {"top_customer_share": top, "max_backlog_share": backlog_max,
            "backlog_share_unverified": unverified,
            "flagged": top > limit or backlog_max > limit}


# --- Forensic flags ---------------------------------------------------------

def mscore(inputs):
    m = _num(inputs, "m_score")
    cutoff = _num(inputs, "cutoff")
    if not inputs.get("cutoff_source"):
        raise ValueError("an implementation records its cutoff with a source")
    lower = THRESHOLDS["mscore_read_closely_lower"]
    upper = THRESHOLDS["mscore_read_closely_upper"]
    in_band = lower < m < upper
    if any(abs(m - edge) <= EPS for edge in (cutoff, lower, upper)):
        status = "ambiguous_boundary"
    elif m > cutoff and in_band:
        status = "ambiguous_overlap"  # the cutoff lies inside or below the band
    elif m > cutoff:
        status = "flag"
    elif in_band:
        status = "read_closely"
    else:
        status = "none"
    return {"status": status}


def event_flag(inputs):
    keys = ("auditor_change_item_4_01", "non_reliance_item_4_02", "restatement")
    return {"fires": any(bool(inputs.get(k)) for k in keys), "checked": "on_receipt"}


def earnings_ahead_of_cash(inputs):
    years = inputs["years"]
    n = THRESHOLDS["earnings_ahead_of_cash_years"]
    if len(years) < n:
        raise ValueError("needs at least two fiscal years")
    ni_above = all(y["net_income"] > y["operating_cash_flow"] for y in years[-n:])
    tata = [(y["net_income_continuing_ops"] - y["operating_cash_flow"]) / y["total_assets"]
            for y in years]
    rises = [b > a for a, b in zip(tata, tata[1:])]
    one_rise = bool(rises) and rises[-1]  # reading B: rose from one year to the next
    two_rises = len(rises) >= 2 and rises[-1] and rises[-2]  # reading A
    if len(rises) < 2:
        tata_rising = AMBIGUOUS if one_rise else False
    else:
        tata_rising = two_rises if one_rise == two_rises else AMBIGUOUS
    if ni_above or tata_rising is True:
        flag = True
    elif tata_rising == AMBIGUOUS:
        flag = AMBIGUOUS
    else:
        flag = False
    return {"total_accruals_to_total_assets": tata, "net_income_above_ocf": ni_above,
            "tata_rising": tata_rising, "flag": flag}


def longer_asset_lives(inputs):
    base = _num(inputs, "carrying_amount") - _num(inputs, "residual_value", 0.0)
    old_life = _num(inputs, "old_remaining_life")
    new_life = _num(inputs, "new_remaining_life")
    if old_life <= 0 or new_life <= 0:
        raise ValueError("remaining lives must be positive")
    old_dep, new_dep = base / old_life, base / new_life
    return {"depreciable_base": base, "depreciation_old_basis": old_dep,
            "depreciation_new_basis": new_dep, "extra_pretax_profit": old_dep - new_dep,
            "flag": new_life > old_life}


# --- Collar plus income -----------------------------------------------------

def collar_price(inputs):
    call_bid, put_ask = inputs.get("call_bid"), inputs.get("put_ask")
    for quote in (call_bid, put_ask):
        # missing, zero or negative: cannot price, never free
        if isinstance(quote, bool) or not isinstance(quote, (int, float)) or quote <= 0:
            return {"status": "cannot_price"}
    days = _num(inputs, "days_to_expiration")
    out = {"net_credit": float(call_bid) - float(put_ask)}
    if days < THRESHOLDS["collar_min_days_to_expiration"]:
        out["status"] = "excluded"
        return out
    spot = _num(inputs, "spot")
    out["status"] = "priced"
    out["net_yield"] = out["net_credit"] / spot
    out["annualized_net"] = out["net_yield"] * 365.0 / days
    return out


def collar_rank(inputs):
    priced, excluded = [], []
    for c in inputs["candidates"]:
        result = collar_price(c)
        if result["status"] == "priced":
            priced.append((result["annualized_net"], c["id"]))
        else:
            excluded.append(c["id"])
    priced.sort(key=lambda p: -p[0])
    return {"order": [cid for _, cid in priced], "excluded": excluded}


# --- Sizing and limits ------------------------------------------------------

def sizing(inputs):
    speculative = _speculative(inputs)
    if speculative:
        given = inputs.get("stressed_loss_per_dollar")
        loss = THRESHOLDS["speculative_stressed_loss_per_dollar"]
        if given is not None and float(given) != loss:
            raise ValueError("speculative sleeve: stressed loss per dollar is 1.0")
    else:
        loss = _num(inputs, "stressed_loss_per_dollar")
    if loss <= 0:
        raise ValueError("stressed loss per dollar must be positive")
    bucket = inputs["bucket"]
    caps = {"bucket": bucket["budget"] - bucket["used"]}
    for name, node in inputs.get("nodes", {}).items():
        caps["node:" + name] = node["budget"] - node["used"]
    budget_size = max(0.0, min(caps.values()) / loss)
    weight = _num(inputs, "sleeve_weight")
    share = THRESHOLDS["speculative_ceiling_share_of_sleeve" if speculative
                       else "size_ceiling_share_of_sleeve"]
    candidates = {key: max(0.0, v / loss) for key, v in caps.items()}
    candidates["tier"] = _num(inputs, "tier_ceiling")
    candidates["sleeve_limit"] = share * weight
    size = min(budget_size, candidates["tier"], candidates["sleeve_limit"])
    binding = sorted(k for k, v in candidates.items() if abs(v - size) <= EPS)
    floor = THRESHOLDS["entry_floor_share_of_sleeve"] * weight
    status = "sized"
    if inputs.get("is_entry", True) and size < floor - EPS:
        status, size = "not_bought", 0.0
    return {"budget_size": budget_size, "size": size, "binding": binding,
            "entry_floor": floor, "status": status}


def drift_band(inputs):
    if inputs.get("account_type") == "taxable":
        return {"rebalance": NOT_APPLIED}
    if inputs.get("account_type") != "retirement":
        raise ValueError("account_type must be 'retirement' or 'taxable'")
    target, weight = _num(inputs, "target_weight"), _num(inputs, "weight")
    if target <= 0:
        raise ValueError("drift is relative to a positive target")
    band = THRESHOLDS["drift_band_relative"] * target
    return {"lower": target - band, "upper": target + band,
            "rebalance": abs(weight - target) > band + EPS}


# --- Wash-sale window -------------------------------------------------------

def wash_sale(inputs):
    sale = datetime.date.fromisoformat(inputs["sale_date"])
    days = datetime.timedelta(days=THRESHOLDS["wash_sale_days_each_side"])
    start, end = sale - days, sale + days
    out = {"window_start": start.isoformat(), "window_end": end.isoformat(),
           "window_days": (end - start).days + 1, "triggering": [], "needs_review": []}
    if not inputs.get("is_loss"):
        out["wash_sale"] = NOT_APPLICABLE
        return out
    kinds = ("purchase", "dividend_reinvestment", "bought_call")
    for a in inputs.get("acquisitions", []):
        if a.get("kind") not in kinds + ("sold_put_deep_itm",):
            raise ValueError("unknown acquisition kind: %s" % a.get("kind"))
        if a.get("owner") not in ("self", "spouse"):
            raise ValueError("acquirer must be 'self' or 'spouse'; others are not covered")
        when = datetime.date.fromisoformat(a["date"])
        if not (start <= when <= end) or not a.get("substantially_identical"):
            continue
        if a["kind"] in kinds:
            out["triggering"].append(a["id"])
        else:
            out["needs_review"].append(a["id"])
    out["wash_sale"] = bool(out["triggering"])
    return out


# Rule ID -> implementation. Every rule ID in spec/signals.json appears here.
RULES = {
    "ttm": ttm,
    "signal.funding_dependence": funding_dependence,
    "SR-1a": sr1a,
    "signal.runway": runway,
    "SR-1b": sr1b,
    "K1": k1,
    "K2": k2,
    "K3": k3,
    "signal.customer_concentration": customer_concentration,
    "flag.mscore": mscore,
    "flag.event": event_flag,
    "flag.earnings_ahead_of_cash": earnings_ahead_of_cash,
    "flag.longer_asset_lives": longer_asset_lives,
    "collar.price": collar_price,
    "collar.rank": collar_rank,
    "sizing.precedence": sizing,
    "limits.drift_band": drift_band,
    "tax.wash_sale_window": wash_sale,
}
