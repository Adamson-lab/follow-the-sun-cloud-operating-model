from typing import Dict

def enforce_sovereign_routing(enclave: str, candidate_pod: str) -> Dict:
    """Ensures FedRAMP/ITAR workloads stay inside CONUS cleared sub-pods regardless of UTC hour."""
    sovereign_enclaves = {"fedramp-high-us", "dod-il4-us", "itar-restricted"}
    if enclave.lower() in sovereign_enclaves and not candidate_pod.startswith("AMER"):
        return {
            "sovereign_override_applied": True,
            "original_solar_pod": candidate_pod,
            "routed_pod": "AMER-SOVEREIGN-CONUS",
            "reason": f"Sovereign enclave '{enclave}' restricted to US-Citizen CONUS pod"
        }
    return {
        "sovereign_override_applied": False,
        "original_solar_pod": candidate_pod,
        "routed_pod": candidate_pod,
        "reason": "Standard global follow-the-sun routing permitted"
    }
