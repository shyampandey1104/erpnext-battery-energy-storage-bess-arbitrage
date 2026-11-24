"""Grid-Scale Battery Energy Storage System (BESS) Power Arbitrage & Dispatch Engine."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class MarketElectricityPriceSlot:
    time_block: str            # e.g., "12:00-12:15"
    market_clearing_price_inr_per_kwh: float # e.g., 2.50 during solar peak, 9.80 during evening peak

class BESSArbitrageDispatchEngine:
    def __init__(self, battery_rated_capacity_kwh: float, max_cycles_per_day: float = 1.5):
        self.capacity_kwh = battery_rated_capacity_kwh
        self.max_cycles = max_cycles_per_day
        self.current_soc_kwh = 0.0
        self.arbitrage_trades: List[Dict[str, Any]] = []

    def evaluate_arbitrage_opportunity(self, charge_slot: MarketElectricityPriceSlot, discharge_slot: MarketElectricityPriceSlot, round_trip_efficiency_pct: float = 88.0) -> Dict[str, Any]:
        cost_to_charge_per_kwh = charge_slot.market_clearing_price_inr_per_kwh
        revenue_per_kwh = discharge_slot.market_clearing_price_inr_per_kwh * (round_trip_efficiency_pct / 100.0)
        spread_per_kwh = round(revenue_per_kwh - cost_to_charge_per_kwh, 3)

        # Minimum economic spread after cycle degradation cost (~1.20 INR/kWh)
        is_viable = spread_per_kwh > 1.20
        gross_profit_per_cycle = round(spread_per_kwh * self.capacity_kwh, 2) if is_viable else 0.0

        trade = {
            "charge_block": charge_slot.time_block,
            "charge_price": cost_to_charge_per_kwh,
            "discharge_block": discharge_slot.time_block,
            "discharge_price": discharge_slot.market_clearing_price_inr_per_kwh,
            "net_spread_per_kwh": spread_per_kwh,
            "is_dispatch_recommended": is_viable,
            "projected_cycle_profit_inr": gross_profit_per_cycle
        }
        self.arbitrage_trades.append(trade)
        return trade
