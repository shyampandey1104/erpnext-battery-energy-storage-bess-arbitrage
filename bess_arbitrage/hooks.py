# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "bess_arbitrage"
app_title = "Erpnext Battery Energy Storage Bess Arbitrage"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Battery Energy Storage Bess Arbitrage - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/bess_arbitrage/css/bess_arbitrage.bundle.css"
app_include_js = "/assets/bess_arbitrage/js/bess_arbitrage.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Battery Energy Storage Bess Arbitrage Entry": {
        "validate": "bess_arbitrage.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "bess_arbitrage.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "bess_arbitrage.tasks.hourly_sync"
    ],
    "daily": [
        "bess_arbitrage.tasks.daily_reconciliation"
    ],
    "weekly": [
        "bess_arbitrage.tasks.weekly_digest"
    ]
}
