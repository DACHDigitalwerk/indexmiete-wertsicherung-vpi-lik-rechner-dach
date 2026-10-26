"""Rechtsstand 2026: Indexmiete (? 557b BGB), Gewerbemiet-Wertsicherung (PrKG), AT VPI (5 % Schwelle) & CH LIK (Art. 269b OR)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class IndexRentInput:
    mode: str = "DE_WOHN"  # "DE_WOHN", "DE_GEW", "AT_VPI", "CH_LIK"
    current_net_rent: float = 1_450.0
    index_old: float = 114.2
    index_new: float = 121.6
    months_since_last_adjustment: int = 16
    threshold_type: str = "NONE"  # "NONE", "PCT", "PTS"
    threshold_value: float = 0.0
    pass_through_pct: float = 100.0


@dataclass(frozen=True)
class IndexRentResult:
    mode: str
    delta_index_points: float
    delta_index_pct: float
    effective_rent_increase_pct: float
    new_net_rent: float
    monthly_increase: float
    annual_increase: float
    waiting_period_met: bool
    threshold_met: bool
    adjustment_triggered: bool


def calculate_index_rent(inp: IndexRentInput) -> IndexRentResult:
    m = inp.mode.upper().strip()
    if m not in ("DE_WOHN", "DE_GEW", "AT_VPI", "CH_LIK"):
        raise ValueError(f"Unsupported mode: {m}")
    if inp.current_net_rent <= 0 or inp.index_old <= 0 or inp.index_new <= 0 or not (0 < inp.pass_through_pct <= 100.0):
        raise ValueError("Invalid numeric parameters for IndexRentInput")

    delta_pts = inp.index_new - inp.index_old
    delta_pct = ((inp.index_new / inp.index_old) - 1.0) * 100.0

    t_type = inp.threshold_type.upper().strip()
    if t_type == "PCT":
        thresh_met = abs(delta_pct) + 1e-9 >= inp.threshold_value
    elif t_type == "PTS":
        thresh_met = abs(delta_pts) + 1e-9 >= inp.threshold_value
    else:
        thresh_met = True

    wait_met = (inp.months_since_last_adjustment >= 12) if m == "DE_WOHN" else True
    triggered = thresh_met and wait_met and (delta_pct > 0)

    eff_pct = (delta_pct * (inp.pass_through_pct / 100.0)) if triggered else 0.0
    new_rent = round(inp.current_net_rent * (1.0 + eff_pct / 100.0), 2)
    diff_m = round(new_rent - inp.current_net_rent, 2)
    diff_y = round(diff_m * 12.0, 2)

    return IndexRentResult(
        mode=m,
        delta_index_points=round(delta_pts, 4),
        delta_index_pct=round(delta_pct, 4),
        effective_rent_increase_pct=round(eff_pct, 4),
        new_net_rent=new_rent,
        monthly_increase=diff_m,
        annual_increase=diff_y,
        waiting_period_met=wait_met,
        threshold_met=thresh_met,
        adjustment_triggered=triggered,
    )
