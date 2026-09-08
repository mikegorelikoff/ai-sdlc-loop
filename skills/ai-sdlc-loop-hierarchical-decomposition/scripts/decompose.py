#!/usr/bin/env python3
"""Offline delivery-tree compiler: prepare, evaluate, render and verify.

Semantic candidates are data. This engine never invents children, executes
verification commands, grants approvals or writes to ticketing systems.
Exit 0: checked; 2: invalid input; 3: valid but blocked decomposition.
Writes require --output, are root-bounded, atomic and idempotent.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
PREFIX = "ai-sdlc-loop" if SKILL_ROOT.name.startswith("ai-sdlc-loop-") else "ai-sdlc"
sys.path.insert(0, str(SKILL_ROOT.parent / (PREFIX + "-shared-runtime") / "scripts"))
import ai_sdlc_toon as codec
from ai_sdlc_safe_io import atomic_write_text, bounded_path as _bounded_path

LEVELS = ("INITIATIVE", "EPIC", "FEATURE", "STORY", "TASK")
ROLES = ("Product", "Delivery", "Architecture", "QA")
AXES = ("business-capability", "user-journey", "workflow-stage", "domain", "lifecycle", "integration", "operational-outcome", "implementation-obligation", "UNKNOWN")
SCHEMA = "ai-sdlc-decomposition-candidate/v1"
REPORT = "ai-sdlc-decomposition/v1"
LIMIT = 2 * 1024 * 1024


class Invalid(ValueError):
    """Fail-closed input error with a field path."""


def bounded_path(root, path):
    result = _bounded_path(root, path)
    if ".git" in result.relative_to(root.resolve()).parts:
        raise Invalid("protected Git metadata path")
    return result


def normalize(value):
    if isinstance(value, dict):
        return {k: v if k == "sequence" else normalize(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        items = [normalize(v) for v in value]
        return sorted(items, key=lambda v: codec.dumps(v))
    return value


def encoded(value):
    return codec.dumps(normalize(value)).rstrip() + "\n"


def digest(value):
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()


def stable_id(scope, kind, key):
    return kind + "-" + digest(dict(scope=scope, kind=kind, key=key))[:16]


def shape(value, rule, path="candidate"):
    kind = rule["type"]
    if kind == "object":
        if not isinstance(value, dict) or set(value) != set(rule["properties"]):
            raise Invalid(path + ": expected exactly declared fields")
        for key, child in rule["properties"].items():
            shape(value[key], child, path + "." + key)
    elif kind == "array":
        if not isinstance(value, list) or not rule.get("minItems", 0) <= len(value) <= rule.get("maxItems", 300):
            raise Invalid(path + ": invalid array size")
        for i, child in enumerate(value):
            shape(child, rule["items"], f"{path}[{i}]")
        if len({encoded(x) for x in value}) != len(value):
            raise Invalid(path + ": duplicate entries")
    elif kind == "string":
        if not isinstance(value, str) or len(value) > rule.get("maxLength", 64000):
            raise Invalid(path + ": invalid text")
        if rule.get("minLength", 0) and not value.strip():
            raise Invalid(path + ": required text missing")
        if "enum" in rule and value not in rule["enum"]:
            raise Invalid(path + ": invalid enum")
        if "pattern" in rule and not re.fullmatch(rule["pattern"], value):
            raise Invalid(path + ": invalid identifier")
    elif kind == "boolean":
        if type(value) is not bool:
            raise Invalid(path + ": expected boolean")
    elif kind == "integer":
        if type(value) is not int or not rule["minimum"] <= value <= rule["maximum"]:
            raise Invalid(path + ": outside bounded iterations")
    else:
        raise Invalid(path + ": unsupported schema type")


def load(path):
    if path.stat().st_size > LIMIT:
        raise Invalid("artifact exceeds 2 MiB")
    return codec.loads(path.read_text(encoding="utf-8"))


def check_shape(candidate):
    contract = load(SKILL_ROOT / "references/decomposition.schema.toon")
    shape(candidate, contract["candidate"])


def index(rows, label):
    result = {row["key"]: row for row in rows}
    if len(result) != len(rows):
        raise Invalid(label + ": duplicate identity")
    return result


def content_fingerprint(candidate):
    return digest({k: v for k, v in candidate.items() if k not in ("reviews", "iteration")})


def context_closure(candidate, keys):
    """Close ancestry, incident dependencies and shared questions without children."""
    nodes = {n["key"]: n for n in candidate["nodes"]}
    result = set(keys)
    for _ in range(len(nodes) + 1):
        previous = set(result)
        result.update(nodes[k]["parent"] for k in previous if nodes[k]["parent"])
        for dep in candidate["dependencies"]:
            if result.intersection((dep["from"], dep["to"])):
                result.update((dep["from"], dep["to"]))
        for question in candidate["unknowns"]:
            if result.intersection(question["affected"]):
                result.update(question["affected"])
        if previous == result:
            return result
    raise Invalid("context closure exceeded node bound")


def branch_fingerprint(candidate, key):
    """Bind a review to its subtree, ancestors and incident obligations."""
    nodes = {n["key"]: n for n in candidate["nodes"]}
    relevant, pending = set(), [key]
    while pending:
        item = pending.pop()
        if item in relevant:
            continue
        relevant.add(item)
        pending.extend(n["key"] for n in nodes.values() if n["parent"] == item)
    relevant = context_closure(candidate, relevant)
    reqs = {r for k in relevant for r in nodes[k]["requirements"]}
    requirements = [r for r in candidate["requirements"] if r["key"] in reqs]
    source_keys = {r["source"] for r in requirements}
    source_keys.update(v for k in relevant for v in nodes[k]["priority_evidence"])
    source_keys.update(v for a in candidate["assumptions"] if any(a["key"] in nodes[k]["assumptions"] for k in relevant) for v in a["evidence"])
    source_keys.update(v for e in candidate["nfr_exclusions"] if e["node"] in relevant for v in e["evidence"])
    assumptions = {a for k in relevant for a in nodes[k]["assumptions"]}
    return digest(dict(scope=candidate["scope"], input_level=candidate["input_level"], target_level=candidate["target_level"],
        nodes=[nodes[k] for k in relevant], external_nodes=[nodes[k] for k in sorted({v for d in candidate["dependencies"] if d["from"] in relevant or d["to"] in relevant for v in (d["from"], d["to"])} - relevant)], requirements=requirements,
        sources=[s for s in candidate["sources"] if s["key"] in source_keys],
        assumptions=[a for a in candidate["assumptions"] if a["key"] in assumptions],
        unknowns=[u for u in candidate["unknowns"] if relevant.intersection(u["affected"])],
        acceptance=[a for a in candidate["acceptance_criteria"] if a["node"] in relevant],
        dependencies=[d for d in candidate["dependencies"] if d["from"] in relevant or d["to"] in relevant],
        exclusions=[e for e in candidate["nfr_exclusions"] if e["node"] in relevant]))


def evaluate(candidate):
    """Fixed gate order; semantic reviews cannot override mechanical defects."""
    check_shape(candidate)
    c = normalize(copy.deepcopy(candidate))
    nodes = index(c["nodes"], "nodes")
    reqs = index(c["requirements"], "requirements")
    sources = index(c["sources"], "sources")
    assumptions = index(c["assumptions"], "assumptions")
    unknowns = index(c["unknowns"], "unknowns")
    criteria = index(c["acceptance_criteria"], "acceptance_criteria")
    defects = []

    def defect(code, node, evidence, action, severity="HIGH"):
        defects.append(dict(code=code, node=node, severity=severity, evidence=evidence, action=action))

    def refs(values, known, field):
        if any(v not in known for v in values):
            raise Invalid(field + ": dangling reference")

    for source in sources.values():
        if hashlib.sha256(source["content"].encode("utf-8")).hexdigest() != source["sha256"]:
            raise Invalid("sources." + source["key"] + ": content digest mismatch")
    for req in reqs.values():
        refs([req["source"]], sources, "requirement.source")
        if req["quote"] not in sources[req["source"]]["content"]:
            defect("UNSUPPORTED_REQUIREMENT", "", req["key"], "Locate exact source evidence", "CRITICAL")
        if req["knowledge"] != "KNOWN":
            defect("UNRESOLVED_REQUIREMENT", "", req["key"], "Confirm interpretation with source owner")
    if not reqs:
        defect("MISSING_REQUIREMENTS", "", "No sourced requirements", "Extract supported requirements")

    roots = [n for n in nodes.values() if not n["parent"]]
    if len(roots) != 1:
        raise Invalid("nodes: exactly one root required")
    root = roots[0]
    if root["type"] != c["input_level"]:
        raise Invalid("input_level: disagrees with root")
    if LEVELS.index(c["target_level"]) < LEVELS.index(c["input_level"]):
        raise Invalid("target_level: precedes input")
    children = {k: [] for k in nodes}
    allowed = {"INITIATIVE": {"EPIC"}, "EPIC": {"FEATURE", "STORY"}, "FEATURE": {"STORY"}, "STORY": {"TASK"}, "TASK": set()}
    for key, node in nodes.items():
        if node["parent"]:
            refs([node["parent"]], nodes, "node.parent")
            if node["type"] not in allowed[nodes[node["parent"]]["type"]]:
                raise Invalid("nodes." + key + ": illegal hierarchy edge")
            children[node["parent"]].append(key)
        if LEVELS.index(node["type"]) > LEVELS.index(c["target_level"]):
            raise Invalid("nodes." + key + ": below configured stop level")
        refs(node["requirements"], reqs, "node.requirements")
        refs(node["assumptions"], assumptions, "node.assumptions")
        refs(node["priority_evidence"], sources, "node.priority_evidence")
        if node["delivery_slice"] != "UNKNOWN" and not node["priority_evidence"]:
            defect("UNSUPPORTED_PRIORITY", key, node["delivery_slice"], "Obtain sourced business priority")
        if not node["requirements"]:
            defect("UNSUPPORTED_SCOPE", key, "No parent requirement trace", "Remove unsupported scope or trace obligation", "CRITICAL")
        if node["parent"] and not set(node["requirements"]).issubset(nodes[node["parent"]]["requirements"]):
            defect("SCOPE_EXPANSION", key, "Trace escapes parent scope", "Repair affected parent/child mapping", "CRITICAL")
        if node["knowledge"] != "KNOWN":
            defect("UNCERTAIN_NODE", key, node["knowledge"], "Validate assumptions before handoff")
        if node["type"] in ("EPIC", "FEATURE") and node["title"].strip().lower() in {"frontend", "backend", "database", "ui", "api"}:
            defect("HORIZONTAL_SLICE", key, node["title"], "Describe a demonstrable delivery outcome")
        if node["technical_outcome"] and not node["technical_justification"]:
            defect("TECHNICAL_JUSTIFICATION", key, node["title"], "Cite meaningful technical delivery scope")
        if node["type"] == "TASK" and not node["implementation_obligation"]:
            defect("TASK_OBLIGATION", key, node["title"], "Explain how task satisfies parent behavior")
        if node["type"] == "STORY" and (not node["actor"] or not node["behavior"] or not node["verification"]):
            defect("STORY_CONTRACT", key, node["title"], "Supply actor, behavior and verification")

    def descendants(key):
        result, queue = set(), [key]
        while queue:
            current = queue.pop()
            if current in result:
                raise Invalid("hierarchy cycle")
            result.add(current)
            queue.extend(children[current])
        return result

    if descendants(root["key"]) != set(nodes):
        raise Invalid("disconnected hierarchy")
    unresolved = set()
    for key, node in nodes.items():
        if node["knowledge"] != "KNOWN":
            unresolved.update(descendants(key))
            if children[key]:
                defect("RECURSIVE_AMBIGUITY", key, node["knowledge"], "Resolve parent uncertainty before expansion", "CRITICAL")
    for item in unknowns.values():
        refs(item["affected"], nodes, "unknown.affected")
        if not item["blocking"]:
            defect("OPEN_QUESTION", item["affected"][0], item["question"], "Resolve optional question", "WARNING")
        if item["blocking"]:
            for key in item["affected"]:
                unresolved.update(descendants(key))
                defect("UNKNOWN_BLOCKS_BRANCH", key, item["question"], "Obtain cited owner decision")
                if children[key]:
                    defect("RECURSIVE_AMBIGUITY", key, item["key"], "Remove speculative descendants", "CRITICAL")
    for item in assumptions.values():
        refs(item["evidence"], sources, "assumption.evidence")
        if item["status"] == "VALIDATED" and (not item["evidence"] or item["validation_needed"]):
            raise Invalid("validated assumption needs evidence and resolved validation")
        for key, node in nodes.items():
            if item["key"] in node["assumptions"] and item["status"] != "VALIDATED":
                unresolved.update(descendants(key))
                defect("ASSUMPTION_PENDING", key, item["key"], item["validation"])
                if children[key]:
                    defect("RECURSIVE_AMBIGUITY", key, item["key"], "Resolve before recursive expansion", "CRITICAL")

    if set(root["requirements"]) != set(reqs):
        defect("ROOT_COVERAGE", root["key"], "Root omits sourced requirements", "Map all requirements or revise explicit scope")
    coverage = {}
    for key, node in nodes.items():
        child_reqs = {r for child in children[key] for r in nodes[child]["requirements"]}
        gaps = set(node["requirements"]) - child_reqs
        pending = node["type"] != c["target_level"] and not children[key]
        coverage[key] = "UNCERTAIN" if key in unresolved else "PARTIAL" if pending or (children[key] and gaps) else "COMPLETE"
        if coverage[key] == "PARTIAL":
            defect("PARENT_COVERAGE", key, ", ".join(sorted(gaps)), "Decompose only supported uncovered behavior")
        if children[key] and node["axis"] == "UNKNOWN":
            defect("AXIS_MISSING", key, node["title"], "Choose and justify an outcome-oriented axis")
        for a in children[key]:
            for b in children[key]:
                if a < b and nodes[a]["outcome"].casefold().strip() == nodes[b]["outcome"].casefold().strip():
                    defect("DUPLICATE_OUTCOME", key, a + ", " + b, "Merge duplicate outcomes")
        nfrs = {r for r in node["requirements"] if reqs[r]["kind"] == "NFR"}
        for child in children[key]:
            missing = nfrs - set(nodes[child]["requirements"])
            for req in missing:
                exclusions = [e for e in c["nfr_exclusions"] if e["requirement"] == req and e["node"] == child]
                if not exclusions:
                    defect("NFR_PROPAGATION", child, req, "Propagate or provide reviewed non-applicability evidence")
    for exclusion in c["nfr_exclusions"]:
        refs([exclusion["node"]], nodes, "nfr_exclusion.node")
        refs([exclusion["requirement"]], reqs, "nfr_exclusion.requirement")
        refs(exclusion["evidence"], sources, "nfr_exclusion.evidence")
        if reqs[exclusion["requirement"]]["kind"] != "NFR":
            raise Invalid("nfr exclusion must reference an NFR")

    for ac in criteria.values():
        refs([ac["node"]], nodes, "acceptance.node")
        refs(ac["requirements"], reqs, "acceptance.requirements")
        if not set(ac["requirements"]).issubset(nodes[ac["node"]]["requirements"]):
            defect("AC_SCOPE", ac["node"], ac["key"], "Remove unsupported acceptance behavior", "CRITICAL")
    for key, node in nodes.items():
        if node["type"] in ("STORY", "TASK"):
            covered = {r for ac in criteria.values() if ac["node"] == key for r in ac["requirements"]}
            if set(node["requirements"]) - covered:
                defect("AC_COVERAGE", key, "Missing verifiable acceptance mapping", "Add observable criteria and verification")

    edges = {key: set() for key in nodes}
    for dep in c["dependencies"]:
        refs([dep["from"], dep["to"]], nodes, "dependency")
        if dep["from"] == dep["to"]:
            raise Invalid("self dependency")
        if dep["type"] in ("BLOCKS", "ENABLES", "DEPENDS_ON"):
            a, b = (dep["to"], dep["from"]) if dep["type"] == "DEPENDS_ON" else (dep["from"], dep["to"])
            edges[a].add(b)
    incoming = {k: sum(k in targets for targets in edges.values()) for k in nodes}
    order = []
    while len(order) < len(nodes):
        ready = sorted(k for k in nodes if incoming[k] == 0 and k not in order)
        if not ready:
            defect("DEPENDENCY_CYCLE", "", "No valid topological ordering", "Remove cycle or model shared contract instead", "CRITICAL")
            break
        for key in ready:
            order.append(key)
            for target in edges[key]:
                incoming[target] -= 1

    fingerprint = content_fingerprint(c)
    review_keys = set()
    branch_fingerprints = {key: branch_fingerprint(c, key) for key in nodes}
    for review in c["reviews"]:
        refs([review["node"]], nodes, "review.node")
        identity = (review["node"], review["role"])
        if identity in review_keys:
            raise Invalid("duplicate review role for node")
        review_keys.add(identity)
        if review["candidate_fingerprint"] != branch_fingerprints[review["node"]]:
            defect("STALE_REVIEW", review["node"], review["role"], "Re-review current candidate")
        if review["verdict"] != "PASS":
            defect("SEMANTIC_" + review["role"].upper(), review["node"], review["evidence"], review["action"], "HIGH" if review["verdict"] == "UNKNOWN" else review["severity"])
        if review["role"] == "Delivery" and review["granularity"] != "CORRECT":
            defect("GRANULARITY", review["node"], review["granularity"], review["action"])
        if nodes[review["node"]]["type"] == "STORY" and review["role"] == "QA":
            investment = review["invest"]
            applicable = all(v == "PASS" for k, v in investment.items() if k != "Independent")
            independent = investment["Independent"] == "PASS" or (investment["Independent"] == "DEPENDENCY" and any(review["node"] in (d["from"], d["to"]) for d in c["dependencies"]))
            if not applicable or not independent:
                defect("INVEST", review["node"], review["evidence"], review["action"])
    for key in nodes:
        for role in ROLES:
            if (key, role) not in review_keys:
                defect("REVIEW_MISSING", key, role, "Obtain independent semantic review")
    defects = normalize(defects)
    blocking = [d for d in defects if d["severity"] in ("CRITICAL", "HIGH")]
    failed_nodes = {d["node"] for d in blocking}
    # A parent's own semantic uncertainty invalidates descendants, but an
    # unrelated blocked sibling does not make a reviewed branch speculative.
    blocked_nodes = set(unresolved)
    for d in blocking:
        if not d["node"]:
            blocked_nodes.update(nodes)
        elif d["code"] != "PARENT_COVERAGE":
            blocked_nodes.update(descendants(d["node"]))
        else:
            blocked_nodes.add(d["node"])
    for _ in range(len(nodes) + 1):
        previous = set(blocked_nodes)
        blocked_nodes.update(k for k in nodes if descendants(k) & blocked_nodes)
        for prerequisite, dependents in edges.items():
            if prerequisite in blocked_nodes:
                for dependent in dependents:
                    blocked_nodes.update(descendants(dependent))
        if previous == blocked_nodes:
            break
    status = "BLOCKED" if blocking else "WARNING" if defects else "PASS"
    result_nodes = []
    ids = {k: stable_id(c["scope"], n["type"], k) for k, n in nodes.items()}
    for key, node in nodes.items():
        result_nodes.append(dict(node, id=ids[key], parent_id=ids.get(node["parent"], ""), coverage=coverage[key], status="BLOCKED" if key in blocked_nodes else "PASS"))
    traceability = [dict(requirement=r, node=ids[k], source=reqs[r]["source"]) for k, n in nodes.items() for r in n["requirements"]]
    return normalize(dict(schema=REPORT, candidate=c, candidate_fingerprint=fingerprint, status=status,
        nodes=result_nodes, traceability=traceability, quality_report=defects,
        coverage="UNCERTAIN" if unresolved else "PARTIAL" if blocking else "COMPLETE",
        sequence=order if not any(d["code"] == "DEPENDENCY_CYCLE" for d in defects) else [],
        next_action="STOP_AND_REPORT" if blocking and c["iteration"] == 3 else "REPAIR_AFFECTED_BRANCHES" if blocking else "HANDOFF_REVIEWED_BRANCH",
        evaluation_metadata=dict(iteration=c["iteration"], max_iterations=3, semantic_basis="Independent reviewer assertions; structural validity is not factual verification")))


def verify_sources(root, candidate):
    for source in candidate["sources"]:
        path = bounded_path(root, Path(source["path"]))
        if not path.is_file() or path.stat().st_size > 256 * 1024:
            raise Invalid("source missing or oversized: " + source["path"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise Invalid("STALE_SOURCE: " + source["path"])


def table(headers, rows):
    def cell(value):
        return (str(value) if len(str(value)) <= 180 else "Full field in canonical artifact (" + str(len(str(value))) + " characters)").replace("&", "&amp;").replace("<", "&lt;").replace("|", "&#124;").replace("\r", " ").replace("\n", "<br>")
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"] + ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows])


def render(report):
    """Render the verified report; full detail stays in the canonical artifact."""
    if evaluate(report["candidate"]) != report:
        raise Invalid("report differs from recomputed result")
    c, nodes = report["candidate"], report["nodes"]
    counts = [(level.title() + "s", sum(n["type"] == level for n in nodes)) for level in LEVELS]
    sections = ["## Decomposition Summary\n\n" + table(["Metric", "Result"], [("Status", report["status"]), ("Input Level", c["input_level"]), ("Target Level", c["target_level"]), *counts, ("Unknowns", len(c["unknowns"])), ("Assumptions", len(c["assumptions"])), ("Coverage", report["coverage"])])]
    def preview(title, columns, rows):
        if rows:
            sections.append("## " + title + "\n\n" + table(columns, rows[:8]) + (f"\n\nShowing 8 of {len(rows)}; remaining records are in the canonical artifact." if len(rows) > 8 else ""))
    preview("Delivery Tree", ["ID", "Type", "Parent", "Title", "Outcome", "Status"], [[n["id"], n["type"], n["parent_id"], n["title"], n["outcome"], n["status"]] for n in sorted(nodes, key=lambda n: (n["status"] != "BLOCKED", LEVELS.index(n["type"]), n["key"]))])
    dependencies = {n["key"]: ", ".join(d["from"] + " " + d["type"] + " " + d["to"] for d in c["dependencies"] if n["key"] in (d["from"],d["to"])) for n in nodes}
    preview("Epics", ["ID", "Epic", "Outcome", "Why it exists", "Dependencies", "Coverage"], [[n["id"],n["title"],n["outcome"],", ".join(n["requirements"]),dependencies[n["key"]],n["coverage"]] for n in nodes if n["type"] == "EPIC"])
    preview("Features", ["ID", "Feature", "Parent", "Capability", "Dependencies", "Assumptions"], [[n["id"],n["title"],n["parent_id"],n["outcome"],dependencies[n["key"]],", ".join(n["assumptions"])] for n in nodes if n["type"] == "FEATURE"])
    preview("Stories", ["ID", "Story", "Parent", "Actor", "Outcome", "Dependencies"], [[n["id"],n["title"],n["parent_id"],n["actor"],n["outcome"],dependencies[n["key"]]] for n in nodes if n["type"] == "STORY"])
    preview("Tasks", ["ID", "Task", "Story", "Engineering outcome", "Dependencies", "Verification"], [[n["id"],n["title"],n["parent_id"],n["implementation_obligation"],dependencies[n["key"]],n["verification"]] for n in nodes if n["type"] == "TASK"])
    preview("INVEST", ["Story", "Criterion", "Assessment", "Evidence"], [[r["node"],k,v,r["evidence"]] for r in c["reviews"] if r["role"] == "QA" and any(n["key"] == r["node"] and n["type"] == "STORY" for n in nodes) for k,v in r["invest"].items()])
    preview("Dependencies", ["From", "Relationship", "To", "Reason"], [[d["from"],d["type"],d["to"],d["reason"]] for d in c["dependencies"]])
    preview("Delivery Order", ["Position", "Work item", "Slice", "Basis"], [[i+1,k,next(n["delivery_slice"] for n in nodes if n["key"]==k),"Dependency order; ties by stable key, business priority remains explicit"] for i,k in enumerate(report["sequence"])])
    preview("Requirement Traceability", ["Requirement", "Source", "Work item"], [[t["requirement"], t["source"], t["node"]] for t in report["traceability"]])
    preview("Acceptance Criteria / Verification", ["ID", "Work item", "Given", "When", "Then", "Verification"], [[a["key"], a["node"], a["given"], a["when"], a["then"], a["verification"]] for a in c["acceptance_criteria"]])
    preview("Assumptions & Unknowns", ["ID", "Type", "Description", "Impact", "Confidence", "Validation"], [[a["key"], "ASSUMED", a["description"], a["impact"], a["confidence"], a["validation"]] for a in c["assumptions"]] + [[u["key"], "UNKNOWN", u["question"], u["impact"], "UNKNOWN", u["question"]] for u in c["unknowns"]])
    preview("Quality Report", ["Check", "Status", "Work item", "Evidence", "Action"], [[d["code"], "BLOCKED" if d["severity"] in ("CRITICAL", "HIGH") else "WARNING", d["node"], d["evidence"], d["action"]] for d in report["quality_report"]] or [["All gates", "PASS", "tree", "Current mechanical checks and reviewer receipts", "Hand off reviewed branch"]])
    preview("Next Action", ["Owner", "Next action", "Required evidence"], [["Delivery owner", report["next_action"], report["candidate_fingerprint"]]])
    return "\n\n".join(sections) + "\n"


def prepare(root, source_path, scope, level, target):
    """Snapshot supplied bytes; never guess requirements or a decomposition."""
    root = root.resolve(strict=True)
    path = bounded_path(root, source_path)
    if path.stat().st_size > 64000:
        raise Invalid("source exceeds 64 KiB; supply a scoped evidence document")
    raw = path.read_bytes()
    content = raw.decode("utf-8")
    if not content.strip():
        raise Invalid("source is empty")
    node = dict(key="root", type=level, parent="", title="Unclassified supplied scope", outcome="UNKNOWN: source interpretation required", requirements=[], assumptions=[], knowledge="UNKNOWN", axis="UNKNOWN", actor="", behavior="", verification="", implementation_obligation="", technical_outcome=False, technical_justification="", delivery_slice="UNKNOWN", priority_evidence=[])
    candidate = dict(schema=SCHEMA, scope=scope, input_level=level, target_level=target, iteration=1,
        sources=[dict(key="source",path=path.relative_to(root).as_posix(),content=content,sha256=hashlib.sha256(raw).hexdigest())],
        requirements=[], nodes=[node], assumptions=[],
        unknowns=[dict(key="scope",question="Confirm source level, outcome and material missing decisions",impact="No safe child decomposition yet",blocking=True,affected=["root"])],
        acceptance_criteria=[],dependencies=[],nfr_exclusions=[],reviews=[])
    check_shape(candidate)
    if LEVELS.index(target) < LEVELS.index(level):
        raise Invalid("target level precedes input level")
    return candidate


def handoff(report, node_key):
    """A trace-complete branch packet; never an execution approval or ticket write."""
    if evaluate(report["candidate"]) != report:
        raise Invalid("stale or modified report")
    by_key = {n["key"]: n for n in report["nodes"]}
    if node_key not in by_key or by_key[node_key]["status"] != "PASS":
        raise Invalid("HANDOFF_BLOCKED: select a reviewed passing branch")
    selected, queue = set(), [node_key]
    while queue:
        key = queue.pop(); selected.add(key)
        queue.extend(n["key"] for n in by_key.values() if n["parent"] == key)
    c = report["candidate"]
    ancestors = set()
    parent = by_key[node_key]["parent"]
    while parent:
        ancestors.add(parent)
        parent = by_key[parent]["parent"]
    context_keys = context_closure(c, selected | ancestors)
    external_keys = context_keys - selected - ancestors
    required = {r for k in context_keys for r in by_key[k]["requirements"]}
    requirements = [r for r in c["requirements"] if r["key"] in required]
    source_keys = {r["source"] for r in requirements}
    assumption_keys = {a for k in context_keys for a in by_key[k]["assumptions"]}
    source_keys.update(v for k in context_keys for v in by_key[k]["priority_evidence"])
    source_keys.update(v for a in c["assumptions"] if a["key"] in assumption_keys for v in a["evidence"])
    source_keys.update(v for e in c["nfr_exclusions"] if e["node"] in context_keys for v in e["evidence"])
    packet = normalize(dict(schema="ai-sdlc-decomposition-handoff/v1",authorizes_execution=False,global_status=report["status"],
        candidate_fingerprint=report["candidate_fingerprint"],branch=node_key,
        nodes=[by_key[k] for k in selected], ancestors=[by_key[k] for k in ancestors], requirements=requirements,
        nfr_exclusions=[e for e in c["nfr_exclusions"] if e["node"] in context_keys],
        sources=[s for s in c["sources"] if s["key"] in source_keys],
        assumptions=[a for a in c["assumptions"] if a["key"] in assumption_keys],
        unknowns=[u for u in c["unknowns"] if context_keys.intersection(u["affected"])],
        acceptance_criteria=[a for a in c["acceptance_criteria"] if a["node"] in context_keys],
        dependencies=[d for d in c["dependencies"] if d["from"] in context_keys or d["to"] in context_keys],
        external_nodes=[by_key[k] for k in external_keys],
        next_required="Owning readiness/SDD approval and repository planning gates"))
    validate_handoff(packet)
    return packet


def validate_handoff(packet):
    """Ensure every exported trace resolves without reconstructing conversation."""
    nodes = {n["key"] for section in ("nodes", "ancestors", "external_nodes") for n in packet[section]}
    sources = {s["key"] for s in packet["sources"]}
    requirements = {r["key"] for r in packet["requirements"]}
    assumptions = {a["key"] for a in packet["assumptions"]}
    def require(values, known):
        if not set(values).issubset(known):
            raise Invalid("HANDOFF_INVALID: dangling exported reference")
    for section in ("nodes", "ancestors", "external_nodes"):
        for n in packet[section]:
            require([n["parent"]] if n["parent"] else [], nodes)
            require(n["requirements"], requirements); require(n["assumptions"], assumptions)
            require(n["priority_evidence"], sources)
    for r in packet["requirements"]:require([r["source"]], sources)
    for a in packet["assumptions"]:require(a["evidence"], sources)
    for q in packet["unknowns"]:require(q["affected"], nodes)
    for d in packet["dependencies"]:require([d["from"],d["to"]], nodes)
    for a in packet["acceptance_criteria"]:
        require([a["node"]], nodes); require(a["requirements"], requirements)
    for e in packet["nfr_exclusions"]:
        require([e["node"]], nodes); require([e["requirement"]], requirements); require(e["evidence"], sources)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "evaluate", "render", "verify", "fingerprint", "handoff", "verify-handoff"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scope")
    parser.add_argument("--input-level", choices=LEVELS)
    parser.add_argument("--target-level", choices=LEVELS, default="STORY")
    parser.add_argument("--node")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    args = parser.parse_args()
    try:
        if args.quick_flow and args.full_flow:
            raise Invalid("conflicting flow flags")
        root = args.root.resolve(strict=True)
        if args.output:
            expected = ".md" if args.command == "render" else ".toon"
            if args.output.suffix != expected:
                raise Invalid("output requires " + expected + " native artifact extension")
            bounded_path(root, args.output)
        if args.command == "prepare":
            if not args.scope or not args.input_level:
                raise Invalid("prepare requires explicit --scope and semantically classified --input-level")
            candidate = prepare(root, args.input, args.scope, args.input_level, args.target_level)
            output = encoded(candidate)
            if args.output:
                if bounded_path(root, args.output) == bounded_path(root, args.input):
                    raise Invalid("output may not overwrite source")
                atomic_write_text(root, args.output, output)
            else:
                print(output, end="")
            return 0
        if args.command == "verify-handoff":
            if not args.report or args.output:
                raise Invalid("verify-handoff requires --report and is read-only")
            packet = load(bounded_path(root, args.input))
            report = load(bounded_path(root, args.report))
            verify_sources(root, report["candidate"])
            expected = handoff(report, packet["branch"])
            if packet != expected:
                raise Invalid("HANDOFF_INVALID: packet differs from current reviewed branch")
            print(encoded(dict(schema="ai-sdlc-decomposition-handoff-check/v1",status="PASS",candidate_fingerprint=report["candidate_fingerprint"],authorizes_execution=False)),end="")
            return 0
        value = load(bounded_path(root, args.input))
        candidate = value["candidate"] if args.command in ("render", "verify", "handoff") else value
        check_shape(candidate)
        verify_sources(root, candidate)
        report = evaluate(candidate)
        if args.command in ("render", "verify", "handoff") and value != report:
            raise Invalid("ARTIFACT_INVALID: report differs from deterministic recomputation")
        output = render(report) if args.command == "render" else encoded(dict(fingerprint=content_fingerprint(candidate),branches={n["key"]:branch_fingerprint(candidate,n["key"]) for n in candidate["nodes"]})) if args.command == "fingerprint" else encoded(report)
        if args.command == "handoff":
            output = encoded(handoff(report, args.node))
        if len(output.encode("utf-8")) > LIMIT:
            raise Invalid("output exceeds bounded artifact size; split explicit scope")
        if args.command == "evaluate" and args.output:
            previous_path = bounded_path(root, args.output)
            if previous_path.exists():
                previous = load(previous_path)
                if previous.get("schema") != REPORT or evaluate(previous["candidate"]) != previous:
                    raise Invalid("existing output is not an authentic decomposition report")
                if previous["candidate"]["scope"] != candidate["scope"]:
                    raise Invalid("scope changed; choose a separate run artifact")
                changed = previous["candidate_fingerprint"] != report["candidate_fingerprint"]
                expected_iteration = previous["candidate"]["iteration"] + int(changed)
                if candidate["iteration"] != expected_iteration:
                    raise Invalid("repair must advance exactly one iteration; reruns preserve the iteration")
            elif candidate["iteration"] != 1:
                raise Invalid("a durable run starts at iteration 1")
        if args.output:
            if bounded_path(root, args.output) == bounded_path(root, args.input) or any(bounded_path(root, args.output) == bounded_path(root, Path(s["path"])) for s in candidate["sources"]):
                raise Invalid("output may not overwrite input or source")
            atomic_write_text(root, args.output, output)
        else:
            print(output, end="")
        return 3 if report["status"] == "BLOCKED" and args.command not in ("fingerprint", "handoff") else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(encoded(dict(schema="ai-sdlc-decomposition-error/v1", code="INVALID_INPUT", message=str(exc), action="Repair the named field; preserve the previous artifact")), end="")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
