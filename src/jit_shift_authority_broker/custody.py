from typing import Dict

ALL_PODS = ["AMER-NEW-YORK", "APAC-SINGAPORE", "EMEA-FRANKFURT", "AMER-SOVEREIGN-CONUS"]

def compute_shift_jit_custody(active_pod: str) -> Dict[str, str]:
    """Grants 8.5h write custody strictly to the active daylight pod and locks sleeping pods to read-only."""
    custody_map = {}
    for pod in ALL_PODS:
        if pod == active_pod:
            custody_map[pod] = "ACTIVE_WRITE_CUSTODY (TTL=8.5h)"
        else:
            custody_map[pod] = "READ_ONLY_OBSERVABILITY (SLEEP_PROTECTED)"
    return custody_map
