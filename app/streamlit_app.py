import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="📚",
)

st.title("Multilingual AI Knowledge Assistant")
st.caption("Ask a question in English, French, or Arabic.")

question = st.text_area(
    "Your question",
    placeholder="What is an API?",
)

if st.button("Ask AI", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Generating answer..."):
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question},
                    timeout=190,
                )
                response.raise_for_status()
                result = response.json()

            st.markdown("### Answer")
            st.write(result["answer"])
            st.caption(f"Model: {result['model']}")

        except requests.RequestException:
            st.error(
                "The API is unavailable. Check that Docker "
                "services are running."
            )