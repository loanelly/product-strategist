#!/usr/bin/env python3
"""Calculate basic unit economics from explicitly unit-tagged JSON input."""

from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation
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
