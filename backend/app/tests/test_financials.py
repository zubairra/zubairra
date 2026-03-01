from app.services.financials import calculate_net_pnl, calculate_taxes


def test_calculate_taxes_eq():
    result = calculate_taxes("EQ", 100000)
    assert result["brokerage"] > 0
    assert result["stt"] > 0


def test_calculate_net_pnl():
    charges = {"brokerage": 10, "stt": 8, "exchange_charges": 4, "gst": 2.5}
    pnl = calculate_net_pnl(1000, 1300, charges)
    assert pnl == 275.5
