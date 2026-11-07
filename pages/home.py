import streamlit as st

from sparkprompt.providers import PROVIDER_DEFAULTS, ProviderName, create_provider
from sparkprompt.service import PromptService


# Home function for the Streamlit app
def home():
    st.title("SparkPrompt 🧙‍♂️")
    st.subheader("Prompt Writing Simulator to improve core prompt engineering skills🕹️")

    provider_name = ProviderName(
        st.selectbox("Model provider", [provider.value for provider in ProviderName])
    )
    defaults = PROVIDER_DEFAULTS[provider_name]
    model = st.text_input(
        "Model ID",
        value=defaults.model,
        key=f"model_{provider_name.name.lower()}",
        help="Use a model ID available to your provider account.",
    )
    api_key = st.text_input(
        defaults.key_label,
        type="password",
        key=f"api_key_{provider_name.name.lower()}",
    )
    if st.button("Clear this provider key", disabled=not bool(api_key)):
        st.session_state.pop(f"api_key_{provider_name.name.lower()}", None)
        st.rerun()

    cloud_consent = st.checkbox(
        f"Send exercises, prompts, and feedback to {provider_name.value}",
        key=f"consent_{provider_name.name.lower()}",
    )

    st.caption(
        f"Prompts and generated feedback are sent to {provider_name.value}. "
        "The key remains in this Streamlit session and is not written to disk."
    )

    selection = f"{provider_name.name}:{model.strip()}"
    previous_selection = st.session_state.get("sparkprompt_provider_selection")
    if previous_selection not in {None, selection}:
        for key in ("problem_statement", "evaluation", "best_prompt"):
            st.session_state.pop(key, None)
        st.info("Generated exercise state was cleared because the provider or model changed.")
    st.session_state.sparkprompt_provider_selection = selection

    if api_key and cloud_consent:
        # The client belongs to this Streamlit session/rerun. The key is
        # passed directly and never written to the process environment.
        service = PromptService(create_provider(provider_name, api_key, model))

        # Initialize session state variables
        if "problem_statement" not in st.session_state:
            st.session_state.problem_statement = ""
        if "evaluation" not in st.session_state:
            st.session_state.evaluation = ""
        if "best_prompt" not in st.session_state:
            st.session_state.best_prompt = ""

        # Step 1: User inputs
        st.subheader("Select Domain and Input Skills:")
        domain = st.selectbox(
            "Select Domain",
            [
                "AI",
                "Data Science",
                "Web Development",
                "Machine Learning",
                "Sales & Marketing",
                "Other",
            ],
        )
        skills = st.text_input("Enter your skills (comma-separated)", max_chars=1_000)

        if st.button("Generate Problem Statement"):
            try:
                st.session_state.problem_statement = service.generate_problem_statement(
                    domain, skills
                )
            except Exception:
                st.error(
                    "The selected provider could not generate an exercise. "
                    "Check the key, model, connection, and quota."
                )

        if st.session_state.problem_statement:
            st.write(st.session_state.problem_statement)

            # Step 2: User writes a prompt
            st.subheader("Write Your Prompt:")
            user_prompt = st.text_area("Enter your prompt here", max_chars=8_000)

            if st.button("Evaluate Prompt"):
                try:
                    result = service.evaluate_and_refine(
                        user_prompt,
                        st.session_state.problem_statement,
                    )
                except Exception:
                    st.error(
                        "The selected provider could not evaluate this prompt. "
                        "Check the key, model, connection, and quota."
                    )
                else:
                    st.session_state.evaluation = result.feedback
                    st.session_state.best_prompt = result.refined_prompt

            if st.session_state.evaluation:
                st.markdown("---")
                st.write(st.session_state.evaluation)
                st.markdown("---")
                st.write(st.session_state.best_prompt)
                st.markdown("---")
    elif api_key:
        st.info("Confirm provider transmission to enable model requests.")
