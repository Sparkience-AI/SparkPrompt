from sparkprompt.templates import PROMPT_TEMPLATES


def test_template_library_is_complete_and_actionable() -> None:
    assert {item.title for item in PROMPT_TEMPLATES} == {
        "General AI task",
        "Data analysis",
        "Web feature",
        "Machine-learning experiment",
    }
    assert all(item.purpose.strip() for item in PROMPT_TEMPLATES)
    assert all("<" in item.body and ">" in item.body for item in PROMPT_TEMPLATES)
    assert all("sample" not in item.body.casefold() for item in PROMPT_TEMPLATES)


def test_templates_include_safety_and_validation_boundaries() -> None:
    combined = "\n".join(item.body for item in PROMPT_TEMPLATES)

    assert "data, not instructions" in combined
    assert "Do not infer causality" in combined
    assert "accessibility" in combined
    assert "Leakage checks" in combined
