# Data

This directory contains schemas, small reproducible samples, experiment templates, and non-sensitive reference data.

## Do not commit

- secrets or API keys;
- private personal contact data;
- credentials/session tokens;
- large raw exports from paid/licensed databases unless redistribution/storage rights explicitly allow it;
- sensitive supplier commercial data without permission;
- buyer/supplier private communications unless deliberately redacted and permitted.

## Planned structure

- `schemas/` — canonical opportunity, buyer, supplier, evidence schemas
- `samples/` — synthetic/redacted examples for tests
- `experiments/` — real benchmark results where storage is appropriate

Raw external data should retain provenance fields and be stored outside Git when licensing/privacy requires it.
