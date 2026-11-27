import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from solar_shift_router.dispatcher import dispatch_shift_command
from handover_state_compiler.compiler import compile_warm_handover
from merkle_handover_ledger.verifier import verify_handover_ledger

class TestFollowTheSunOperatingModel(unittest.TestCase):
    def test_solar_utc_routing_across_three_daylight_pods(self):
        amer = dispatch_shift_command(15, 0, "commercial-global")
        self.assertEqual(amer["active_command_pod"], "AMER-NEW-YORK")
        self.assertEqual(amer["jit_custody_state"]["APAC-SINGAPORE"], "READ_ONLY_OBSERVABILITY (SLEEP_PROTECTED)")

        apac = dispatch_shift_command(2, 30, "commercial-global")
        self.assertEqual(apac["active_command_pod"], "APAC-SINGAPORE")

        emea = dispatch_shift_command(9, 15, "commercial-global")
        self.assertEqual(emea["active_command_pod"], "EMEA-FRANKFURT")

    def test_thirty_minute_warm_handover_overlap_detection(self):
        overlap = dispatch_shift_command(20, 45, "commercial-global")
        self.assertTrue(overlap["warm_handover_overlap"])
        self.assertEqual(overlap["next_incoming_pod"], "APAC-SINGAPORE")

    def test_sovereign_fedramp_workload_fenced_to_conus_during_apac_hours(self):
        sovereign = dispatch_shift_command(2, 30, "fedramp-high-us")
        self.assertEqual(sovereign["active_command_pod"], "AMER-SOVEREIGN-CONUS")
        self.assertTrue(sovereign["sovereignty_decision"]["sovereign_override_applied"])

    def test_warm_handover_compiler_and_merkle_proof_verification(self):
        ledger_path = os.path.join(os.path.dirname(__file__), "../../evidence/merkle-receipts/latest_handover_proof.json")
        res = compile_warm_handover("AMER", "APAC", 20, 30, ledger_output=ledger_path)
        self.assertTrue(res["handover_record"]["warm_overlap_verified"])
        self.assertTrue(verify_handover_ledger(ledger_path))

if __name__ == "__main__":
    unittest.main()
