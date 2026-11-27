import argparse
import hashlib
import json
import os
import sys
from typing import Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solar_shift_router.dispatcher import dispatch_shift_command
from merkle_handover_ledger.verifier import seal_handover_attestation

def compile_warm_handover(
    outgoing_pod: str,
    incoming_pod: str,
    utc_hour: int,
    utc_minute: int,
    ledger_output: str = "evidence/merkle-receipts/latest_handover_proof.json"
) -> Dict:
    dispatch = dispatch_shift_command(utc_hour, utc_minute, "commercial-global")
    fido2_sig = "fido2-" + hashlib.sha256(f"{outgoing_pod}->{incoming_pod}@{utc_hour}:{utc_minute}".encode("utf-8")).hexdigest()[:24]

    incident_snapshot = [
        {
            "incident_id": "INC-2026-8841",
            "severity": "SEV-2",
            "service": "global-fx-settlement-bus",
            "executed_runbook_steps": ["STEP-1-DRAIN-STALE-CONSUMER", "STEP-2-VERIFY-REPLICA-LAG"],
            "next_action": "Monitor Kafka consumer lag for 15m; close if < 200ms",
            "eu_pii_redacted_at_edge": True
        }
    ]

    manifest = {
        "outgoing_pod": outgoing_pod,
        "incoming_pod": incoming_pod,
        "handover_window_utc": f"{utc_hour:02d}:{utc_minute:02d} UTC",
        "warm_overlap_verified": dispatch["warm_handover_overlap"],
        "incoming_lead_fido2_signature": fido2_sig,
        "active_incidents_transferred": incident_snapshot,
        "attestation_leaves": [
            {"outgoing": outgoing_pod, "incoming": incoming_pod, "fido2_sig": fido2_sig},
            {"incident_count": len(incident_snapshot), "incidents": incident_snapshot}
        ]
    }

    sealed = seal_handover_attestation(manifest)
    if ledger_output:
        os.makedirs(os.path.dirname(ledger_output), exist_ok=True)
        with open(ledger_output, "w", encoding="utf-8") as f:
            json.dump(sealed, f, indent=2)

    return sealed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Follow-the-Sun Warm Handover State Compiler")
    parser.add_argument("--outgoing-pod", default="AMER")
    parser.add_argument("--incoming-pod", default="APAC")
    parser.add_argument("--utc-hour", type=int, default=20)
    parser.add_argument("--utc-minute", type=int, default=30)
    args = parser.parse_args()
    res = compile_warm_handover(args.outgoing_pod, args.incoming_pod, args.utc_hour, args.utc_minute)
    print(json.dumps(res["handover_record"], indent=2))
    print("Merkle Root:", res["merkle_root_sha256"])
