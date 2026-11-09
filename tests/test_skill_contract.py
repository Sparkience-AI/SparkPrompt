import json
from pathlib import Path

SKILL_ROOT = Path(__file__).parents[1] / ".agents" / "skills" / "sparkprompt"
LLMS_SOURCE = (Path(__file__).parents[1] / "llms.txt").read_text(encoding="utf-8")


def test_skill_eval_suite_covers_routing_and_risk_cases() -> None:
    cases = json.loads((SKILL_ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))

    assert len({case["id"] for case in cases}) == len(cases)
    assert {case["should_trigger"] for case in cases} == {True, False}
    assert {"positive", "negative", "missing-input", "adversarial"} <= {
        case["category"] for case in cases
    }
    assert all(case["expected_behaviors"] for case in cases)
    assert all(case["forbidden_behaviors"] for case in cases)


def test_skill_bundle_has_required_agent_files() -> None:
    assert (SKILL_ROOT / "SKILL.md").is_file()
    assert (SKILL_ROOT / "agents" / "openai.yaml").is_file()
    assert (SKILL_ROOT / "references" / "rubric.md").is_file()


def test_skill_frontmatter_and_interface_are_discoverable() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    interface = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

    assert skill.startswith("---\nname: sparkprompt\ndescription:")
    assert "default_prompt:" in interface
    assert "$sparkprompt" in interface


def test_discovery_metadata_points_to_shipped_skill_files() -> None:
    assert ".agents/skills/sparkprompt/SKILL.md" in LLMS_SOURCE
    assert ".agents/skills/sparkprompt/references/rubric.md" in LLMS_SOURCE
    assert "skills/sparkprompt/" not in LLMS_SOURCE.replace(".agents/skills/sparkprompt/", "")
