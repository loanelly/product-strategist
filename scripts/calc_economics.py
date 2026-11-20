#!/usr/bin/env python3
"""Calculate basic unit economics from explicitly unit-tagged JSON input."""

from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from pathlib import Path
from typing import Any

CURRENCY = re.compile(r"^[A-Z]{3}$")


class InputError(ValueError):
    """Raised when the input is missing data or uses incompatible units."""


def number(value: Any, field: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise InputError(f"{field} must be a number")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise InputError(f"{field} must be a valid number") from exc
    if not result.is_finite():
        raise InputError(f"{field} must be finite")
    return result


def object_field(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise InputError(f"Missing or invalid object: {key}")
    return value


def calculate(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("mode") == "plan_year_profit_threshold":
        return calculate_plan_year_threshold(data)

    if data.get("period") != "month":
        raise InputError("period must be 'month'; all formulas use monthly units")

    arpu = object_field(data, "arpu")
    margin = object_field(data, "gross_margin")
    retention = object_field(data, "retention")
    spend = object_field(data, "acquisition_spend")
    customers = object_field(data, "new_customers")

    currency = data.get("currency")
    if not isinstance(currency, str) or not CURRENCY.fullmatch(currency):
        raise InputError("currency must be a three-letter uppercase currency code")
    if arpu.get("currency") != currency or spend.get("currency") != currency:
        raise InputError("ARPU, acquisition spend, and top-level currency must match")
    if arpu.get("period") != "month" or retention.get("period") != "month":
        raise InputError("ARPU and retention periods must both be 'month'")
    if margin.get("unit") != "ratio" or retention.get("unit") != "ratio":
        raise InputError("gross_margin and retention units must be 'ratio' (0 to 1)")
    if customers.get("unit") != "customers":
        raise InputError("new_customers unit must be 'customers'")

    arpu_value = number(arpu.get("value"), "arpu.value")
    margin_value = number(margin.get("value"), "gross_margin.value")
    retention_value = number(retention.get("value"), "retention.value")
    spend_value = number(spend.get("value"), "acquisition_spend.value")
    customer_count = number(customers.get("value"), "new_customers.value")
    if arpu_value <= 0:
        raise InputError("arpu.value must be greater than zero")
    if not Decimal(0) <= margin_value <= Decimal(1):
        raise InputError("gross_margin.value must be between 0 and 1")
    if not Decimal(0) <= retention_value < Decimal(1):
        raise InputError("retention.value must be between 0 and 1 (1 makes LTV undefined)")
    if spend_value < 0:
        raise InputError("acquisition_spend.value cannot be negative")
    if customer_count <= 0 or customer_count != customer_count.to_integral_value():
        raise InputError("new_customers.value must be a positive whole number")

    contribution = arpu_value * margin_value
    if contribution <= 0:
        raise InputError("Gross contribution per month must be greater than zero")
    cac = spend_value / customer_count
    ltv = contribution / (Decimal(1) - retention_value)
    payback = cac / contribution
    return {
        "currency": currency,
        "period": "month",
        "retention_rate": float(retention_value),
        "gross_margin_ratio": float(margin_value),
        "ltv": round(float(ltv), 6),
        "cac": round(float(cac), 6),
        "payback_months": round(float(payback), 6),
        "formulas": {
            "ltv": "monthly_arpu * gross_margin / (1 - monthly_retention)",
            "cac": "acquisition_spend / new_customers",
            "payback_months": "cac / (monthly_arpu * gross_margin)",
        },
        "assumptions": [
            "Monthly retention is a constant cohort survival rate.",
            "LTV is undiscounted and excludes costs beyond gross margin.",
            "CAC uses the supplied acquisition spend and acquired-customer count.",
        ],
    }


def calculate_plan_year_threshold(data: dict[str, Any]) -> dict[str, Any]:
    currency = data.get("currency")
    if not isinstance(currency, str) or not CURRENCY.fullmatch(currency):
        raise InputError("currency must be a three-letter uppercase currency code")

    def annual_amount(field: str) -> Decimal:
        value = object_field(data, field)
        if value.get("currency") != currency or value.get("period") != "year":
            raise InputError(f"{field} currency and period must match the plan year")
        amount = number(value.get("value"), f"{field}.value")
        if amount < 0:
            raise InputError(f"{field}.value cannot be negative")
        return amount

    baseline = annual_amount("baseline_gross_profit")
    target = annual_amount("target_gross_profit")
    contribution = object_field(data, "incremental_paid_month_contribution")
    if contribution.get("currency") != currency:
        raise InputError("incremental contribution currency must match")
    if contribution.get("unit") != "gross_profit_per_paid_month":
        raise InputError(
            "incremental contribution unit must be 'gross_profit_per_paid_month'"
        )
    contribution_value = number(contribution.get("value"), "incremental contribution.value")
    if contribution_value <= 0:
        raise InputError("incremental contribution.value must be greater than zero")

    gap = max(Decimal(0), target - baseline)
    paid_months = (gap / contribution_value).to_integral_value(rounding=ROUND_CEILING)
    return {
        "mode": "plan_year_profit_threshold",
        "currency": currency,
        "period": "year",
        "baseline_gross_profit": float(baseline),
        "target_gross_profit": float(target),
        "gross_profit_gap": float(gap),
        "gross_profit_per_incremental_paid_month": float(contribution_value),
        "minimum_incremental_paid_months_before_new_direct_costs": int(paid_months),
        "threshold_formula": (
            "ceil((target_gross_profit - baseline_gross_profit + "
            "incremental_direct_costs) / gross_profit_per_incremental_paid_month)"
        ),
        "limitations": [
            "This is a break-even threshold, not a forecast.",
            "New direct costs are not supplied and must be added to the numerator.",
            "Paid-month increments must be measured against the unchanged-service baseline.",
            "No LTV, CAC, retention, development-cost payback, or cannibalization is inferred.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="Input JSON file; defaults to stdin")
    args = parser.parse_args()
    try:
        raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise InputError("Input must be a JSON object")
        result = calculate(data)
    except OSError as exc:
        print(f"ERROR: Cannot read input: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
