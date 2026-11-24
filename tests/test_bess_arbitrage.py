import unittest
from bess_arbitrage.engine import MarketElectricityPriceSlot, BESSArbitrageDispatchEngine

class TestBESSArbitrageDispatchEngine(unittest.TestCase):
    def setUp(self):
        self.bess = BESSArbitrageDispatchEngine(battery_rated_capacity_kwh=10000.0) # 10 MWh BESS

    def test_profitable_arbitrage_trade(self):
        # Charge during afternoon solar depression (₹2.20), discharge during evening peak (₹8.50)
        c_slot = MarketElectricityPriceSlot("13:00-13:15", 2.20)
        d_slot = MarketElectricityPriceSlot("19:30-19:45", 8.50)
        res = self.bess.evaluate_arbitrage_opportunity(c_slot, d_slot, round_trip_efficiency_pct=88.0)
        self.assertTrue(res["is_dispatch_recommended"])
        self.assertGreater(res["projected_cycle_profit_inr"], 40000.0)

if __name__ == "__main__":
    unittest.main()
