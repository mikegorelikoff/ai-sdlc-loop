#!/usr/bin/env python3
"""Feature-level state machine for AI SDLC skill chains.

The module keeps the lifecycle graph, compact TOON state serialization, and
hybrid quick/full transition enforcement in one place so individual skills do
not invent their own chain rules.
"""

from __future__ import annotations

import argparse
import ast
from ai_sdlc_toon import encode_toon
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from ai_sdlc_artifact_profiles import PROFILES
from ai_sdlc_paths import atomic_write_text, first_existing, legacy_state_path, state_path, workspace_base, write_lock
from ai_sdlc_validation_receipt import validate_receipt


STATUSES = {"not_started", "in_progress", "blocked", "done", "skipped", "not_applicable"}
COMPLETE_STATUSES = {"done", "skipped", "not_applicable"}


@dataclass(frozen=True)
class StageDef:
    """Canonical lifecycle stage definition."""

    stage_id: str
    skill: str
    workspace: str
    artifacts: str
    predecessors: tuple[str, ...] = ()
    optional: bool = False


REFINEMENT_STAGES: tuple[StageDef, ...] = tuple(
    StageDef(
        profile.stage_id,
        profile.skill,
        "refinement",
        profile.artifact_name,
        profile.predecessors,
        profile.optional,
    )
    for profile in PROFILES
)


STAGES: tuple[StageDef, ...] = REFINEMENT_STAGES + (
    StageDef("branching", "ai-sdlc-loop-branching", "implementation", "branch-plan.md", ()),
    StageDef("sdd", "ai-sdlc-sdd", "implementation", "specs/<feature>", ("branching",)),
    StageDef("validation", "ai-sdlc-loop-validation", "implementation", "validation.md", ("sdd",)),
    StageDef("code_review", "ai-sdlc-loop-code-review", "implementation", "code-review.md", ("validation",)),
    StageDef("security_testing", "ai-sdlc-loop-security-testing", "implementation", "security-review.md", ("sdd",), True),
    StageDef("commit_prep", "ai-sdlc-loop-commit-prep", "implementation", "commit-readiness.md", ("code_review",)),
    StageDef("conventional_commit", "ai-sdlc-loop-conventional-commit", "implementation", "commit-message.md", ("commit_prep",)),
    StageDef("approvals_sandbox", "ai-sdlc-loop-approvals-sandbox", "utility", "approval-plan.md", (), True),
)


STAGE_BY_ID = {stage.stage_id: stage for stage in STAGES}
STAGE_BY_SKILL = {stage.skill: stage for stage in STAGES}


def initial_state(feature: str, workspace: str, entrypoint: str | None = None, *, observed_on: date | None = None) -> dict[str, object]:
    """Create a complete state dictionary with all lifecycle stages."""
    current_stage = entrypoint or ("branching" if workspace == "implementation" else "discovery")
    stages = []
    for stage in STAGES:
        status = "not_applicable" if stage.workspace == "utility" else "not_started"
        if stage.stage_id == current_stage:
            status = "not_started"
        stages.append(
            {
                "id": stage.stage_id,
                "skill": stage.skill,
                "status": status,
                "workspace": stage.workspace,
                "artifacts": stage.artifacts.replace("<feature>", feature),
                "decision_ref": "",
            }
        )
    state: dict[str, object] = {
        "feature": feature,
        "workspace": workspace,
        "current_stage": current_stage,
        "active_skill": "",
        "flow_mode": "default",
        "updated_at": (observed_on or date.today()).isoformat(),
        "decision_log": f"{workspace_base(workspace)}/{feature}/decision-log.md",
        "upstream_state": state_path(feature, "refinement").as_posix() if workspace == "implementation" else "",
        "stages": stages,
        "skips": [],
    }
    return state


def csv_escape(value: object) -> str:
    """Use the canonical scalar encoder; never edit semantic punctuation."""
    return encode_toon(str(value)).rstrip("\n")


def to_toon(state: dict[str, object]) -> str:
    """Serialize state using the repository's compact TOON subset."""
    validate_state_shape(state)
    lines = [
        f"feature: {csv_escape(state.get('feature', ''))}",
        f"workspace: {csv_escape(state.get('workspace', ''))}",
        f"current_stage: {csv_escape(state.get('current_stage', ''))}",
        f"active_skill: {csv_escape(state.get('active_skill', ''))}".rstrip(),
        f"flow_mode: {csv_escape(state.get('flow_mode', 'default'))}",
        f"updated_at: {csv_escape(state.get('updated_at', ''))}",
        f"decision_log: {csv_escape(state.get('decision_log', ''))}",
    ]
    if "upstream_state" in state:
        lines.append(f"upstream_state: {csv_escape(state.get('upstream_state'))}")

    lines.append("")
    lines.append("stages[%d]{id,skill,status,workspace,artifacts,decision_ref}:" % len(state.get("stages", [])))
    order = {stage.stage_id: index for index, stage in enumerate(STAGES)}
    for stage in sorted(state.get("stages", []), key=lambda row: order[row["id"]]):
        row = stage if isinstance(stage, dict) else {}
        lines.append(
            "  "
            + ",".join(
                csv_escape(row.get(key, ""))
                for key in ("id", "skill", "status", "workspace", "artifacts", "decision_ref")
            )
        )

    skips = state.get("skips", [])
    lines.append("")
    lines.append("skips[%d]{stage,reason,decision_ref,flow_mode}:" % len(skips))
    for skip in skips:
        row = skip if isinstance(skip, dict) else {}
        lines.append(
            "  "
            + ",".join(csv_escape(row.get(key, "")) for key in ("stage", "reason", "decision_ref", "flow_mode"))
        )
    return "\n".join(lines).rstrip() + "\n"


def _state_scalar(value: str) -> str:
    """Decode a bounded quoted text scalar; legacy bare empty cells stay readable."""
    if value.startswith('"'):
        try:
            decoded = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ValueError("STATE_PARSE_ERROR: malformed quoted text") from exc
        if not isinstance(decoded, str):
            raise ValueError("STATE_PARSE_ERROR: state cells must be text")
        return decoded
    return value


def parse_row(line: str, columns: tuple[str, ...]) -> dict[str, str]:
    """Read canonical escaped cells without splitting quoted commas."""
    fields = []; start = 0; quoted = False; escaped = False
    source = line.strip()
    for index, character in enumerate(source):
        if escaped:
            escaped = False
        elif character == "\\" and quoted:
            escaped = True
        elif character == '"':
            quoted = not quoted
        elif character == ',' and not quoted:
            fields.append(source[start:index].strip()); start = index + 1
    if quoted or escaped:
        raise ValueError("STATE_PARSE_ERROR: unterminated quoted cell")
    fields.append(source[start:].strip())
    if len(fields) != len(columns):
        raise ValueError("STATE_PARSE_ERROR: row width differs from declared columns")
    return {key: _state_scalar(value) for key, value in zip(columns, fields)}


def validate_state_shape(state: dict[str, object]) -> None:
    """Reject ambiguous state before serialization or lifecycle mutation."""
    if not isinstance(state, dict):
        raise ValueError("STATE_SCHEMA_ERROR: state must be a mapping")
    allowed = {'feature', 'workspace', 'current_stage', 'active_skill', 'flow_mode', 'updated_at', 'decision_log', 'upstream_state', 'stages', 'skips'}
    if set(state) - allowed:
        raise ValueError("STATE_SCHEMA_ERROR: unknown root fields")
    if 'upstream_state' in state and not isinstance(state['upstream_state'], str):
        raise ValueError("STATE_SCHEMA_ERROR: upstream state must be text")
    for key in ('feature', 'workspace', 'current_stage', 'active_skill', 'flow_mode', 'updated_at', 'decision_log'):
        if not isinstance(state.get(key), str):
            raise ValueError("STATE_SCHEMA_ERROR: missing text field " + key)
    if state['flow_mode'] not in ('default', 'quick', 'full'):
        raise ValueError("STATE_SCHEMA_ERROR: invalid flow mode")
    if state['current_stage'] not in STAGE_BY_ID:
        raise ValueError("STATE_SCHEMA_ERROR: unknown current stage")
    identities = set()
    for key, columns in [('stages', ('id','skill','status','workspace','artifacts','decision_ref')), ('skips', ('stage','reason','decision_ref','flow_mode'))]:
        if not isinstance(state.get(key), list):
            raise ValueError("STATE_SCHEMA_ERROR: expected list " + key)
        for row in state[key]:
            if not isinstance(row, dict) or set(row) != set(columns) or any(not isinstance(v, str) for v in row.values()):
                raise ValueError("STATE_SCHEMA_ERROR: invalid " + key + " row")
            if key == 'stages':
                if row['id'] in identities or row['id'] not in STAGE_BY_ID or row['status'] not in STATUSES:
                    raise ValueError("STATE_SCHEMA_ERROR: duplicate/unknown stage or invalid status")
                definition = STAGE_BY_ID[row['id']]
                if row['skill'] != definition.skill or row['workspace'] != definition.workspace:
                    raise ValueError("STATE_SCHEMA_ERROR: stage owner differs from registered policy")
                identities.add(row['id'])
    active = [row['skill'] for row in state['stages'] if row['status'] == 'in_progress']
    if len(active) > 1 or (active and state['active_skill'] != active[0]) or (not active and state['active_skill']):
        raise ValueError("STATE_SCHEMA_ERROR: active skill and in-progress stage disagree")


def from_toon(text: str) -> dict[str, object]:
    """Parse current and legacy state tables with exact counts and field identities."""
    if len(text.encode('utf-8')) > 1_000_000:
        raise ValueError("STATE_PARSE_ERROR: state exceeds byte budget")
    state: dict[str, object] = {}; declarations = {}; mode = None
    columns_by_mode = {'stages': ('id','skill','status','workspace','artifacts','decision_ref'), 'skips': ('stage','reason','decision_ref','flow_mode')}
    for raw in text.splitlines():
        if not raw.strip(): continue
        header = re.fullmatch(r'(stages|skips)\[(\d+)\]\{([^}]+)\}:', raw)
        if header:
            mode, count, columns = header.groups()
            if mode in state or tuple(columns.split(',')) != columns_by_mode[mode]:
                raise ValueError("STATE_PARSE_ERROR: repeated table or invalid columns")
            declarations[mode] = int(count); state[mode] = []
        elif raw.startswith('  ') and mode:
            state[mode].append(parse_row(raw, columns_by_mode[mode]))
        elif ':' in raw and not raw[0].isspace():
            mode = None; key, value = raw.split(':', 1); key = key.strip()
            if key in state: raise ValueError("STATE_PARSE_ERROR: repeated field " + key)
            state[key] = _state_scalar(value.strip())
        else:
            raise ValueError("STATE_PARSE_ERROR: unrecognized state line")
    for key in ('stages', 'skips'):
        if key not in declarations or len(state[key]) != declarations[key]:
            raise ValueError("STATE_PARSE_ERROR: table count mismatch: " + key)
    validate_state_shape(state)
    return state


def load_state(path: Path) -> dict[str, object]:
    """Read state from a TOON file."""
    return from_toon(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, object]) -> None:
    """Write state to a TOON file, creating parent directories."""
    atomic_write_text(path, to_toon(state))


def stage_for_skill(skill: str) -> StageDef:
    """Return the canonical stage definition for a skill name."""
    if skill not in STAGE_BY_SKILL:
        raise ValueError(f"unknown skill: {skill}")
    return STAGE_BY_SKILL[skill]


def stage_row(state: dict[str, object], stage_id: str) -> dict[str, str]:
    """Return the mutable row for a stage in a parsed state dictionary."""
    for row in state.get("stages", []):
        if isinstance(row, dict) and row.get("id") == stage_id:
            return row  # type: ignore[return-value]
    raise ValueError(f"state missing stage: {stage_id}")


def active_stage_rows(state: dict[str, object]) -> list[dict[str, str]]:
    """Return stages currently marked in progress."""
    return [row for row in state.get("stages", []) if isinstance(row, dict) and row.get("status") == "in_progress"]  # type: ignore[return-value]


def flow_mode_from_args(args: argparse.Namespace) -> str:
    """Resolve flow mode from argparse flags with full-flow precedence."""
    if getattr(args, "full_flow", False):
        return "full"
    if getattr(args, "quick_flow", False):
        return "quick"
    return "default"


def validate_transition(
    state: dict[str, object],
    skill: str,
    flow_mode: str,
    decision_ref: str = "",
    assumption: str = "",
) -> tuple[list[str], list[str]]:
    """Validate whether a skill may start or complete in the current state."""
    validate_state_shape(state)
    stage = stage_for_skill(skill)
    errors: list[str] = []
    if flow_mode not in ("default", "quick", "full"):
        errors.append("invalid transition flow mode")
    warnings: list[str] = []

    in_progress = [row for row in active_stage_rows(state) if row.get("skill") != skill]
    if in_progress:
        errors.append("another lifecycle skill is in progress: " + ", ".join(row.get("skill", "") for row in in_progress))

    row = stage_row(state, stage.stage_id)
    if row.get("status") == "blocked" and not decision_ref:
        errors.append("blocked stage requires a decision_ref documenting resolution")
    if row.get("status") == "done":
        warnings.append(f"stage already done: {stage.stage_id}")

    missing = [
        predecessor
        for predecessor in stage.predecessors
        if stage_row(state, predecessor).get("status") not in COMPLETE_STATUSES
    ]
    if missing:
        message = f"predecessor stages not complete for {skill}: {', '.join(missing)}"
        if flow_mode == "quick" and (decision_ref or assumption):
            warnings.append(message + " (quick-flow skip accepted with trace)")
        else:
            errors.append(message)

    return errors, warnings


def record_skip(state: dict[str, object], stage_id: str, reason: str, decision_ref: str, flow_mode: str) -> None:
    """Append a quick-flow skip or assumption record to state."""
    skips = state.setdefault("skips", [])
    assert isinstance(skips, list)
    entry = {"stage": stage_id, "reason": reason, "decision_ref": decision_ref, "flow_mode": flow_mode}
    if entry not in skips:
        skips.append(entry)


def begin_stage(state: dict[str, object], skill: str, flow_mode: str, decision_ref: str = "", assumption: str = "", *, observed_on: date | None = None) -> tuple[list[str], list[str]]:
    """Mark a skill stage in progress after transition validation."""
    errors, warnings = validate_transition(state, skill, flow_mode, decision_ref, assumption)
    if errors:
        return errors, warnings
    stage = stage_for_skill(skill)
    row = stage_row(state, stage.stage_id)
    row["status"] = "in_progress"
    if decision_ref:
        row["decision_ref"] = decision_ref
    state["current_stage"] = stage.stage_id
    state["active_skill"] = skill
    state["flow_mode"] = flow_mode
    state["updated_at"] = (observed_on or date.today()).isoformat()
    if assumption:
        record_skip(state, stage.stage_id, assumption, decision_ref, flow_mode)
    return [], warnings


def complete_stage(
    state: dict[str, object],
    skill: str,
    artifacts: str = "",
    decision_ref: str = "",
    flow_mode: str = "default",
    assumption: str = "",
    *, observed_on: date | None = None,
) -> tuple[list[str], list[str]]:
    """Mark a skill stage done and store artifact/decision trace."""
    errors, warnings = validate_transition(state, skill, flow_mode, decision_ref, assumption)
    if errors:
        return errors, warnings
    stage = stage_for_skill(skill)
    row = stage_row(state, stage.stage_id)
    if row.get("status") != "in_progress" or state.get("active_skill") != skill:
        errors.append(f"stage must be begun before completion: {stage.stage_id}")
    if not artifacts:
        errors.append(f"completion artifact is required: {row.get('artifacts') or stage.artifacts}")
    if errors:
        return errors, warnings
    row["status"] = "done"
    if artifacts:
        row["artifacts"] = artifacts
    if decision_ref:
        row["decision_ref"] = decision_ref
    state["current_stage"] = stage.stage_id
    state["active_skill"] = ""
    state["flow_mode"] = flow_mode
    state["updated_at"] = (observed_on or date.today()).isoformat()
    if assumption:
        record_skip(state, stage.stage_id, assumption, decision_ref, flow_mode)
    return [], warnings


def completion_artifact_errors(
    state: dict[str, object], skill: str, artifacts: str, flow_mode: str, root: Path
) -> list[str]:
    """Require completion evidence at the canonical feature route."""
    if not artifacts:
        return ["--artifacts is required for stage completion"]
    if "," in artifacts:
        return ["--artifacts must name one canonical stage artifact"]
    stage = stage_for_skill(skill)
    feature = str(state.get("feature", ""))
    supplied = Path(artifacts)
    expected = Path(stage.artifacts.replace("<feature>", feature))
    if stage.stage_id == "sdd":
        canonical = Path("specs") / feature
    else:
        canonical = Path(workspace_base(stage.workspace)) / feature / expected.name
    normalized = supplied if supplied.is_absolute() else root / supplied
    expected_path = canonical if canonical.is_absolute() else root / canonical
    if normalized.resolve() != expected_path.resolve():
        return [f"completion artifact must use canonical path {canonical.as_posix()}: {artifacts}"]
    if not normalized.exists():
        return [f"completion artifact does not exist: {artifacts}"]

    finalized_statuses = {"review", "approved", "validated", "stable"}

    def finalized_markdown(path: Path) -> list[str]:
        if not path.is_file():
            return [f"completion evidence is not a file: {path.relative_to(root)}"]
        text = path.read_text(encoding="utf-8", errors="replace")
        label = path.relative_to(root).as_posix()
        if 'schema: "ai-sdlc-artifact-metadata/v1"' not in text:
            return [f"completion artifact lacks canonical metadata: {label}"]
        status_matches = re.findall(r'^\s*status:\s*["\']?([^"\'\n]+)', text, re.MULTILINE)
        if not any(status.strip() in finalized_statuses for status in status_matches):
            return [f"completion artifact is not finalized for review: {label}"]
        body = text.split("---", 2)[-1].strip() if text.startswith("---") else text.strip()
        if len(body) < 40 or not re.search(r"(?m)^#\s+\S", body):
            return [f"completion artifact has no meaningful review body: {label}"]
        return []

    if stage.stage_id == "sdd":
        if not normalized.is_dir():
            return [f"SDD completion artifact must be a directory: {artifacts}"]
        required = ("requirements.md", "design.md", "test-cases.md", "qa.md", "tasks.md")
        errors: list[str] = []
        for name in required:
            errors.extend(finalized_markdown(normalized / name))
        plan = normalized / "plan.md"
        machine_plan = normalized / "_ai_sdlc" / "plan.toon"
        if not plan.is_file() or not plan.read_text(encoding="utf-8", errors="replace").strip():
            errors.append(f"SDD completion evidence is missing plan projection: {plan.relative_to(root)}")
        if not machine_plan.is_file() or not machine_plan.read_text(encoding="utf-8", errors="replace").strip():
            errors.append(f"SDD completion evidence is missing machine plan: {machine_plan.relative_to(root)}")
        return errors

    if normalized.is_dir():
        return [f"completion artifact must be a file: {artifacts}"]
    errors = finalized_markdown(normalized)
    if errors:
        return errors
    text = normalized.read_text(encoding="utf-8", errors="replace")
    if stage.stage_id == "validation":
        receipt = normalized.parent / "_ai_sdlc" / "validation-receipt.toon"
        receipt_errors = validate_receipt(receipt, root)
        if receipt_errors:
            return [
                f"validation completion receipt is not current: {error}"
                for error in receipt_errors
            ]
    if stage.stage_id == "code_review" and "## Findings" not in text:
        return [f"code-review completion artifact must contain a Findings section: {artifacts}"]
    if stage.stage_id == "security_testing" and not any(
        heading in text for heading in ("## Findings", "## Threat", "## Security")
    ):
        return [f"security completion artifact must contain findings or threat analysis: {artifacts}"]
    return []


def add_state_arguments(parser: argparse.ArgumentParser) -> None:
    """Add common state-machine flags to a skill helper parser."""
    parser.add_argument("--state-check", action="store_true", help="Validate feature state before running this skill")
    parser.add_argument("--begin-state", action="store_true", help="Mark this skill stage in progress in state.toon")
    parser.add_argument("--complete-state", action="store_true", help="Mark this skill stage done in state.toon")
    parser.add_argument("--decision-ref", default="", help="Decision-log ID supporting this state transition")
    parser.add_argument("--assumption", default="", help="Quick-flow assumption allowing a skipped predecessor")
    parser.add_argument("--state-workspace", choices=["refinement", "implementation"], help="Override state workspace")


def run_state_action(args: argparse.Namespace, skill: str, workspace: str, artifacts: str = "") -> int:
    """Execute requested state-machine side effects for a skill helper."""
    if not (getattr(args, "state_check", False) or getattr(args, "begin_state", False) or getattr(args, "complete_state", False)):
        return 0
    feature = getattr(args, "feature", None)
    if not feature or feature == "<feature-name>":
        print("ERROR: --feature is required for state machine operations")
        return 1
    resolved_workspace = getattr(args, "state_workspace", None) or workspace
    path = state_path(feature, resolved_workspace)
    with write_lock(path.parent):
        read_path = first_existing(path, legacy_state_path(feature, resolved_workspace))
        if read_path.exists():
            state = load_state(read_path)
        elif getattr(args, "begin_state", False):
            state = initial_state(feature, resolved_workspace)
        else:
            print(f"STATE ERROR: authoritative state is missing: {path}")
            return 1
        flow = flow_mode_from_args(args)
        decision_ref = getattr(args, "decision_ref", "")
        assumption = getattr(args, "assumption", "")

        errors: list[str] = []
        warnings: list[str] = []
        if getattr(args, "begin_state", False):
            errors, warnings = begin_stage(state, skill, flow, decision_ref, assumption)
        elif getattr(args, "complete_state", False):
            errors = completion_artifact_errors(state, skill, artifacts, flow, Path.cwd())
            if not errors:
                errors, warnings = complete_stage(state, skill, artifacts, decision_ref, flow, assumption)
        else:
            errors, warnings = validate_transition(state, skill, flow, decision_ref, assumption)

        for warning in warnings:
            print(f"STATE WARN: {warning}")
        if errors:
            for error in errors:
                print(f"STATE ERROR: {error}")
            return 1
        if getattr(args, "begin_state", False) or getattr(args, "complete_state", False):
            save_state(path, state)
            print(f"STATE: updated {path}")
        else:
            print(f"STATE: ok {path}")
    return 0
