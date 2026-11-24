# ERPNext Grid-Scale BESS Energy Storage & Power Exchange Arbitrage Engine

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![IEX Power Trading](https://img.shields.io/badge/IEX-DAM%20%2F%20RTM%20Trading-gold.svg)]()
[![Energy Storage](https://img.shields.io/badge/BESS-Arbitrage%20Engine-teal.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

With the deployment of utility-scale **Battery Energy Storage Systems (BESS - 10MW to 500MW)** connected to high-voltage grid substations:
1. **Volatile Power Exchange Tariffs:** Power clearing prices on the Indian Energy Exchange (IEX) fluctuate between ₹1.80/kWh during midday solar peaks and ₹10.00/kWh during evening peak demand.
2. **Cycle Life Degradation Cost:** Charging and discharging lithium iron phosphate (LFP) batteries degrades cell capacity (typically costing ₹1.00–₹1.50/kWh in degradation amortized cost); dispatching when price spreads are narrow destroys asset value.
3. **Manual Trading Disconnect:** Power scheduling teams lack an automated engine that ingests Day-Ahead Market (DAM) / Real-Time Market (RTM) clearing prices and schedules optimal charge/discharge blocks.

This Frappe application acts as an intelligent BESS Merchant Dispatch & Power Arbitrage Controller.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["IEX DAM / RTM Power Price Feeds (15-Min Blocks)"] -->|Ingest Market Clearing Prices| B["Arbitrage Opportunity Analyzer"]
    C["BESS Telemetry (Current SoC & Degradation Cost)"] --> B
    B -->|Calculate Price Spread vs Battery Efficiency (88%)| D{"Net Spread > Degradation Cost Hurdle?"}
    D -->|Yes (Economically Profitable)| E["Generate Dispatch Schedule: Charge Afternoon / Discharge Peak"]
    D -->|No (Spread Too Narrow)| F["Hold Battery: Standby Preservation Mode"]
    E -->|Execute Trades on Power Exchange| G["Automated Power Sales Invoicing & Ledger Settlement"]
```

---

## 🚀 Key Engineering Capabilities

- **15-Minute Time Block Arbitrage:** Models Day-Ahead Market (DAM) and Real-Time Market (RTM) price spreads.
- **Degradation Cost Safeguard:** Protects battery warranty by enforcing hurdle rates before recommending dispatch.
- **Round-Trip Efficiency Adjustment:** Automatically calculates real-world round-trip losses (AC-to-AC ~88%).
- **Settlement & Trading P&L Ledger:** Tracks daily merchant arbitrage revenue against battery degradation write-offs.

---

## 📂 Frappe DocType Schema & Data Structure

```text
bess_arbitrage/
├── bess_arbitrage_core/
│   ├── doctype/
│   │   ├── bess_power_slot/
│   │   │   ├── bess_power_slot.json
│   │   │   ├── bess_power_slot.py
│   │   │   └── bess_power_slot.js
│   │   └── bess_arbitrage_trade/
│   │       └── bess_arbitrage_trade.json
│   └── workspace/
│       └── bess_arbitrage_workspace/
│           └── bess_arbitrage_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/bess_arbitrage.api.evaluate_arbitrage_opportunity`
- **Whitelisted Method:** `@frappe.whitelist() def generate_dispatch_schedule()`
- **Hooks Event:** `scheduler_events.cron(*/15 * * * *)` runs 15-minute time-block price evaluations.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/erpnext-battery-energy-storage-bess-arbitrage
bench --site erp.yourdomain.com install-app bess_arbitrage
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Optimized for Renewable IPPs, Battery Storage Developers, and Power Trading Desks.
