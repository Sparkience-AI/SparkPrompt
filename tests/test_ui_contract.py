from pathlib import Path

HOME_SOURCE = (Path(__file__).parents[1] / "pages" / "home.py").read_text(encoding="utf-8")


def test_cloud_provider_ui_requires_password_key_and_transmission_consent() -> None:
    assert 'type="password"' in HOME_SOURCE
    assert "cloud_consent = st.checkbox(" in HOME_SOURCE
    assert "if api_key and cloud_consent:" in HOME_SOURCE
    assert "os.environ" not in HOME_SOURCE


def test_provider_or_model_change_clears_generated_exercise_state() -> None:
    assert "sparkprompt_provider_selection" in HOME_SOURCE
    assert '("problem_statement", "evaluation", "best_prompt")' in HOME_SOURCE


def test_provider_failures_are_not_rendered_verbatim() -> None:
    assert "st.error(str(" not in HOME_SOURCE
    assert "Check the key, model, connection, and quota." in HOME_SOURCE
