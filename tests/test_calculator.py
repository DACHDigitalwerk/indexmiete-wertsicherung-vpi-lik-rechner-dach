import pytest
from indexmiete_dach import IndexRentInput, calculate_index_rent

def test_de_wohn_557b_triggered():
    res = calculate_index_rent(IndexRentInput(mode="DE_WOHN", current_net_rent=1000.0, index_old=110.0, index_new=115.5, months_since_last_adjustment=14))
    assert res.adjustment_triggered is True
    assert abs(res.delta_index_pct - 5.0) < 1e-4
    assert res.new_net_rent == 1050.0

def test_de_wohn_blocked_under_12_months():
    res = calculate_index_rent(IndexRentInput(mode="DE_WOHN", current_net_rent=1000.0, index_old=110.0, index_new=120.0, months_since_last_adjustment=10))
    assert res.waiting_period_met is False
    assert res.adjustment_triggered is False
    assert res.new_net_rent == 1000.0

def test_de_gewerbe_pct_threshold_and_passthrough():
    res = calculate_index_rent(IndexRentInput(mode="DE_GEW", current_net_rent=2000.0, index_old=100.0, index_new=110.0, threshold_type="PCT", threshold_value=10.0, pass_through_pct=80.0))
    assert res.adjustment_triggered is True
    assert abs(res.effective_rent_increase_pct - 8.0) < 1e-4
    assert res.new_net_rent == 2160.0

def test_de_gewerbe_points_threshold_not_met():
    res = calculate_index_rent(IndexRentInput(mode="DE_GEW", current_net_rent=2000.0, index_old=110.0, index_new=114.2, threshold_type="PTS", threshold_value=5.0))
    assert res.threshold_met is False
    assert res.adjustment_triggered is False

def test_de_gewerbe_points_threshold_met():
    res = calculate_index_rent(IndexRentInput(mode="DE_GEW", current_net_rent=2000.0, index_old=110.0, index_new=115.5, threshold_type="PTS", threshold_value=5.0))
    assert res.threshold_met is True
    assert res.adjustment_triggered is True

def test_at_vpi_5_pct_threshold_met():
    res = calculate_index_rent(IndexRentInput(mode="AT_VPI", current_net_rent=1200.0, index_old=100.0, index_new=105.2, threshold_type="PCT", threshold_value=5.0))
    assert res.adjustment_triggered is True
    assert res.new_net_rent == 1262.4

def test_at_vpi_5_pct_threshold_missed():
    res = calculate_index_rent(IndexRentInput(mode="AT_VPI", current_net_rent=1200.0, index_old=100.0, index_new=104.8, threshold_type="PCT", threshold_value=5.0))
    assert res.adjustment_triggered is False
    assert res.monthly_increase == 0.0

def test_ch_lik_adjustment():
    res = calculate_index_rent(IndexRentInput(mode="CH_LIK", current_net_rent=3000.0, index_old=100.0, index_new=103.5))
    assert res.adjustment_triggered is True
    assert res.new_net_rent == 3105.0

def test_invalid_mode_raises():
    with pytest.raises(ValueError):
        calculate_index_rent(IndexRentInput(mode="INVALID"))

def test_invalid_rent_raises():
    with pytest.raises(ValueError):
        calculate_index_rent(IndexRentInput(current_net_rent=-100.0))
