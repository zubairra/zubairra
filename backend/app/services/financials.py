def calculate_taxes(segment: str, turnover: float) -> dict[str, float]:
    segment = segment.upper()
    if segment == "EQ":
        brokerage_rate, stt_rate, exch_rate = 0.0003, 0.001, 0.0000325
    else:  # F&O
        brokerage_rate, stt_rate, exch_rate = 0.0005, 0.000625, 0.00005

    brokerage = turnover * brokerage_rate
    stt = turnover * stt_rate
    exchange_charges = turnover * exch_rate
    gst = 0.18 * (brokerage + exchange_charges)

    return {
        "brokerage": round(brokerage, 2),
        "stt": round(stt, 2),
        "exchange_charges": round(exchange_charges, 2),
        "gst": round(gst, 2),
    }


def calculate_net_pnl(buy_value: float, sell_value: float, charges: dict[str, float]) -> float:
    total_charges = charges["brokerage"] + charges["stt"] + charges["exchange_charges"] + charges["gst"]
    return round((sell_value - buy_value) - total_charges, 2)
