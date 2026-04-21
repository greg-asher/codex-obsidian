# Validation

1. Run `obsidian version` using the sanitized wrapper.
2. Run read-only checks: `sync:status`, `publish:status`, `publish:list`.
3. Validate restore guardrails with an explicit `path=` and `version=` test plan.
4. Validate publish mutation guardrails with explicit scope messaging.
5. Confirm response includes risk level and side-effect summary.
6. Confirm Headless Sync requests are treated as out-of-scope.
