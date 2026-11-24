# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

import unittest
from bess_arbitrage.controllers.base_controller import EnterpriseBaseController
from bess_arbitrage.controllers.workflow_handler import WorkflowStateMachine
from bess_arbitrage.services.integration_service import EnterpriseIntegrationService
from bess_arbitrage.services.validator import EnterpriseValidationEngine
from bess_arbitrage.tasks import hourly_sync, daily_reconciliation, weekly_digest
from bess_arbitrage import api
from bess_arbitrage.bess_arbitrage.doctype.bess_arbitrage_entry.bess_arbitrage_entry import BatteryEnergyStorageBessArbitrageEntry
from bess_arbitrage.bess_arbitrage.doctype.bess_arbitrage_item.bess_arbitrage_item import BatteryEnergyStorageBessArbitrageItem
from bess_arbitrage.bess_arbitrage.doctype.bess_arbitrage_settings.bess_arbitrage_settings import BatteryEnergyStorageBessArbitrageSettings
from bess_arbitrage.bess_arbitrage.doctype.bess_arbitrage_audit_log.bess_arbitrage_audit_log import BatteryEnergyStorageBessArbitrageAuditLog
from bess_arbitrage.bess_arbitrage.report.bess_arbitrage_summary.bess_arbitrage_summary import execute as run_report

class TestEnterpriseArchitecture(unittest.TestCase):
    def setUp(self):
        self.entry = BatteryEnergyStorageBessArbitrageEntry()
        self.entry.title = "Test Erpnext Battery Energy Storage Bess Arbitrage"
        self.entry.party = "Alpha Enterprise Corp"
        self.entry.status = "Draft"

        item1 = BatteryEnergyStorageBessArbitrageItem()
        item1.item_code = "ITEM-001"
        item1.qty = 10.0
        item1.rate = 1500.0
        item1.validate()

        item2 = BatteryEnergyStorageBessArbitrageItem()
        item2.item_code = "ITEM-002"
        item2.qty = 5.0
        item2.rate = 2000.0
        item2.validate()

        self.entry.items = [item1, item2]

    def test_multi_doctype_aggregation(self):
        self.entry.validate()
        self.assertEqual(self.entry.total_qty, 15.0)
        self.assertEqual(self.entry.total_amount, 25000.0)
        self.assertEqual(self.entry.grand_total, 25000.0)

    def test_submission_and_cancellation_lifecycle(self):
        self.entry.validate()
        self.entry.on_submit()
        self.assertEqual(self.entry.status, "Submitted")
        self.assertEqual(self.entry.audit_status, "Compliant")

        self.entry.on_cancel()
        self.assertEqual(self.entry.status, "Cancelled")
        self.assertEqual(self.entry.audit_status, "Flagged")

    def test_workflow_state_machine(self):
        self.assertTrue(WorkflowStateMachine.apply_transition(self.entry, "Pending Review"))
        self.assertEqual(self.entry.status, "Pending Review")
        self.assertTrue(WorkflowStateMachine.apply_transition(self.entry, "Approved"))
        self.assertEqual(self.entry.status, "Approved")

    def test_settings_single_doctype(self):
        settings = BatteryEnergyStorageBessArbitrageSettings()
        settings.batch_size = 500
        settings.validate()
        res = settings.test_connection()
        self.assertEqual(res["status"], "success")

    def test_tamper_proof_audit_log(self):
        audit = BatteryEnergyStorageBessArbitrageAuditLog()
        audit.reference_doctype = "Erpnext Battery Energy Storage Bess Arbitrage Entry"
        audit.reference_name = "TEST-REF-001"
        audit.action = "Submitted"
        audit.before_insert()
        self.assertIsNotNone(audit.checksum_hash)
        self.assertEqual(len(audit.checksum_hash), 64)

    def test_script_report_execution(self):
        columns, data, message, chart, summary = run_report()
        self.assertTrue(len(columns) >= 5)
        self.assertTrue(len(data) >= 1)
        self.assertIsNotNone(chart)
        self.assertTrue(len(summary) >= 2)

    def test_api_endpoints(self):
        ping_res = api.ping()
        self.assertEqual(ping_res["status"], "ok")

        overview = api.get_status_overview()
        self.assertEqual(overview["operational_status"], "ONLINE")
        self.assertEqual(len(overview["doctypes"]), 4)

    def test_scheduler_background_tasks(self):
        self.assertEqual(hourly_sync()["status"], "COMPLETED")
        self.assertEqual(daily_reconciliation()["status"], "VERIFIED_100_PERCENT")
        self.assertEqual(weekly_digest()["status"], "DISPATCHED")

if __name__ == "__main__":
    unittest.main()
