#!/usr/bin/env python3
"""Read-only framework diagnosis. No candidate code execution or network access.

Explicit root; stdout only. Exit 0 healthy, 2 diagnosed non-healthy, 1 invalid
invocation. Stable SHA-256 identities exclude clock, cwd and execution order.
The installed sibling runtime is trusted; the inspected tree is data only.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = HERE.parent.name[:-len("doctor")]
RUNTIME = HERE.parents[1] / (PREFIX + "shared-runtime") / "scripts"
sys.path.insert(0, str(RUNTIME))
sys.dont_write_bytecode = True
from ai_sdlc_toon import decode_toon, encode_toon

SCHEMA = "ai-sdlc-framework-diagnostics/v1"

@dataclass(frozen=True)
class Check:
    id: str
    layer: str
    code: str
    route: str
    severity: str = "HIGH"

# Policy is deliberately separate from check implementation.
REGISTRY = {item.id: item for item in (
    Check("DOC-ENV-001", "ENVIRONMENT", "DEPENDENCY_UNAVAILABLE", "ENVIRONMENT", "CRITICAL"),
    Check("DOC-REPO-001", "REPOSITORY", "REPOSITORY_UNAVAILABLE", "ENVIRONMENT", "CRITICAL"),
    Check("DOC-REG-001", "REPOSITORY", "REGISTRY_INVALID", "SKILL_CONTRACT"),
    Check("DOC-REG-002", "REPOSITORY", "INVENTORY_DRIFT", "SKILL_CONTRACT"),
    Check("DOC-SKILL-001", "SKILL", "MISSING_SKILL", "SKILL_CONTRACT"),
    Check("DOC-SKILL-002", "CONTRACTS", "CHAT_CONTRACT_INVALID", "SKILL_CONTRACT"),
    Check("DOC-PY-002", "PYTHON", "LOCAL_IMPORT_MISSING", "PYTHON"),
    Check("DOC-LINK-001", "CONTRACTS", "MISSING_SCRIPT", "PYTHON"),
    Check("DOC-PY-001", "PYTHON", "PYTHON_SYNTAX_FAILED", "PYTHON"),
    Check("DOC-TOON-001", "TOON", "TOON_PARSE_FAILED", "TOON"),
    Check("DOC-TOON-002", "TOON", "TOON_ROUNDTRIP_FAILED", "TOON"),
    Check("DOC-HUNTER-001", "HANDOFFS", "HUNTER_CONTRACT_INVALID", "SCHEMA"),
    Check("DOC-HUNTER-002", "EVALS", "HUNTER_GATE_FAILED", "EVAL"),
    Check("DOC-ROUTE-001", "ROUTING", "ROUTE_TARGET_MISSING", "ROUTING"),
    Check("DOC-HANDOFF-001", "HANDOFFS", "HANDOFF_INVALID", "SCHEMA"),
    Check("DOC-CHAT-001", "EVALS", "CHAT_EVAL_FAILED", "EVAL"),
    Check("DOC-GRAPH-001", "ROUTING", "STEP_GRAPH_INVALID", "ROUTING"),
    Check("DOC-TEST-001", "TESTS", "TEST_COVERAGE_MISSING", "TEST", "MEDIUM"),
    Check("DOC-EVAL-001", "EVALS", "CHAT_EVAL_MISSING", "EVAL", "MEDIUM"),
    Check("DOC-EVAL-002", "EVALS", "EXECUTION_EVAL_FAILED", "EVAL"),
    Check("DOC-OKF-001", "OKF", "OKF_INVALID", "OKF"),
    Check("DOC-STATE-001", "STATE", "STATE_INVALID", "ROUTING"),
    Check("DOC-STATE-002", "STATE", "TRANSITION_SIMULATION_FAILED", "ROUTING"),
    Check("DOC-DET-001", "DETERMINISM", "ARTIFACT_VARIANCE", "PYTHON"),
    Check("DOC-SCOPE-001", "COVERAGE", "CHECK_NOT_EXECUTED", "TEST", "MEDIUM"),
)}
STATUSES = {"PASS", "FAIL", "BLOCKED", "UNKNOWN", "N/A"}


def stable_id(check_id, component):
    return "DOC-" + hashlib.sha256((check_id + "\0" + component).encode("utf-8")).hexdigest()[:20]


def health(checks):
    if any(c["status"] == "BLOCKED" and c["severity"] == "CRITICAL" for c in checks):
        return "BLOCKED"
    if any(c["status"] == "FAIL" and c["severity"] in {"HIGH", "CRITICAL"} for c in checks):
        return "UNHEALTHY"
    if any(c["status"] in {"FAIL", "BLOCKED", "UNKNOWN"} for c in checks):
        return "DEGRADED"
    return "HEALTHY"


def regular(root, relative):
    path = root / relative
    path.relative_to(root)
    if path.is_absolute() and (".." in Path(relative).parts or Path(relative).is_absolute()):
        raise ValueError("unsafe relative path")
    for part in (path, *path.parents):
        if part == root.parent:
            break
        if part.is_symlink():
            raise ValueError("symlink is outside the diagnostic file contract")
    if not path.is_file() or path.stat().st_size > 4_000_000:
        raise ValueError("missing regular file or file exceeds 4 MB limit")
    return path


def load(root, relative):
    return decode_toon(regular(root, relative).read_text(encoding="utf-8"))


def inventory(root):
    if PREFIX == "ai-sdlc-loop-":
        tree = ast.parse(regular(root, "install.py").read_text(encoding="utf-8"))
        values = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "SKILLS" for t in n.targets)]
        if len(values) != 1:
            raise ValueError("exactly one installer SKILLS declaration required")
        names = list(values[0])
    else:
        names = []
        paths = sorted((root / "modules").glob("*/module.toon"))
        for path in paths:
            value = load(root, path.relative_to(root))
            if value.get("schema") != "ai-sdlc-module/v1":
                raise ValueError("invalid module contract")
            for row in value["skills"]:
                if row["path"] != "skills/" + row["name"]:
                    raise ValueError("module skill path does not match identity")
                names.append(row["name"])
    if not names or any(not isinstance(n, str) or not n.startswith(PREFIX) or "/" in n or ".." in n for n in names):
        raise ValueError("invalid registered skill identities")
    if len(names) != len(set(names)):
        raise ValueError("duplicate registered skill identity")
    return sorted(names)


def diagnose(root, mode="quick", target=None, artifacts=()):
    checks = []

    def add(key, component, status, evidence, depends=()):
        policy = REGISTRY[key]
        blocked_by = sorted(c["id"] for c in depends if c["status"] not in {"PASS", "N/A"})
        if blocked_by:
            status, evidence = "BLOCKED", "Prerequisite check did not pass"
        value = dict(id=stable_id(key, component), check_id=key, component=component,
                     layer=policy.layer, code=policy.code if status not in {"PASS", "N/A"} else "",
                     status=status, severity=policy.severity, repair_route=policy.route,
                     evidence=str(evidence), blocked_by=blocked_by)
        checks.append(value)
        return value

    def run(key, component, function, depends=()):
        if any(c["status"] not in {"PASS", "N/A"} for c in depends):
            return add(key, component, "BLOCKED", "", depends)
        try:
            evidence = function()
            return add(key, component, "PASS", evidence or "validated", depends)
        except (OSError, ValueError, TypeError, KeyError, AttributeError, ImportError, SyntaxError, AssertionError, RuntimeError) as exc:
            # No raw file contents/environment values in diagnostics.
            return add(key, component, "FAIL", type(exc).__name__ + ": " + str(exc).replace(str(root), "<root>"), depends)

    add("DOC-ENV-001", "python", "PASS" if sys.version_info >= (3, 9) else "BLOCKED", "Python >= 3.9 required")
    repo = add("DOC-REPO-001", ".", "PASS" if root.is_dir() and not root.is_symlink() and (root / "skills").is_dir() and not (root / "skills").is_symlink() else "BLOCKED", "regular repository and skills/ required")
    names = []
    def registry():
        names.extend(inventory(root))
        return str(len(names)) + " registered skills"
    reg = run("DOC-REG-001", "registry", registry, [repo])
    actual = sorted(p.name for p in (root / "skills").glob(PREFIX + "*") if p.is_dir()) if repo["status"] == "PASS" else []
    run("DOC-REG-002", "skills", lambda: require(actual == names, "missing=" + str(sorted(set(names)-set(actual))) + ";unregistered=" + str(sorted(set(actual)-set(names)))), [reg])
    if PREFIX + "flow" in names:
        def routes():
            if PREFIX == "ai-sdlc-loop-":
                path = "skills/" + PREFIX + "flow/scripts/flow.py"
                tree = ast.parse(regular(root, path).read_text(encoding="utf-8"))
                values = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ROUTES" for t in n.targets)]
                require(len(values) == 1, "missing declarative ROUTES")
                owners = [row[2] for row in values[0]]
            else:
                owners = [row["skill"] for row in load(root, "skills/ai-sdlc-flow/references/selector-registry.toon")["actions"]]
            for owner in sorted(set(owners)):
                require(owner in names, "unregistered route target: " + owner)
                regular(root, "skills/" + owner + "/SKILL.md")
            return str(len(owners)) + " selector targets resolve; utilities retain direct entrypoints"
        run("DOC-ROUTE-001", "flow-selectors", routes, [reg])
    if target and target not in names:
        add("DOC-SKILL-001", target, "FAIL", "target is not registered")
    selected = [n for n in sorted(set(names) | set(actual)) if not target or n in {target, PREFIX + "shared-runtime", PREFIX + "doctor"}]
    for name in selected:
        relative = "skills/" + name
        skill = root / relative
        present = run("DOC-SKILL-001", name, lambda r=relative: str(regular(root, r + "/SKILL.md").relative_to(root)), [reg])
        def chat(s=skill):
            import chat_output
            chat_output.contract(s)
            text = (s / "SKILL.md").read_text(encoding="utf-8")
            require("## Chat Output Contract" in text and "## Deterministic Execution Contract" in text, "missing execution or chat contract")
            return "native chat contract and execution boundary validated"
        chat_check = run("DOC-SKILL-002", name, chat, [present])
        def graph(n=name):
            manifest = load(root, "skills/" + n + "/steps/manifest.toon")
            if manifest.get("schema") == "ai-sdlc-loop-skill-steps/v1" and PREFIX == "ai-sdlc-loop-":
                from loop_steps import select_steps
                select_steps(root / "skills", n, sorted(manifest["entrypoints"])[0])
            else:
                from ai_sdlc_steps import load_manifest
                load_manifest(root, n)
            return "native graph validator: paths, dependencies, reachability, contracts"
        def script_links(s=skill):
            text = regular(root, s.relative_to(root) / "SKILL.md").read_text(encoding="utf-8")
            links = re.findall(r"\]\((scripts/[^)#]+\.py)(?:#[^)]*)?\)", text)
            for link in sorted(set(links)):
                regular(root, s.relative_to(root) / link)
            return str(len(set(links))) + " explicit script references resolved"
        run("DOC-LINK-001", name, script_links, [present])
        graph_check = run("DOC-GRAPH-001", name, graph, [present])
        # Only framework scripts and native contract files, never project source or caches.
        for path in sorted(skill.rglob("*.py")):
            if "tests" in path.relative_to(skill).parts or "__pycache__" in path.parts:
                continue
            rel = path.relative_to(root).as_posix()
            parsed_py = run("DOC-PY-001", rel, lambda r=rel: syntax(root, r), [present])
            run("DOC-PY-002", rel, lambda r=rel: local_imports(root, r), [parsed_py])
        for path in sorted(skill.rglob("*.toon")):
            if "tests" in path.relative_to(skill).parts or "fixtures" in path.relative_to(skill).parts:
                continue  # intentional invalid test inputs are not production defects
            rel = path.relative_to(root).as_posix()
            parsed = run("DOC-TOON-001", rel, lambda r=rel: parse_check(root, r), [present])
            run("DOC-TOON-002", rel, lambda r=rel: roundtrip(load(root, r)), [parsed])
        tests = list((skill / "tests").glob("test*.py"))
        # Loop compact stages use centrally registered regression suites.
        central = (root / "tests").is_dir() if PREFIX == "ai-sdlc-loop-" else False
        add("DOC-TEST-001", name, "PASS" if tests or central else "UNKNOWN", "local tests present" if tests else "central test suite present; semantic coverage not inferred" if central else "no local test suite; coverage needs owner evidence", [present])
        fixture = skill / "tests/fixtures/chat-scenarios.toon"
        eval_check = run("DOC-EVAL-001", name, lambda f=fixture: parse_check(root, f.relative_to(root)), [present])
        if mode != "quick":
            def chat_scenarios(s=skill):
                import chat_output as chat
                contract = chat.contract(s)
                suite = load(root, s.relative_to(root) / "tests/fixtures/chat-scenarios.toon")
                require(suite.get("skill") == s.name and {c["id"] for c in suite["scenarios"]} == set(chat.SCENARIOS), "chat scenario inventory mismatch")
                for case in suite["scenarios"]:
                    output = chat.render(contract, case["result"])
                    result = chat.evaluate(contract, output, required_facts=case["required_facts"], expected_status=case["result"]["summary"]["Status"])
                    require(result["status"] == "PASS", case["id"] + ": " + str(result["failures"]))
                    require(chat.render(contract, case["result"]) == output, "chat rendering variance")
                return "eight native chat scenarios rendered, evaluated and repeated"
            run("DOC-CHAT-001", name, chat_scenarios, [chat_check, eval_check])
            def evaluate(n=name):
                # The selector can warm an installed context cache. A minimal
                # isolated source fixture prevents any candidate code execution.
                with tempfile.TemporaryDirectory(prefix="doctor-eval-") as directory:
                    fixture = Path(directory)
                    sources = set((root / "skills" / n).rglob("*"))
                    sources.update((root / "skills" / (PREFIX + "shared-runtime") / "references").rglob("*"))
                    for source in sorted(sources):
                        if source.is_file() and "__pycache__" not in source.parts:
                            relative = source.relative_to(root)
                            regular(root, relative)
                            destination = fixture / relative
                            destination.parent.mkdir(parents=True, exist_ok=True)
                            destination.write_bytes(source.read_bytes())
                    for owner in names:
                        destination = fixture / "skills" / owner / "SKILL.md"
                        if not destination.exists():
                            destination.parent.mkdir(parents=True, exist_ok=True)
                            destination.write_text("Owner presence fixture\n", encoding="utf-8")
                    m = load(fixture, "skills/" + n + "/steps/manifest.toon")
                    if m.get("schema") == "ai-sdlc-loop-skill-steps/v1":
                        from loop_steps import select_steps
                        for phase in sorted(m["entrypoints"]):
                            selection = select_steps(fixture / "skills", n, phase)
                            terminal = select_steps(fixture / "skills", n, phase, selection["execution_order"])
                            require(terminal["complete"], "synthetic lifecycle failed to reach terminal state")
                        return "compact lifecycle selection and terminal replay passed"
                    from ai_sdlc_skill_eval import evaluate_skill
                    result = evaluate_skill(fixture, n)
                    require(result["failed"] == 0, "; ".join(str(c).replace(str(fixture), "<fixture>") for c in result["scenarios"] if c["status"] == "failed") if "scenarios" in result else "native execution scenario failed")
                    return str(result["passed"]) + " native execution scenarios passed in isolated fixture"
            run("DOC-EVAL-002", name, evaluate, [graph_check])

    for kind, relative in artifacts:
        def artifact(k=kind, r=relative):
            if k == "toon":
                return roundtrip(load(root, r))
            if k == "decomposition":
                engine = trusted_skill("hierarchical-decomposition", "decompose")
                report = load(root, r)
                engine.check_shape(report["candidate"])
                engine.verify_sources(root, report["candidate"])
                require(engine.evaluate(report["candidate"]) == report, "decomposition report differs from recomputed evidence")
                return "schema, source fingerprints, coverage and references validated"
            if k == "handoff":
                packet_path, report_path = r.split("@", 1)
                engine = trusted_skill("hierarchical-decomposition", "decompose")
                packet, report = load(root, packet_path), load(root, report_path)
                engine.verify_sources(root, report["candidate"])
                require(engine.handoff(report, packet["branch"]) == packet, "handoff differs from current producer report")
                return "producer report, source freshness and exported references validated"
            if k == "loop-state":
                require(PREFIX == "ai-sdlc-loop-", "Loop state requires Loop doctor")
                flow = trusted_skill("flow", "flow")
                feature = r
                require(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", feature), "invalid Loop feature")
                state, _ = flow.lifecycle_state(root, feature)
                require(state != "not-started", "Loop state missing")
                from loop import current_spec
                spec = current_spec(root, feature)
                data = load(root, ".ai-sdlc-loop/" + feature + "/state.toon")
                require(data.get("spec_fingerprint") == spec["fingerprint"], "state/spec fingerprint drift")
                return "native Loop stage and spec fingerprint valid; approval is not inferred"
            if k == "state":
                from ai_sdlc_state_machine import from_toon
                from_toon(regular(root, r).read_text(encoding="utf-8"))
                return "native Backbone lifecycle state shape valid; history not reconstructed"
            from ai_sdlc_okf import validate_bundle
            path = root / r
            require(not Path(r).is_absolute() and ".." not in Path(r).parts and path.is_dir(), "invalid bundle path")
            for member in sorted(path.rglob("*")):
                require(not member.is_symlink(), "symlink in OKF bundle")
            for parent in (path, *path.parents):
                if parent == root.parent:
                    break
                require(not parent.is_symlink(), "symlink OKF bundle ancestor")
            errors = validate_bundle(path)
            require(not errors, "; ".join(errors))
            return "native OKF v0.2 provenance validated"
        run({"toon":"DOC-TOON-002", "state":"DOC-STATE-001", "loop-state":"DOC-STATE-001", "decomposition":"DOC-HANDOFF-001", "handoff":"DOC-HANDOFF-001", "okf":"DOC-OKF-001"}[kind], relative, artifact, [repo])
    if mode != "quick":
        run("DOC-STATE-002", "native-state-simulation", state_simulation, [repo])
    if mode == "deep":
        first = diagnose(root, "standard", target, artifacts)
        second = diagnose(root, "standard", target, artifacts)
        add("DOC-DET-001", "repeated-standard-diagnostics", "PASS" if encode_toon(first) == encode_toon(second) else "FAIL", "two complete standard runs compared byte-for-byte")
    add("DOC-SCOPE-001", "application-tests", "N/A", "arbitrary project tests and imports never executed; use authorized validation skill")
    hunter_names = {PREFIX + kind for kind in ("edge-case-hunter", "blind-case-hunter", "bug-hunter")}
    if hunter_names & set(names):
        def hunter_contract():
            require(hunter_names <= set(names), "incomplete hunter family registration")
            from ai_sdlc_hunters import CONTRACT
            actual = load(root, "skills/" + PREFIX + "shared-runtime/references/hunters.schema.toon")
            require(actual == CONTRACT, "hunter shared schema drift")
            for name in sorted(hunter_names):
                regular(root, "skills/" + name + "/scripts/hunt.py")
                require(load(root, "skills/" + name + "/references/chat-output.toon")["skill"] == name, "hunter output identity drift")
            return "three hunters share current schema, evidence enums, entrypoints and output contracts"
        check_hunters = run("DOC-HUNTER-001", "hunter-family", hunter_contract, [reg])
        if mode != "quick":
            def hunter_eval():
                from ai_sdlc_hunters import self_check
                return self_check()
            run("DOC-HUNTER-002", "hunter-family", hunter_eval, [check_hunters])
    else:
        add("DOC-SCOPE-001", "hunter-integration", "N/A", "no hunter package registered")
    checks.sort(key=lambda c: (c["check_id"], c["component"]))
    findings = [dict(c, root_cause="Observed contract failure; deeper causal attribution requires evidence") for c in checks if c["status"] in {"FAIL", "UNKNOWN"} or (c["status"] == "BLOCKED" and not c["blocked_by"])]
    findings.sort(key=lambda c: ({"CRITICAL":0,"HIGH":1,"MEDIUM":2}[c["severity"]], c["layer"], c["component"], c["check_id"]))
    result = dict(schema=SCHEMA, execution="PASS", health=health(checks), mode=mode, target=target or "all", checks=checks, findings=findings,
                  limits=["No arbitrary script imports or tests", "TOON round-trip is not arbitrary artifact schema validation", "No inference of cross-artifact semantic compatibility", "State simulation uses Backbone lifecycle, not Loop approval state"])
    result["fingerprint"] = hashlib.sha256(encode_toon(result).encode("utf-8")).hexdigest()
    validate_report(result)
    return result


def trusted_skill(skill, module):
    # Load only the doctor package's sibling implementation, never root data.
    path = HERE.parents[1] / (PREFIX + skill) / "scripts" / (module + ".py")
    name = "doctor_adapter_" + PREFIX.replace("-", "_") + skill.replace("-", "_")
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        require(spec is not None and spec.loader is not None, "required installed adapter missing")
        loaded = importlib.util.module_from_spec(spec)
        sys.modules[name] = loaded
        try:
            spec.loader.exec_module(loaded)
        except Exception:
            del sys.modules[name]
            raise
    return sys.modules[name]


def require(condition, message):
    if not condition:
        raise ValueError(message)
    return "validated"


def local_imports(root, relative):
    tree = ast.parse(regular(root, relative).read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    # Only repository-owned absolute imports have a mechanically known owner.
    required = sorted(n for n in names if n.startswith("ai_sdlc_"))
    for name in required:
        candidates = [(root / relative).parent / (name + ".py"), root / "skills" / (PREFIX + "shared-runtime") / "scripts" / (name + ".py")]
        require(any(p.is_file() and not p.is_symlink() for p in candidates), "unresolved framework import: " + name)
    return str(len(required)) + " framework imports resolved statically; external imports not executed"


def syntax(root, relative):
    ast.parse(regular(root, relative).read_text(encoding="utf-8"), filename=relative)
    return "Python AST parses; imports not executed"


def parse_check(root, relative):
    load(root, relative)
    return "TOON parsed"


def roundtrip(value):
    encoded = encode_toon(value)
    require(decode_toon(encoded) == value, "TOON value drift")
    require(encode_toon(decode_toon(encoded)) == encoded, "TOON byte drift")
    return "value and canonical bytes preserved"


def state_simulation():
    from ai_sdlc_state_machine import initial_state, begin_stage, validate_transition, STAGES
    state = initial_state("doctor-fixture", "refinement", observed_on=date(2000, 1, 1))
    first = STAGES[0].skill
    errors, _ = begin_stage(state, first, "full", observed_on=date(2000, 1, 1))
    require(not errors, str(errors))
    errors, _ = validate_transition(state, STAGES[-1].skill, "full")
    require(bool(errors), "illegal transition accepted")
    return "legal initial transition accepted; unavailable final transition rejected; memory only"


def validate_report(value):
    require(value.get("schema") == SCHEMA and value.get("execution") == "PASS", "invalid diagnostic report identity")
    require(value.get("health") == health(value["checks"]), "health aggregation mismatch")
    contract = decode_toon((HERE.parent / "references/framework-report.schema.toon").read_text(encoding="utf-8"))
    require(set(value) == set(contract["required"]), "unexpected or missing report fields")
    unsigned = {k:v for k,v in value.items() if k != "fingerprint"}
    require(value["fingerprint"] == hashlib.sha256(encode_toon(unsigned).encode("utf-8")).hexdigest(), "diagnostic fingerprint mismatch")
    identities = [c["id"] for c in value["checks"]]
    require(len(identities) == len(set(identities)), "duplicate check identity")
    for check in value["checks"]:
        require(check["check_id"] in REGISTRY and check["status"] in STATUSES, "invalid check contract")
        policy = REGISTRY[check["check_id"]]
        require(check["layer"] == policy.layer and check["severity"] == policy.severity and check["repair_route"] == policy.route, "diagnostic policy mismatch")
        require(check["code"] == ("" if check["status"] in {"PASS", "N/A"} else policy.code), "diagnostic code mismatch")
        require(check["id"] == stable_id(check["check_id"], check["component"]), "unstable diagnostic identity")
        require(set(check["blocked_by"]) <= set(identities), "dangling diagnostic prerequisite")
    require(value["checks"] == sorted(value["checks"], key=lambda c:(c["check_id"],c["component"])), "noncanonical check ordering")
    expected = {c["id"] for c in value["checks"] if c["status"] in {"FAIL","UNKNOWN"} or (c["status"] == "BLOCKED" and not c["blocked_by"])}
    require({c["id"] for c in value["findings"]} == expected, "missing or fabricated root findings")
    return value


def markdown(value):
    import chat_output
    contract = chat_output.contract(HERE.parent)
    status = {"HEALTHY":"PASS", "UNHEALTHY":"FAIL", "BLOCKED":"BLOCKED", "DEGRADED":"WARNING"}[value["health"]]
    primary = []
    for layer in sorted({c["layer"] for c in value["checks"]}):
        group = [c for c in value["checks"] if c["layer"] == layer]
        observed = "; ".join(str(sum(c["status"] == state for c in group)) + " " + state for state in ("PASS","FAIL","BLOCKED","UNKNOWN","N/A"))
        primary.append(dict(zip(contract["primary"], [layer, observed, "All requested checks terminal", {"HEALTHY":"PASS","UNHEALTHY":"FAIL","BLOCKED":"BLOCKED","DEGRADED":"WARNING"}[health(group)], "None" if health(group)=="HEALTHY" else "See diagnostic findings"])))
    failures=[]
    actions=[]
    if status in {"FAIL","BLOCKED"}:
        first=value["findings"][0]
        failures=[dict(zip(contract["failure"], ["requested source root",status,first["code"],first["id"],first["repair_route"]]))]
    if value["findings"]:
        actions=[dict(Owner=c["repair_route"], **{"Next action":"Resolve " + c["id"],"Expected evidence":"Rerun " + c["check_id"]}) for c in value["findings"][:8]]
    result=dict(schema="ai-sdlc-chat-result/v1", summary=dict(Status=status, Decision=value["health"] + "; doctor execution=" + value["execution"], Evidence="profile="+value["mode"]+"; fingerprint="+value["fingerprint"]), primary=primary, failures=failures, actions=actions, full_artifact="same invocation --format toon")
    result["secondary"] = [dict(zip(contract["secondary"], [c["id"], c["severity"], c["component"][:175], c["code"], c["evidence"][:175] or "prerequisite failed", c["repair_route"]])) for c in value["findings"]]
    rendered=chat_output.render(contract,result)
    evaluation=chat_output.evaluate(contract,rendered)
    require(evaluation["status"] == "PASS", str(evaluation["failures"]))
    return rendered


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    flows = parser.add_mutually_exclusive_group()
    flows.add_argument("--quick-flow", action="store_true", help="non-interactive diagnostic handoff; health rules unchanged")
    flows.add_argument("--full-flow", action="store_true", help="verified diagnostic handoff; health rules unchanged")
    parser.add_argument("--state-check", action="store_true", help="require an explicit typed state artifact")
    parser.add_argument("--begin-state", action="store_true", help="rejected: Doctor cannot mutate lifecycle state")
    parser.add_argument("--complete-state", action="store_true", help="rejected: Doctor cannot mutate lifecycle state")
    parser.add_argument("--mode", choices=("quick", "standard", "deep"), default="quick")
    parser.add_argument("--skill")
    parser.add_argument("--artifact", action="append", default=[], help="toon:path, state:path, okf:bundle, loop-state:feature, decomposition:report or handoff:packet@report; root-relative")
    parser.add_argument("--format", choices=("toon", "markdown"), default="toon")
    args = parser.parse_args(argv)
    try:
        require(not args.begin_state and not args.complete_state, "Doctor cannot mutate lifecycle state")
        artifacts = []
        for item in args.artifact:
            kind, relative = item.split(":", 1)
            require(kind in {"toon", "okf", "state", "loop-state", "decomposition", "handoff"}, "unsupported artifact kind")
            artifacts.append((kind, relative))
        require(not args.state_check or any(k in {"state", "loop-state"} for k,r in artifacts), "state check requires a typed state artifact")
        result = diagnose(args.root.absolute(), args.mode, args.skill, tuple(sorted(set(artifacts))))
        print(markdown(result) if args.format == "markdown" else encode_toon(result), end="")
        return 0 if result["health"] == "HEALTHY" else 2
    except (OSError, ValueError, TypeError) as exc:
        print(encode_toon(dict(schema="ai-sdlc-doctor-error/v1", execution="FAIL", health="UNKNOWN", code="INVALID_INPUT", evidence=type(exc).__name__)), end="")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
