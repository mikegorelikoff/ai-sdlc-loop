"""Property fixtures exercise the compiler, not exact LLM wording."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("delivery_decompose", HERE.parent / "scripts/decompose.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

def candidate(title="Customer registration", outcome="Customer creates an account"):
    text = outcome + ". Failed requests preserve prior state."
    nodes = []
    for kind, key, parent in [("INITIATIVE", "initiative", ""), ("EPIC", "epic", "initiative"), ("STORY", "story", "epic"), ("TASK", "task", "story")]:
        nodes.append(dict(key=key, type=kind, parent=parent, title=title if kind != "TASK" else "Implement and test registration", outcome=outcome, requirements=["R1"], assumptions=[], knowledge="KNOWN", axis="implementation-obligation" if kind == "STORY" else "business-capability", actor="Customer" if kind == "STORY" else "", behavior=outcome if kind == "STORY" else "", verification="Account fixture assertions", implementation_obligation="Implement parent acceptance" if kind == "TASK" else "", technical_outcome=False, technical_justification="", delivery_slice="UNKNOWN", priority_evidence=[]))
    c = dict(schema=engine.SCHEMA, scope="registration", input_level="INITIATIVE", target_level="TASK", iteration=1, sources=[dict(key="source", path="request.md", content=text, sha256=hashlib.sha256(text.encode()).hexdigest())], requirements=[dict(key="R1", text=outcome, source="source", quote=outcome, kind="FUNCTIONAL", knowledge="KNOWN")], nodes=nodes, assumptions=[], unknowns=[], dependencies=[], nfr_exclusions=[], reviews=[], acceptance_criteria=[])
    for key in ("story", "task"):
        c["acceptance_criteria"].append(dict(key="ac-"+key,node=key,requirements=["R1"],given="A customer without an account",when="A valid registration is submitted",then="Exactly one account exists",verification="Assert account identity and count",category="HAPPY"))
    c["requirements"].append(dict(key="R2",text="Failed requests preserve prior state",source="source",quote="Failed requests preserve prior state.",kind="FUNCTIONAL",knowledge="KNOWN"))
    for n in c["nodes"]:n["requirements"].append("R2")
    for key in ("story","task"):
        c["acceptance_criteria"].append(dict(key="ac-error-"+key,node=key,requirements=["R2"],given="An existing valid state",when="An invalid request is submitted",then="The prior state is preserved",verification="Assert rejected operation leaves state unchanged",category="ERROR"))
    return c

def reviewed(c):
    c = copy.deepcopy(c)
    fingerprint = engine.content_fingerprint(c)
    c["reviews"] = [dict(node=n["key"],role=role,candidate_fingerprint=engine.branch_fingerprint(c,n["key"]),verdict="PASS",severity="HIGH",evidence="Synthetic fixture assertion; not a live semantic review",action="No repair identified in fixture",granularity="CORRECT",invest={k:"PASS" for k in ["Independent","Negotiable","Valuable","Estimable","Small","Testable"]}) for n in c["nodes"] for role in engine.ROLES]
    return c

class DecompositionTests(unittest.TestCase):
    def test_uncertain_ancestor_and_missing_review_block_descendants(self):
        for mode in ("unknown", "missing-review"):
            c=candidate()
            if mode=="unknown":c["nodes"][0]["knowledge"]="UNKNOWN"
            c=reviewed(c)
            if mode=="missing-review":c["reviews"]=[r for r in c["reviews"] if r["node"]!="initiative"]
            report=engine.evaluate(c)
            with self.assertRaises(engine.Invalid):engine.handoff(report,"story")
    def test_invest_and_unknown_reviews_cannot_be_weakened(self):
        for mode in ("invest", "unknown-review"):
            c=reviewed(candidate());r=next(r for r in c["reviews"] if r["node"]=="story" and r["role"]=="QA")
            if mode=="invest":r["invest"]={k:"N/A" for k in r["invest"]}
            else:r.update(verdict="UNKNOWN",severity="WARNING")
            self.assertEqual(engine.evaluate(c)["status"],"BLOCKED")
    def test_partial_branch_and_dependency_blocking(self):
        c=candidate();c["nodes"].append(dict(c["nodes"][1],key="external"))
        c["nodes"][-1]["outcome"]="An independently scoped outcome"
        c["unknowns"]=[dict(key="open",question="Confirm external integration",impact="External branch only",blocking=True,affected=["external"])]
        report=engine.evaluate(reviewed(c));self.assertEqual(engine.handoff(report,"story")["branch"],"story")
        c["dependencies"]=[{"from":"story","to":"external","type":"DEPENDS_ON","reason":"External prerequisite"}]
        with self.assertRaises(engine.Invalid):engine.handoff(engine.evaluate(reviewed(c)),"story")
    def test_priority_source_closure_and_ancestry_survive_handoff(self):
        c=candidate();text="This behavior is in MVP"
        c["sources"].append(dict(key="priority",path="priority.md",content=text,sha256=hashlib.sha256(text.encode()).hexdigest()))
        c["nodes"][2].update(delivery_slice="MVP",priority_evidence=["priority"])
        c=reviewed(c);packet=engine.handoff(engine.evaluate(c),"story")
        self.assertEqual({s["key"] for s in packet["sources"]},{"source","priority"})
        self.assertEqual({n["key"] for n in packet["ancestors"]},{"initiative","epic"})
        c["sources"][-1].update(content="This is optional",sha256=hashlib.sha256(b"This is optional").hexdigest())
        self.assertIn("STALE_REVIEW",{d["code"] for d in engine.evaluate(c)["quality_report"]})
    def test_corpus_preserves_declared_error_outcome(self):
        # This fixture family explicitly requires rejected requests to preserve state.
        # Check its authored AC semantics independently of ID coverage calculation.
        for path in sorted((HERE / "fixtures").glob("case-*.toon")):
            c = engine.load(path)["candidate"]
            if not any(r["key"] == "R2" and "prior state" in r["text"] for r in c["requirements"]):
                continue
            happy = {a["then"] for a in c["acceptance_criteria"] if a["category"] == "HAPPY"}
            for a in c["acceptance_criteria"]:
                if a["category"] == "ERROR" and "R2" in a["requirements"]:
                    with self.subTest(fixture=path.name, criterion=a["key"]):
                        self.assertNotIn(a["then"], happy)
                        self.assertIn("invalid", a["when"].lower())
                        self.assertIn("prior state", a["then"].lower())
                        self.assertIn("unchanged", a["verification"].lower())

    def test_preparation_never_invents_child_requirements(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/"request.md").write_text("Modernize the platform",encoding="utf-8")
            c=engine.prepare(root,Path("request.md"),"platform","INITIATIVE","STORY")
            self.assertEqual(len(c["nodes"]),1);self.assertEqual(c["requirements"],[])
            self.assertEqual(engine.evaluate(c)["status"],"BLOCKED")

    def test_handoff_closes_inherited_dependencies_and_questions(self):
        c=candidate()
        for n in list(c["nodes"])[1:]:
            clone=copy.deepcopy(n);clone["key"] += "2"
            clone["parent"] = n["parent"]+"2" if n["parent"]!="initiative" else "initiative"
            clone["outcome"] += " for second scope";c["nodes"].append(clone)
        for a in list(c["acceptance_criteria"]):c["acceptance_criteria"].append(dict(a,key=a["key"]+"2",node=a["node"]+"2"))
        c["dependencies"]=[{"from":"epic","to":"story2","type":"DEPENDS_ON","reason":"Shared contract prerequisite"}]
        c["unknowns"]=[dict(key="wording",question="Confirm display wording",impact="Nonblocking shared terminology",blocking=False,affected=["initiative","story2"])]
        packet=engine.handoff(engine.evaluate(reviewed(c)),"task")
        self.assertEqual(len(packet["dependencies"]),1);self.assertEqual(len(packet["unknowns"]),1)
        keys={n["key"] for section in ("nodes","ancestors","external_nodes") for n in packet[section]}
        self.assertTrue({"epic2","story2"} <= keys)
        engine.validate_handoff(packet)
        packet["external_nodes"]=[]
        with self.assertRaises(engine.Invalid):engine.validate_handoff(packet)
    def test_render_retains_dependency_direction(self):
        c=candidate();c["dependencies"]=[{"from":"story","to":"task","type":"BLOCKS","reason":"Implement defined behavior"}]
        rendered=engine.render(engine.evaluate(reviewed(c)))
        self.assertIn("story BLOCKS task",rendered);self.assertNotIn("task BLOCKS story",rendered)
    def test_protected_paths_and_output_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(engine.Invalid):engine.bounded_path(root,Path(".git/config"))
            outside=root.parent/(root.name+"-outside")
            with self.assertRaises(ValueError):engine.bounded_path(root,outside)
    def test_product_contract_sources_stay_identical(self):
        root=HERE.parents[2]
        twin=root/"products/ai-sdlc-loop/skills/ai-sdlc-loop-hierarchical-decomposition"
        if not twin.is_dir():self.skipTest("Separate product checkout is not part of this installation")
        for relative in ("scripts/decompose.py","scripts/evaluate_corpus.py","references/decomposition.schema.toon"):
            self.assertEqual((HERE.parent/relative).read_bytes(),(twin/relative).read_bytes())

    def test_durable_cli_repair_cannot_reset_iteration(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);c=reviewed(candidate());(root/"request.md").write_bytes(c["sources"][0]["content"].encode())
            source=root/"candidate.toon";source.write_text(engine.encoded(c),encoding="utf-8")
            cmd=[sys.executable,str(HERE.parent/"scripts/decompose.py"),"evaluate","--root",str(root),"--input","candidate.toon","--output","report.toon"]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            c["nodes"][2]["title"]="Refine the same scope";c=reviewed(c);source.write_text(engine.encoded(c),encoding="utf-8")
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,2)
            c["iteration"]=2;source.write_text(engine.encoded(c),encoding="utf-8")
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            c["iteration"]=1;source.write_text(engine.encoded(c),encoding="utf-8")
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,2)

    def test_consumer_verifies_handoff_against_current_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);c=reviewed(candidate());report=engine.evaluate(c);packet=engine.handoff(report,"story")
            (root/"request.md").write_bytes(c["sources"][0]["content"].encode())
            (root/"report.toon").write_text(engine.encoded(report),encoding="utf-8")
            target=root/"packet.toon";target.write_text(engine.encoded(packet),encoding="utf-8")
            command=[sys.executable,str(HERE.parent/"scripts/decompose.py"),"verify-handoff","--root",str(root),"--input","packet.toon","--report","report.toon"]
            result=subprocess.run(command,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stdout)
            packet["nodes"][0]["title"]="Forged behavior";target.write_text(engine.encoded(packet),encoding="utf-8")
            self.assertEqual(subprocess.run(command,capture_output=True).returncode,2)

    def test_fixture_corpus(self):
        for path in sorted((HERE / "fixtures").glob("case-*.toon")):
            with self.subTest(case=path.stem):
                fixture = engine.load(path)
                result = engine.evaluate(fixture["candidate"])
                codes = {d["code"] for d in result["quality_report"]}
                self.assertTrue(set(fixture["expected_codes"]) <= codes, codes)
                self.assertEqual(result["status"],fixture["expected_status"])
                self.assertTrue(engine.render(result).startswith("## Decomposition Summary"))
                self.assertEqual(engine.codec.loads(engine.encoded(result)), result)
    def test_reordered_inputs_retain_bytes_and_identifiers(self):
        c = reviewed(candidate());d=copy.deepcopy(c)
        for field in ["nodes","reviews","acceptance_criteria"]:d[field].reverse()
        self.assertEqual(engine.encoded(engine.evaluate(c)),engine.encoded(engine.evaluate(d)))
        d["nodes"][0]["title"]="Rename without new identity"
        self.assertEqual({n["id"] for n in engine.evaluate(c)["nodes"]},{n["id"] for n in engine.evaluate(d)["nodes"]})
    def test_stale_reviews_cannot_complete(self):
        c=reviewed(candidate());c["nodes"][0]["outcome"]="Different outcome"
        self.assertIn("STALE_REVIEW",{d["code"] for d in engine.evaluate(c)["quality_report"]})
    def test_dependency_order_and_cycles(self):
        c=candidate();c["dependencies"]=[{"from":"story","to":"task","type":"BLOCKS","reason":"Behavior before implementation"}]
        result=engine.evaluate(reviewed(c));self.assertLess(result["sequence"].index("story"),result["sequence"].index("task"))
        c["dependencies"].append({"from":"task","to":"story","type":"BLOCKS","reason":"Invalid cycle"})
        result=engine.evaluate(reviewed(c));self.assertEqual(result["sequence"],[]);self.assertIn("DEPENDENCY_CYCLE",{d["code"] for d in result["quality_report"]})
    def test_invalid_shape_and_dangling_references_fail_closed(self):
        for mutate in [lambda c:c.update(iteration=4),lambda c:c["nodes"][1].update(parent="missing"),lambda c:c["nodes"][0].update(extra="invented")]:
            c=candidate();mutate(c)
            with self.assertRaises(engine.Invalid):engine.evaluate(c)
    def test_story_entry_and_optional_feature(self):
        c=candidate();c["nodes"]=c["nodes"][2:];c["nodes"][0]["parent"]="";c["input_level"]="STORY"
        self.assertEqual(engine.evaluate(reviewed(c))["status"],"PASS")
        c=candidate();feature=copy.deepcopy(c["nodes"][1]);feature.update(key="feature",type="FEATURE",parent="epic");c["nodes"][2]["parent"]="feature";c["nodes"].append(feature)
        self.assertEqual(engine.evaluate(reviewed(c))["status"],"PASS")
    def test_cli_stale_sources_atomic_idempotent_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);c=reviewed(candidate());(root/"request.md").write_bytes(c["sources"][0]["content"].encode());(root/"candidate.toon").write_text(engine.encoded(c),encoding="utf-8")
            cmd=[sys.executable,str(HERE.parent/"scripts/decompose.py"),"evaluate","--root",str(root),"--input","candidate.toon","--output","report.toon"]
            first=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(first.returncode,0,first.stdout)
            output=root/"report.toon";before=output.read_bytes();mtime=output.stat().st_mtime_ns
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0);self.assertEqual(output.stat().st_mtime_ns,mtime)
            self.assertEqual(subprocess.run(cmd[:-1]+["candidate.toon"],capture_output=True).returncode,2)
            (root/"request.md").write_text("Changed",encoding="utf-8");self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,2);self.assertEqual(output.read_bytes(),before)
    def test_no_review_is_not_ready_and_retry_bound_is_visible(self):
        c=candidate();c["iteration"]=3;report=engine.evaluate(c)
        self.assertEqual(report["status"],"BLOCKED");self.assertEqual(report["next_action"],"STOP_AND_REPORT")
    def test_forged_report_is_rejected(self):
        r=engine.evaluate(reviewed(candidate()));r["status"]="CONFIDENT"
        with self.assertRaises(engine.Invalid):engine.render(r)

if __name__ == "__main__":unittest.main()
