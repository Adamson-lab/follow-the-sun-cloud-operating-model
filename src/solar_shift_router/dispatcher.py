import argparse
import json
import os
import sys
from typing import Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sovereign_jurisdiction_fence.fence import enforce_sovereign_routing
from jit_shift_authority_broker.custody import compute_shift_jit_custody

def resolve_solar_pod(utc_hour: int, utc_minute: int) -> Dict:
    """Determines active daylight command pod and whether the 30-minute warm handover overlap is active."""
    total_mins = (utc_hour % 24) * 60 + (utc_minute % 60)

    # 13:00 - 21:00 UTC (780 - 1260): AMER Daylight (Overlap 20:30 - 21:00 = 1230 - 1260)
    if 780 <= total_mins < 1260:
        return {
            "solar_pod": "AMER-NEW-YORK",
            "warm_handover_active": total_mins >= 1230,
            "incoming_pod": "APAC-SINGAPORE" if total_mins >= 1230 else None
        }
    # 05:00 - 13:00 UTC (300 - 780): EMEA Daylight (Overlap 12:30 - 13:00 = 750 - 780)
    if 300 <= total_mins < 780:
        return {
            "solar_pod": "EMEA-FRANKFURT",
            "warm_handover_active": total_mins >= 750,
            "incoming_pod": "AMER-NEW-YORK" if total_mins >= 750 else None
        }
    # 21:00 - 05:00 UTC (1260..1440 or 0..300): APAC Daylight (Overlap 04:30 - 05:00 = 270 - 300)
    return {
        "solar_pod": "APAC-SINGAPORE",
        "warm_handover_active": 270 <= total_mins < 300,
        "incoming_pod": "EMEA-FRANKFURT" if 270 <= total_mins < 300 else None
    }

def dispatch_shift_command(utc_hour: int, utc_minute: int, enclave: str = "commercial-global") -> Dict:
    solar = resolve_solar_pod(utc_hour, utc_minute)
    fenced = enforce_sovereign_routing(enclave, solar["solar_pod"])
    active_pod = fenced["routed_pod"]
    custody = compute_shift_jit_custody(active_pod)
    return {
        "utc_timestamp": f"{utc_hour:02d}:{utc_minute:02d} UTC",
        "enclave": enclave,
        "active_command_pod": active_pod,
        "warm_handover_overlap": solar["warm_handover_active"],
        "next_incoming_pod": solar["incoming_pod"],
        "sovereignty_decision": fenced,
        "jit_custody_state": custody,
        "overnight_sleep_interrupts": 0
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Follow-the-Sun Solar Shift & Sovereign Dispatcher")
    parser.add_argument("--utc-hour", type=int, default=2)
    parser.add_argument("--utc-minute", type=int, default=30)
    parser.add_argument("--enclave", default="commercial-global")
    args = parser.parse_args()
    print(json.dumps(dispatch_shift_command(args.utc_hour, args.utc_minute, args.enclave), indent=2))
