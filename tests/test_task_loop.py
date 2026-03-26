import io
import json
import os
import shutil
import subprocess
import unittest
import uuid
from contextlib import contextmanager, redirect_stdout
from pathlib import Path

from scripts import task_loop


@contextmanager
def pushd(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class TaskLoopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace_tmp_root = Path(__file__).resolve().parents[1] / ".tmp_test_work"
        self.workspace_tmp_root.mkdir(exist_ok=True)
        self.repo_root = self.workspace_tmp_root / f"task-loop-{uuid.uuid4().hex}"
        self.repo_root.mkdir()
        self.addCleanup(shutil.rmtree, self.repo_root, True)
        self.addCleanup(self.cleanup_workspace_tmp_root)
        subprocess.run(
            ["git", "init"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        with pushd(self.repo_root), redirect_stdout(io.StringIO()):
            rc = task_loop.main(
                [
                    "init",
                    "--task-id",
                    "chapter-1",
                    "--task-text",
                    "Подготовить главу 1 дипломной работы",
                    "--guides",
                    "both",
                ]
        )
        self.assertEqual(rc, 0)
        self.task_dir = self.repo_root / ".agents" / "tasks" / "chapter-1"

    def cleanup_workspace_tmp_root(self) -> None:
        try:
            self.workspace_tmp_root.rmdir()
        except OSError:
            pass

    def capture_main(self, argv: list[str]) -> tuple[int, str]:
        buffer = io.StringIO()
        with pushd(self.repo_root), redirect_stdout(buffer):
            rc = task_loop.main(argv)
        return rc, buffer.getvalue()

    def write_text(self, relative_path: str, content: str) -> None:
        path = self.task_dir / relative_path
        path.write_text(content, encoding="utf-8", newline="\n")

    def write_json(self, relative_path: str, data: dict) -> None:
        self.write_text(relative_path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    def set_mtime(self, relative_path: str, timestamp: int) -> None:
        path = self.task_dir / relative_path
        os.utime(path, (timestamp, timestamp))

    def populate_complete_task(self) -> None:
        self.write_text(
            "spec.md",
            "# Spec\n\n"
            "## Task\n"
            "Chapter 1 is frozen.\n\n"
            "## Acceptance\n"
            "- AC1: Scope is frozen.\n",
        )
        self.write_text(
            "requirements.md",
            "# Requirements\n\n"
            "- keep structure: yes\n"
            "- fresh verify: yes\n",
        )
        self.write_text(
            "writing_profile.md",
            "# Writing Profile\n\n"
            "- avoid fluff\n",
        )
        self.write_text(
            "advisor_preferences.md",
            "# Advisor Preferences\n\n"
            "- prefer cautious wording\n",
        )
        self.write_text(
            "sources_registry.md",
            "# Sources\n\n"
            "| source_id | краткое название | тип источника | язык | уровень доверия | полный текст доступен | допустимое использование | проверенный локатор доступен | заметки |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| S1 | Основной источник | статья | ru | высокий | да | несущие тезисы | да | |\n",
        )
        self.write_text(
            "candidate_sources.md",
            "# Candidate Sources\n\n"
            "| candidate_id | краткое название | почему рассматривается | статус проверки | можно ли перевести в approved | заметки |\n"
            "|---|---|---|---|---|---|\n",
        )
        self.write_text(
            "outline.md",
            "# Outline\n\n"
            "## [S1] Реальный раздел\n"
            "- цель раздела: показать подход\n"
            "- planned claims:\n"
            "  - [C1]\n",
        )
        self.write_text(
            "draft.md",
            "# Draft\n\n"
            "## [S1] Реальный раздел\n\n"
            "Это реальный текст раздела.\n",
        )
        self.write_text(
            "claim_source_map.csv",
            "claim_id,section_id,claim_text,claim_type,source_ids,locator_if_available,direct_quote_used,evidence_strength,confidence_note,gap_flag,notes\n"
            "C1,S1,\"Это реальный тезис\",fact,S1,,нет,strong,,no,\n",
        )
        self.write_text("quotes.md", "# Quotes\n")
        self.write_text("evidence.md", "# Evidence\n\n- AC1: pass\n")
        self.write_text("feedback_digest.md", "# Feedback Digest\n\n- H1: keep claims cautious\n")
        self.write_text("handoff.md", "# Handoff\n\n- stable: S1\n")
        self.write_text("problems.md", "# Problems\n\n## Неблокирующие проблемы\n")
        self.write_text("revision_log.md", "# Revision Log\n\n- iteration 1\n")
        self.write_text(
            "feedback_log.jsonl",
            json.dumps(
                {
                    "feedback_id": "F1",
                    "source": "user",
                    "signal_type": "directive",
                    "raw_feedback": "Сделай формулировку осторожнее.",
                    "distilled_hint": "Ослабь слишком сильные выводы.",
                    "action_required": "update draft",
                    "status": "applied",
                },
                ensure_ascii=False,
            )
            + "\n",
        )
        self.write_text(
            "events.jsonl",
            json.dumps(
                {
                    "timestamp": "2026-03-26T23:10:00Z",
                    "event_type": "phase_complete",
                    "role": "section-drafter",
                    "summary": "Draft refreshed",
                    "next_step": "evidence",
                }
            )
            + "\n",
        )
        self.write_json(
            "evidence.json",
            {
                "task_id": "chapter-1",
                "generated_at": "2026-03-26T23:10:00Z",
                "artifact_timestamps": {"draft.md": "2026-03-26T23:09:00Z"},
                "overall_status": "PASS",
                "acceptance_criteria": [
                    {"id": "AC1", "text": "Scope is frozen", "status": "PASS", "proof": [], "gaps": []}
                ],
                "quality_gates": [
                    {"id": "QG3", "status": "PASS", "reason": "Sources are registered."}
                ],
                "artifacts_used": ["draft.md", "claim_source_map.csv"],
                "recommended_next_step": "verify",
                "unresolved_gaps": [],
            },
        )
        self.write_json(
            "verdict.json",
            {
                "task_id": "chapter-1",
                "generated_at": "2026-03-26T23:12:00Z",
                "artifact_timestamps": {"evidence.json": "2026-03-26T23:10:00Z"},
                "overall_verdict": "PASS",
                "acceptance_criteria": [
                    {"id": "AC1", "status": "PASS", "reason": "Verified."}
                ],
                "quality_gates": [
                    {"id": "QG3", "status": "PASS", "reason": "Verified."}
                ],
                "artifacts_used": ["draft.md", "evidence.json"],
                "warnings": [],
                "blocking_issues": [],
            },
        )

    def test_init_creates_required_artifacts_and_guides(self) -> None:
        self.assertTrue((self.task_dir / "evidence.json").exists())
        self.assertTrue((self.task_dir / "feedback_digest.md").exists())
        self.assertTrue((self.task_dir / "scratchpad.md").exists())
        self.assertTrue((self.repo_root / "AGENTS.md").exists())
        self.assertTrue((self.repo_root / "CLAUDE.md").exists())
        self.assertIn("thesis-task-proof-loop", (self.repo_root / "AGENTS.md").read_text(encoding="utf-8"))

    def test_validate_passes_after_init(self) -> None:
        rc, output = self.capture_main(["validate", "--task-id", "chapter-1"])
        self.assertEqual(rc, 0)
        self.assertIn("Validation passed", output)

    def test_status_suggests_evidence_when_evidence_bundle_is_stale(self) -> None:
        self.populate_complete_task()

        base = 1_700_000_000
        for index, relative_path in enumerate(
            [
                "spec.md",
                "requirements.md",
                "writing_profile.md",
                "advisor_preferences.md",
                "sources_registry.md",
                "candidate_sources.md",
                "outline.md",
                "claim_source_map.csv",
                "quotes.md",
                "feedback_log.jsonl",
                "revision_log.md",
                "evidence.md",
                "evidence.json",
                "feedback_digest.md",
                "verdict.json",
                "draft.md",
            ],
            start=1,
        ):
            self.set_mtime(relative_path, base + index)

        rc, output = self.capture_main(["status", "--task-id", "chapter-1"])
        self.assertEqual(rc, 0)
        self.assertIn("Evidence stale: yes", output)
        self.assertIn("Suggested next command: evidence", output)

    def test_status_suggests_verify_when_verdict_is_stale_but_evidence_is_fresh(self) -> None:
        self.populate_complete_task()

        base = 1_700_100_000
        for index, relative_path in enumerate(
            [
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
                "verdict.json",
                "evidence.md",
                "evidence.json",
                "feedback_digest.md",
            ],
            start=1,
        ):
            self.set_mtime(relative_path, base + index)

        rc, output = self.capture_main(["status", "--task-id", "chapter-1"])
        self.assertEqual(rc, 0)
        self.assertIn("Evidence stale: no", output)
        self.assertIn("Verdict stale: yes", output)
        self.assertIn("Suggested next command: verify", output)

    def test_validate_warns_when_evidence_and_verdict_are_stale(self) -> None:
        self.populate_complete_task()

        base = 1_700_200_000
        for index, relative_path in enumerate(
            [
                "spec.md",
                "requirements.md",
                "writing_profile.md",
                "advisor_preferences.md",
                "sources_registry.md",
                "candidate_sources.md",
                "outline.md",
                "claim_source_map.csv",
                "quotes.md",
                "feedback_log.jsonl",
                "revision_log.md",
                "evidence.md",
                "evidence.json",
                "feedback_digest.md",
                "verdict.json",
                "draft.md",
            ],
            start=1,
        ):
            self.set_mtime(relative_path, base + index)

        rc, output = self.capture_main(["validate", "--task-id", "chapter-1"])
        self.assertEqual(rc, 0)
        self.assertIn("WARNING: evidence artifacts appear stale relative to: draft.md", output)
        self.assertIn("WARNING: verdict.json appears stale relative to: draft.md", output)


if __name__ == "__main__":
    unittest.main()
