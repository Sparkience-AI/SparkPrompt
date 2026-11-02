import streamlit as st

from sparkprompt.providers import GeminiProvider
from sparkprompt.service import PromptService


# Home function for the Streamlit app
def home():
    st.title("SparkPrompt 🧙‍♂️")
    st.subheader("Prompt Writing Simulator to improve core prompt engineering skills🕹️")

    # Step 0: User input for Google API key
    api_key = st.text_input(
        "Enter your Google API Key",
        type="password",
        key="google_api_key",
    )
    if st.button("Clear API key", disabled=not bool(api_key)):
        st.session_state.pop("google_api_key", None)
        st.rerun()

    if api_key:
        # The client belongs to this Streamlit session/rerun. The key is
        # passed directly and never written to the process environment.
        service = PromptService(GeminiProvider(api_key))

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
        skills = st.text_input("Enter your skills (comma-separated)")

        if st.button("Generate Problem Statement"):
            st.session_state.problem_statement = service.generate_problem_statement(domain, skills)

        if st.session_state.problem_statement:
            st.write(st.session_state.problem_statement)

            # Step 2: User writes a prompt
            st.subheader("Write Your Prompt:")
            user_prompt = st.text_area("Enter your prompt here")

            if st.button("Evaluate Prompt"):
                result = service.evaluate_and_refine(
                    user_prompt,
                    st.session_state.problem_statement,
                )
                st.session_state.evaluation = result.feedback
                st.session_state.best_prompt = result.refined_prompt

            if st.session_state.evaluation:
                st.markdown("---")
                st.write(st.session_state.evaluation)
                st.markdown("---")
                st.write(st.session_state.best_prompt)
                st.markdown("---")
