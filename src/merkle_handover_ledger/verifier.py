import argparse
import hashlib
import json
from datetime import datetime, timezone
from typing import List, Dict

def sha256_hex(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def compute_merkle_root(leaves: List[Dict]) -> str:
    if not leaves:
        return sha256_hex("EMPTY_HANDOVER_LEDGER")
    layer = [sha256_hex(json.dumps(x, sort_keys=True)) for x in leaves]
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        layer = [sha256_hex(layer[i] + layer[i + 1]) for i in range(0, len(layer), 2)]
    return layer[0]

def seal_handover_attestation(manifest: Dict) -> Dict:
    leaves = manifest.get("attestation_leaves", [])
    root = compute_merkle_root(leaves)
    return {
        "schema_version": "1.0.0-FTS-DORA-MASTRM-MERKLE",
        "sealed_at_utc": datetime.now(timezone.utc).isoformat(),
        "merkle_root_sha256": root,
        "worm_storage_anchors": [
            f"s3://adamson-lab-fts-worm/handovers/{root[:16]}.json",
            f"https://adamsonlabftsworm.blob.core.windows.net/handovers/{root[:16]}.json",
            f"gs://adamson-lab-fts-worm-gcp/handovers/{root[:16]}.json"
        ],
        "handover_record": manifest
    }

def verify_handover_ledger(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    expected = doc["merkle_root_sha256"]
    recomputed = compute_merkle_root(doc["handover_record"]["attestation_leaves"])
    if expected != recomputed:
        raise ValueError(f"EU DORA HANDOVER TAMPER ALERT: {expected} != {recomputed}")
    print(f"[VERIFIED] Shift Handover Merkle Root: {recomputed}")
    print(f"[VERIFIED] Transition: {doc['handover_record']['outgoing_pod']} -> {doc['handover_record']['incoming_pod']}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify EU DORA & MAS TRM Shift Handover Merkle Proof")
    parser.add_argument("--ledger", required=True)
    args = parser.parse_args()
    verify_handover_ledger(args.ledger)
