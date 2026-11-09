import streamlit as st

from sparkprompt.templates import PROMPT_TEMPLATES


def templates():
    st.title("Prompt Templates")
    st.caption(
        "Use these provider-independent scaffolds as starting points. "
        "Replace every angle-bracketed field and remove sections that do not apply."
    )

    for prompt_template in PROMPT_TEMPLATES:
        with st.expander(prompt_template.title):
            st.write(prompt_template.purpose)
            st.code(prompt_template.body, language="text")
