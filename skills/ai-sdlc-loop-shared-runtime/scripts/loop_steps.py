"""Read-only deterministic selection for Loop's existing compact stage graphs.

Semantic v2 graphs remain owned by ai_sdlc_steps. This module interprets only
the fixed Loop v1 manifest; it neither executes actions nor grants approvals.
"""

import hashlib
import re
from pathlib import Path

from toon import decode_toon, encode_toon
from ai_sdlc_step_context import execution_reference, chat_reference


def select_steps(skills_root: Path, skill: str, phase: str, completed=()):
    if skills_root.is_symlink() or not skills_root.is_dir():
        raise ValueError("STEP_UNKNOWN_SKILL: invalid skills root")
    if not re.fullmatch(r"ai-sdlc-loop-[a-z0-9-]+", skill):
        raise ValueError("STEP_UNKNOWN_SKILL: invalid Loop skill identity")
    directory = skills_root / skill
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("STEP_UNKNOWN_SKILL: missing regular skill directory")

    def read(relative):
        if not isinstance(relative, str) or not re.fullmatch(r"steps/[a-z0-9-]+\.(?:md|toon)", relative):
            raise ValueError("STEP_INVALID_MANIFEST: unsafe step path")
        path = directory / relative
        if path.parent.is_symlink() or path.is_symlink() or not path.is_file():
            raise ValueError("STEP_INVALID_MANIFEST: missing regular step file")
        return path.read_text(encoding="utf-8")

    manifest = decode_toon(read("steps/manifest.toon"))
    if (not isinstance(manifest, dict)
            or set(manifest) != {"schema", "skill", "entrypoints", "steps"}
            or manifest["schema"] != "ai-sdlc-loop-skill-steps/v1"
            or manifest["skill"] != skill):
        raise ValueError("STEP_INVALID_MANIFEST: expected matching Loop v1 graph")
    nodes = manifest["steps"]
    entries = manifest["entrypoints"]
    if not isinstance(nodes, list) or not nodes or not isinstance(entries, dict) or not entries:
        raise ValueError("STEP_INVALID_MANIFEST: missing nodes or entrypoints")
    by_id, dependencies, documents, references = {}, {}, {}, {}
    for node in nodes:
        if not isinstance(node, dict) or set(node) not in (
            {"id", "depends_on", "path", "side_effect"},
            {"id", "depends_on", "path", "side_effect", "owner"},
        ):
            raise ValueError("STEP_INVALID_MANIFEST: invalid node fields")
        identity = node["id"]
        if not isinstance(identity, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", identity) or identity in by_id:
            raise ValueError("STEP_INVALID_MANIFEST: duplicate or invalid node")
        if (not isinstance(node["side_effect"], str)
                or node["side_effect"] not in {"none", "state-write", "workspace-write", "command-execution", "git-commit"}):
            raise ValueError("STEP_INVALID_MANIFEST: unknown side effect")
        if "owner" in node and (not isinstance(node["owner"], str)
                or not re.fullmatch(r"ai-sdlc-loop-[a-z0-9-]+", node["owner"])
                or (skills_root / node["owner"]).is_symlink()
                or not (skills_root / node["owner"] / "SKILL.md").is_file()):
            raise ValueError("STEP_INVALID_MANIFEST: missing owning skill")
        if not isinstance(node["depends_on"], str):
            raise ValueError("STEP_INVALID_MANIFEST: depends_on must be a comma-separated string")
        deps = node["depends_on"].split(",") if node["depends_on"] else []
        if len(set(deps)) != len(deps):
            raise ValueError("STEP_INVALID_MANIFEST: duplicate dependency")
        if not isinstance(node["path"], str) or node["path"] in documents:
            raise ValueError("STEP_INVALID_MANIFEST: duplicate step path")
        document = read(node["path"])
        for reference in (execution_reference(directory, document), chat_reference(directory, document)):
            if reference:
                relative, content, _path = reference
                references[relative] = hashlib.sha256(content.encode()).hexdigest()
        if any(heading not in document for heading in ("## Entry", "## Procedure", "## Exit")):
            raise ValueError("STEP_INVALID_MANIFEST: incomplete step procedure")
        documents[node["path"]] = hashlib.sha256(document.encode()).hexdigest()
        by_id[identity], dependencies[identity] = node, set(deps)
    if any(deps - by_id.keys() for deps in dependencies.values()):
        raise ValueError("STEP_INVALID_MANIFEST: unknown dependency")
    order, pending = [], set(by_id)
    while pending:
        ready = sorted(key for key in pending if dependencies[key] <= set(order))
        if not ready:
            raise ValueError("STEP_INVALID_MANIFEST: cyclic dependencies")
        order.extend(ready)
        pending.difference_update(ready)
    if any(not isinstance(key, str) or not isinstance(target, str) or target not in by_id
           for key, target in entries.items()):
        raise ValueError("STEP_INVALID_MANIFEST: invalid entrypoint")

    def closure(targets):
        result, pending = set(), list(targets)
        while pending:
            key = pending.pop()
            if key not in result:
                result.add(key)
                pending.extend(dependencies[key])
        return result

    if closure(entries.values()) != set(by_id):
        raise ValueError("STEP_INVALID_MANIFEST: unreachable node")
    declared = {Path(path).name for path in documents}
    if {path.name for path in (directory / "steps").glob("*.md")} != declared:
        raise ValueError("STEP_INVALID_MANIFEST: undeclared step file")
    if phase not in entries:
        raise ValueError("STEP_UNKNOWN_PHASE: " + phase)
    completed = set(completed)
    if completed - by_id.keys():
        raise ValueError("STEP_UNKNOWN_COMPLETION: unknown completed node")
    if any(dependencies[key] - completed for key in completed):
        raise ValueError("STEP_INVALID_COMPLETION: incomplete predecessor evidence")
    selected = closure([entries[phase]])
    pending = [key for key in order if key in selected and key not in completed]
    ready = [key for key in pending if dependencies[key] <= completed]
    value = {
        "schema": "ai-sdlc-loop-step-selection/v1", "skill": skill, "phase": phase,
        "graph_fingerprint": hashlib.sha256(encode_toon({"manifest": manifest, "documents": documents, "references": references}).encode()).hexdigest(),
        "execution_order": [key for key in order if key in selected],
        "completed_steps": sorted(completed), "pending_steps": pending,
        "ready_steps": ready, "selected_paths": [by_id[key]["path"] for key in ready],
        "required_references": sorted(references),
        "complete": not pending, "authorizes_execution": False,
    }
    value["fingerprint"] = hashlib.sha256(encode_toon(value).encode()).hexdigest()
    return value
