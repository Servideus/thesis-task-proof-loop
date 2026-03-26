from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_ROOT / "templates"
TASKS_DIR = Path(".agents") / "tasks"
MANAGED_BLOCK_START = "<!-- thesis-task-proof-loop:begin -->"
MANAGED_BLOCK_END = "<!-- thesis-task-proof-loop:end -->"

REQUIRED_TASK_FILES = {
    "spec.md": "spec.template.md",
    "requirements.md": "requirements.template.md",
    "writing_profile.md": "writing_profile.template.md",
    "advisor_preferences.md": "advisor_preferences.template.md",
    "sources_registry.md": "sources_registry.template.md",
    "candidate_sources.md": "candidate_sources.template.md",
    "outline.md": "outline.template.md",
    "draft.md": "draft.template.md",
    "claim_source_map.csv": "claim_source_map.template.csv",
    "quotes.md": "quotes.template.md",
    "evidence.md": "evidence.template.md",
    "evidence.json": "evidence.template.json",
    "feedback_digest.md": "feedback_digest.template.md",
    "handoff.md": "handoff.template.md",
    "problems.md": "problems.template.md",
    "revision_log.md": "revision_log.template.md",
    "verdict.json": "verdict.template.json",
    "scratchpad.md": "scratchpad.template.md",
}

EMPTY_TASK_FILES = (
    "feedback_log.jsonl",
    "events.jsonl",
)

EVIDENCE_DEPENDENCY_FILES = (
    "spec.md",
    "requirements.md",
    "writing_profile.md",
    "advisor_preferences.md",
    "sources_registry.md",
    "candidate_sources.md",
    "outline.md",
    "draft.md",
    "claim_source_map.csv",
    "quotes.md",
    "feedback_log.jsonl",
    "revision_log.md",
)

EVIDENCE_BUNDLE_FILES = (
    "evidence.md",
    "evidence.json",
    "feedback_digest.md",
)

VERDICT_DEPENDENCY_FILES = (
    "spec.md",
    "requirements.md",
    "writing_profile.md",
    "advisor_preferences.md",
    "sources_registry.md",
    "candidate_sources.md",
    "outline.md",
    "draft.md",
    "claim_source_map.csv",
    "quotes.md",
    "evidence.md",
    "evidence.json",
    "feedback_digest.md",
)

GUIDE_BLOCK = """<!-- thesis-task-proof-loop:begin -->
Use `thesis-task-proof-loop` for long academic writing tasks in this repository.

Task folder:
- `.agents/tasks/<TASK_ID>/`

Main-line rule:
- Treat task files as the source of truth.
- Keep approved sources in `sources_registry.md`.
- Keep unapproved or side-track materials in `candidate_sources.md` or `scratchpad.md`.
- Run verification in a fresh session.
- Apply only minimal traceable fixes after `problems.md`.

Recommended command order:
1. `init`
2. `freeze`
3. `sources`
4. `outline`
5. `draft`
6. `map`
7. `evidence`
8. `verify`
9. `fix`
10. `verify`

Before any reset or role change:
- update touched artifacts
- refresh `feedback_digest.md`
- refresh `handoff.md`
- append an event to `events.jsonl`
<!-- thesis-task-proof-loop:end -->
"""


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def write_text_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def replace_managed_block(existing: str, block: str) -> str:
    pattern = re.compile(
        rf"{re.escape(MANAGED_BLOCK_START)}.*?{re.escape(MANAGED_BLOCK_END)}",
        re.DOTALL,
    )
    if pattern.search(existing):
        updated = pattern.sub(block, existing)
        return updated.rstrip() + "\n"
    if existing.strip():
        return existing.rstrip() + "\n\n" + block.rstrip() + "\n"
    return block.rstrip() + "\n"


def git_repo_root(start: Path) -> Path | None:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    stdout = proc.stdout.strip()
    return Path(stdout) if stdout else None


def detect_repo_root(start: Path) -> Path:
    root = git_repo_root(start)
    if root is not None:
        return root

    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def normalize_task_id(task_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", task_id.strip())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    if not cleaned:
        raise ValueError("task id must contain letters, digits, dot, underscore, or dash")
    return cleaned


def load_task_seed(task_file: str | None, task_text: str | None) -> str:
    if task_file and task_text:
        raise ValueError("use either --task-file or --task-text, not both")
    if task_file:
        return Path(task_file).read_text(encoding="utf-8").strip()
    return (task_text or "").strip()


def render_template(template_name: str, task_id: str, task_statement: str) -> str:
    template_path = TEMPLATES_DIR / template_name
    content = template_path.read_text(encoding="utf-8")
    rendered = content.replace("<TASK_ID>", task_id)
    rendered = rendered.replace("<TASK_STATEMENT>", task_statement or "(заполни исходную формулировку задачи)")
    return rendered


def task_dir(repo_root: Path, task_id: str) -> Path:
    return repo_root / TASKS_DIR / task_id


def write_guides(repo_root: Path, guides_mode: str) -> None:
    guide_targets: list[Path] = []
    if guides_mode in {"auto", "both", "agents"}:
        guide_targets.append(repo_root / "AGENTS.md")
    if guides_mode in {"auto", "both", "claude"}:
        guide_targets.append(repo_root / "CLAUDE.md")

    for guide_path in guide_targets:
        updated = replace_managed_block(read_text(guide_path), GUIDE_BLOCK)
        guide_path.write_text(updated, encoding="utf-8", newline="\n")


def init_task(args: argparse.Namespace) -> int:
    repo_root = detect_repo_root(Path.cwd())
    task_id = normalize_task_id(args.task_id)
    task_statement = load_task_seed(args.task_file, args.task_text)
    target_dir = task_dir(repo_root, task_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "raw").mkdir(exist_ok=True)

    for file_name, template_name in REQUIRED_TASK_FILES.items():
        rendered = render_template(template_name, task_id, task_statement)
        write_text_if_missing(target_dir / file_name, rendered)

    for file_name in EMPTY_TASK_FILES:
        write_text_if_missing(target_dir / file_name, "")

    if args.guides != "none":
        write_guides(repo_root, args.guides)

    print(f"Initialized {target_dir}")
    return 0


def parse_json(path: Path, required_keys: Iterable[str]) -> tuple[dict, list[str]]:
    errors: list[str] = []
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return {}, [f"{path.name}: invalid JSON ({exc})"]
    missing = [key for key in required_keys if key not in data]
    if missing:
        errors.append(f"{path.name}: missing keys {', '.join(missing)}")
    return data, errors


def outline_section_ids(path: Path) -> set[str]:
    section_ids: set[str] = set()
    pattern = re.compile(r"^## \[([A-Za-z]\d+(?:\.\d+)*)\] ")
    for line in read_text(path).splitlines():
        match = pattern.match(line.strip())
        if match:
            section_ids.add(match.group(1))
    return section_ids


def parse_sources_registry(path: Path) -> set[str]:
    source_ids: set[str] = set()
    for line in read_text(path).splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        source_id, short_title = cells[0], cells[1]
        if source_id in {"source_id", "---", ""}:
            continue
        if short_title:
            source_ids.add(source_id)
    return source_ids


def parse_claim_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    text = read_text(path).strip()
    if not text:
        return [], [f"{path.name}: empty file"]
    reader = csv.DictReader(text.splitlines())
    expected_fields = [
        "claim_id",
        "section_id",
        "claim_text",
        "claim_type",
        "source_ids",
        "locator_if_available",
        "direct_quote_used",
        "evidence_strength",
        "confidence_note",
        "gap_flag",
        "notes",
    ]
    if reader.fieldnames != expected_fields:
        return [], [f"{path.name}: unexpected header"]
    return list(reader), []


def parse_jsonl(path: Path, required_keys: Iterable[str]) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}:{line_number}: invalid JSONL ({exc})")
            continue
        missing = [key for key in required_keys if key not in data]
        if missing:
            errors.append(
                f"{path.name}:{line_number}: missing keys {', '.join(missing)}"
            )
    return errors


def existing_paths(base_dir: Path, file_names: Iterable[str]) -> list[Path]:
    return [base_dir / name for name in file_names if (base_dir / name).exists()]


def stale_inputs(target_dir: Path, bundle_files: Iterable[str], dependency_files: Iterable[str]) -> list[str]:
    bundle_paths = existing_paths(target_dir, bundle_files)
    dependency_paths = existing_paths(target_dir, dependency_files)
    if not bundle_paths or not dependency_paths:
        return []

    oldest_bundle_mtime = min(path.stat().st_mtime_ns for path in bundle_paths)
    return [
        path.name
        for path in dependency_paths
        if path.stat().st_mtime_ns > oldest_bundle_mtime
    ]


def validate_task_dir(target_dir: Path, task_id: str) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not target_dir.exists():
        return ValidationResult([f"task directory not found: {target_dir}"], [])

    required_paths = [target_dir / name for name in REQUIRED_TASK_FILES]
    required_paths.extend(target_dir / name for name in EMPTY_TASK_FILES)
    required_paths.append(target_dir / "raw")
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing required path: {path.name}")

    if errors:
        return ValidationResult(errors, warnings)

    evidence_json, evidence_errors = parse_json(
        target_dir / "evidence.json",
        (
            "task_id",
            "generated_at",
            "artifact_timestamps",
            "overall_status",
            "acceptance_criteria",
            "quality_gates",
            "artifacts_used",
            "recommended_next_step",
        ),
    )
    errors.extend(evidence_errors)

    verdict_json, verdict_errors = parse_json(
        target_dir / "verdict.json",
        (
            "task_id",
            "generated_at",
            "artifact_timestamps",
            "overall_verdict",
            "acceptance_criteria",
            "quality_gates",
            "artifacts_used",
            "warnings",
            "blocking_issues",
        ),
    )
    errors.extend(verdict_errors)

    for file_name, field_name in (
        ("evidence.json", "overall_status"),
        ("verdict.json", "overall_verdict"),
    ):
        data = evidence_json if file_name == "evidence.json" else verdict_json
        value = data.get(field_name)
        allowed = {"PASS", "PASS_WITH_WARNINGS", "FAIL", "UNKNOWN"}
        if value is not None and value not in allowed:
            errors.append(f"{file_name}: invalid {field_name} '{value}'")

    for file_name, data in (("evidence.json", evidence_json), ("verdict.json", verdict_json)):
        value = data.get("task_id")
        if value and value != task_id:
            errors.append(f"{file_name}: task_id '{value}' does not match '{task_id}'")

    if evidence_json.get("overall_status") != "UNKNOWN":
        if not str(evidence_json.get("generated_at", "")).strip():
            warnings.append("evidence.json: overall_status is set but generated_at is empty")
        if not evidence_json.get("artifact_timestamps"):
            warnings.append("evidence.json: overall_status is set but artifact_timestamps is empty")
    if verdict_json.get("overall_verdict") != "UNKNOWN":
        if not str(verdict_json.get("generated_at", "")).strip():
            warnings.append("verdict.json: overall_verdict is set but generated_at is empty")
        if not verdict_json.get("artifact_timestamps"):
            warnings.append("verdict.json: overall_verdict is set but artifact_timestamps is empty")

    rows, row_errors = parse_claim_rows(target_dir / "claim_source_map.csv")
    errors.extend(row_errors)

    source_ids = parse_sources_registry(target_dir / "sources_registry.md")
    outline_ids = outline_section_ids(target_dir / "outline.md")
    draft_ids = outline_section_ids(target_dir / "draft.md")
    known_sections = outline_ids | draft_ids

    if not outline_ids:
        warnings.append("outline.md has no canonical section ids like '## [S1] ...'")
    if not draft_ids:
        warnings.append("draft.md has no canonical section ids like '## [S1] ...'")

    for row in rows:
        claim_id = row["claim_id"].strip()
        section_id = row["section_id"].strip()
        claim_text = row["claim_text"].strip()
        source_field = row["source_ids"].strip()
        direct_quote = row["direct_quote_used"].strip().lower()

        if claim_id and not claim_text:
            warnings.append(f"claim {claim_id}: empty claim_text")
        if section_id and known_sections and section_id not in known_sections:
            errors.append(f"claim {claim_id}: unknown section_id '{section_id}'")
        if source_field:
            for source_id in [part.strip() for part in source_field.split(";") if part.strip()]:
                if source_ids and source_id not in source_ids:
                    errors.append(f"claim {claim_id}: unknown source_id '{source_id}'")
        if direct_quote in {"yes", "true", "да"} and not read_text(target_dir / "quotes.md").strip():
            warnings.append(f"claim {claim_id}: direct quote flagged but quotes.md is empty")

    errors.extend(
        parse_jsonl(
            target_dir / "feedback_log.jsonl",
            (
                "feedback_id",
                "source",
                "signal_type",
                "raw_feedback",
                "distilled_hint",
                "action_required",
                "status",
            ),
        )
    )
    errors.extend(
        parse_jsonl(
            target_dir / "events.jsonl",
            (
                "timestamp",
                "event_type",
                "role",
                "summary",
                "next_step",
            ),
        )
    )

    stale_evidence = stale_inputs(target_dir, EVIDENCE_BUNDLE_FILES, EVIDENCE_DEPENDENCY_FILES)
    if stale_evidence and evidence_json.get("overall_status") != "UNKNOWN":
        warnings.append(
            "evidence artifacts appear stale relative to: "
            + ", ".join(sorted(set(stale_evidence)))
        )

    stale_verdict = stale_inputs(target_dir, ("verdict.json",), VERDICT_DEPENDENCY_FILES)
    if stale_verdict and verdict_json.get("overall_verdict") != "UNKNOWN":
        warnings.append(
            "verdict.json appears stale relative to: "
            + ", ".join(sorted(set(stale_verdict)))
        )

    return ValidationResult(errors, warnings)


def validate_task(args: argparse.Namespace) -> int:
    repo_root = detect_repo_root(Path.cwd())
    task_id = normalize_task_id(args.task_id)
    target_dir = task_dir(repo_root, task_id)
    result = validate_task_dir(target_dir, task_id)
    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")
    if result.ok:
        print(f"Validation passed for {target_dir}")
        return 0
    return 1


def count_jsonl_entries(path: Path) -> int:
    return sum(1 for line in read_text(path).splitlines() if line.strip())


def has_placeholder(text: str) -> bool:
    markers = (
        "<TASK_STATEMENT>",
        "[todo]",
        "заполни",
        "placeholder",
        "риск 1:",
        "шаг 1:",
        "название раздела",
        "здесь пишется содержательный текст",
    )
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in markers)


def infer_next_step(
    target_dir: Path,
    evidence_json: dict,
    verdict_json: dict,
    sections_count: int,
    nonempty_claims: int,
    sources_count: int,
    evidence_stale: bool,
    verdict_stale: bool,
) -> str:
    spec_text = read_text(target_dir / "spec.md")
    outline_text = read_text(target_dir / "outline.md")
    draft_text = read_text(target_dir / "draft.md")

    if not spec_text.strip() or has_placeholder(spec_text):
        return "freeze"
    if sources_count == 0:
        return "sources"
    if sections_count == 0 or has_placeholder(outline_text):
        return "outline"
    if not draft_text.strip() or has_placeholder(draft_text):
        return "draft"
    if nonempty_claims == 0:
        return "map"
    if evidence_json.get("overall_status") == "UNKNOWN" or evidence_stale:
        return "evidence"
    verdict = verdict_json.get("overall_verdict", "UNKNOWN")
    if verdict == "UNKNOWN" or verdict_stale:
        return "verify"
    if verdict in {"FAIL", "PASS_WITH_WARNINGS"}:
        return "fix"
    return "status"


def status_task(args: argparse.Namespace) -> int:
    repo_root = detect_repo_root(Path.cwd())
    task_id = normalize_task_id(args.task_id)
    target_dir = task_dir(repo_root, task_id)

    if not target_dir.exists():
        print(f"Task not found: {target_dir}")
        print("Suggested next command: init")
        return 1

    result = validate_task_dir(target_dir, task_id)
    evidence_json, _ = parse_json(
        target_dir / "evidence.json",
        (
            "task_id",
            "overall_status",
            "acceptance_criteria",
            "quality_gates",
            "artifacts_used",
            "recommended_next_step",
        ),
    )
    verdict_json, _ = parse_json(
        target_dir / "verdict.json",
        (
            "task_id",
            "overall_verdict",
            "acceptance_criteria",
            "quality_gates",
            "artifacts_used",
            "warnings",
            "blocking_issues",
        ),
    )

    sources_count = len(parse_sources_registry(target_dir / "sources_registry.md"))
    sections_count = len(outline_section_ids(target_dir / "outline.md"))
    claims, _ = parse_claim_rows(target_dir / "claim_source_map.csv")
    nonempty_claims = sum(1 for row in claims if row.get("claim_text", "").strip())
    stale_evidence_inputs = stale_inputs(target_dir, EVIDENCE_BUNDLE_FILES, EVIDENCE_DEPENDENCY_FILES)
    stale_verdict_inputs = stale_inputs(target_dir, ("verdict.json",), VERDICT_DEPENDENCY_FILES)
    next_step = infer_next_step(
        target_dir,
        evidence_json,
        verdict_json,
        sections_count,
        nonempty_claims,
        sources_count,
        bool(stale_evidence_inputs),
        bool(stale_verdict_inputs),
    )

    print(f"Task: {task_id}")
    print(f"Path: {target_dir}")
    print(f"Validation: {'OK' if result.ok else 'ERRORS'}")
    print(f"Evidence overall_status: {evidence_json.get('overall_status', 'UNKNOWN')}")
    print(f"Verdict overall_verdict: {verdict_json.get('overall_verdict', 'UNKNOWN')}")
    print(f"Sources registered: {sources_count}")
    print(f"Outline sections: {sections_count}")
    print(f"Mapped claims: {nonempty_claims}")
    print(f"Feedback entries: {count_jsonl_entries(target_dir / 'feedback_log.jsonl')}")
    print(f"Event entries: {count_jsonl_entries(target_dir / 'events.jsonl')}")
    print(
        "Evidence stale: "
        + ("yes" if stale_evidence_inputs else "no")
        + (
            f" ({', '.join(sorted(set(stale_evidence_inputs)))})"
            if stale_evidence_inputs
            else ""
        )
    )
    print(
        "Verdict stale: "
        + ("yes" if stale_verdict_inputs else "no")
        + (
            f" ({', '.join(sorted(set(stale_verdict_inputs)))})"
            if stale_verdict_inputs
            else ""
        )
    )
    print(f"Suggested next command: {next_step}")
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"- {warning}")
    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(f"- {error}")
    return 0 if result.ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Repo-local workflow tooling for thesis-task-proof-loop."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a repo-local thesis task.")
    init_parser.add_argument("--task-id", required=True)
    init_parser.add_argument("--task-file")
    init_parser.add_argument("--task-text")
    init_parser.add_argument(
        "--guides",
        choices=("auto", "both", "agents", "claude", "none"),
        default="none",
        help="Create or refresh managed guidance blocks in AGENTS.md / CLAUDE.md.",
    )
    init_parser.set_defaults(func=init_task)

    validate_parser = subparsers.add_parser("validate", help="Validate the task artifact set.")
    validate_parser.add_argument("--task-id", required=True)
    validate_parser.set_defaults(func=validate_task)

    status_parser = subparsers.add_parser("status", help="Summarize task status and next step.")
    status_parser.add_argument("--task-id", required=True)
    status_parser.set_defaults(func=status_task)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
