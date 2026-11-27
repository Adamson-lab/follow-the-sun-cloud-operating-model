# Security Policy: Sovereign Jurisdiction Routing & Shift-Bound JIT Custody

## Reporting a Vulnerability
Report vulnerabilities privately to **Favour Ikeoluwa Adamson** (`favouradamson803@gmail.com`).

## Core Operating Model Security Controls
1. **Sovereign Jurisdiction Precedence:** FedRAMP/ITAR workloads are never routed to non-CONUS pods regardless of UTC hour.
2. **Shift-Synchronized JIT Custody:** Cloud write permissions expire automatically at shift end (`8.5h TTL`).
3. **GDPR Edge Redaction:** EU personal data is tokenized at the Frankfurt edge prior to cross-region handover.
