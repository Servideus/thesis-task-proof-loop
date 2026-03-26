# Quality Gates

Use these gates when freezing the task and when reviewing the result.

## Core gates

### QG1. Scope match
The output matches the frozen task and does not drift into unrelated material.

### QG2. Outline match
The output follows the approved outline or records justified deviations explicitly.

### QG3. Source discipline
Core claims rely only on approved sources from `sources_registry.md`.

### QG4. Traceability
Substantive claims are present in `claim_source_map.csv`.

### QG5. Citation plausibility
No invented bibliographic details, page numbers, or quotations.

### QG6. Evidence proportionality
Claims are no stronger than the evidence allows.

### QG7. Internal logic
The section is coherent, non-contradictory, and ordered.

### QG8. Terminology consistency
Key terms are used consistently unless a distinction is explicitly introduced.

### QG9. Formatting compliance
Known formatting rules are followed or deviations are recorded.

### QG10. Honest uncertainty
Open questions, weak evidence, and unresolved limits are labeled.

## Optional gates

### QG11. Concision
The text is not padded with generic filler.

### QG12. Quote control
Direct quotations are used deliberately and recorded in `quotes.md` when relevant.

### QG13. Revision discipline
Fixes are targeted and logged in `revision_log.md`.

## Review result meanings

### PASS
The section meets the core gates.

### PASS_WITH_WARNINGS
The section is usable, but there are non-blocking risks that must remain visible.

### FAIL
The section is not reliable enough because scope, sources, traceability, or logic are insufficient.
