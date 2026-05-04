from __future__ import annotations

from dataclasses import dataclass
from datetime import date


MONTH_NAMES = [
    "Ocak",
    "Şubat",
    "Mart",
    "Nisan",
    "Mayıs",
    "Haziran",
    "Temmuz",
    "Ağustos",
    "Eylül",
    "Ekim",
    "Kasım",
    "Aralık",
]

QUARTERS = [
    (1, "1. Dönem", [1, 2, 3], "Ocak - Şubat - Mart"),
    (2, "2. Dönem", [4, 5, 6], "Nisan - Mayıs - Haziran"),
    (3, "3. Dönem", [7, 8, 9], "Temmuz - Ağustos - Eylül"),
    (4, "4. Dönem", [10, 11, 12], "Ekim - Kasım - Aralık"),
]

# 2026 yılı ücret dışı gelirler için gelir vergisi tarifesi.
# Şahıs şirketi / ticari kazanç tahmini için kullanılır.
# Her yıl değişebileceği için sonraki pakette ayarlar ekranından düzenlenebilir hale getirilebilir.
INCOME_TAX_BRACKETS_2026_NON_WAGE = [
    (190_000.00, 0.15),
    (400_000.00, 0.20),
    (1_000_000.00, 0.27),
    (5_300_000.00, 0.35),
    (None, 0.40),
]


@dataclass(frozen=True)
class IncomeTaxResult:
    taxable_income: float
    tax: float
    effective_rate: float
    bracket_label: str


def current_year() -> int:
    return date.today().year


def month_name(month: int) -> str:
    try:
        return MONTH_NAMES[int(month) - 1]
    except Exception:
        return str(month)


def quarter_for_month(month: int) -> int:
    month = int(month)
    if month <= 3:
        return 1
    if month <= 6:
        return 2
    if month <= 9:
        return 3
    return 4


def income_tax_2026_non_wage(income: float) -> IncomeTaxResult:
    income = max(float(income or 0), 0.0)
    if income <= 0:
        return IncomeTaxResult(0.0, 0.0, 0.0, "Kâr yok")

    remaining = income
    previous_limit = 0.0
    total_tax = 0.0
    active_rate = 0.15

    for limit, rate in INCOME_TAX_BRACKETS_2026_NON_WAGE:
        active_rate = rate
        if limit is None:
            taxable_part = max(remaining, 0.0)
        else:
            taxable_part = max(min(income, limit) - previous_limit, 0.0)

        if taxable_part > 0:
            total_tax += taxable_part * rate
            remaining -= taxable_part

        if limit is None or income <= limit:
            break
        previous_limit = limit

    effective = (total_tax / income * 100) if income else 0.0
    return IncomeTaxResult(
        taxable_income=round(income, 2),
        tax=round(total_tax, 2),
        effective_rate=round(effective, 2),
        bracket_label=f"%{int(active_rate * 100)} dilimi",
    )


def kdv_result_label(amount: float) -> str:
    amount = float(amount or 0)
    if amount > 0:
        return "Ödenecek KDV"
    if amount < 0:
        return "Devreden KDV"
    return "KDV Yok"
