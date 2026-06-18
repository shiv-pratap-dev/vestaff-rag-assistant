import uuid
import requests
import streamlit as st


 
# CONFIG
 

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="VeStaff RAG",
    page_icon="📄",
    layout="wide"
)

 
# MONOCHROME STYLING
 

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0f1117;
        color: white;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: #9ca3af;
        margin-bottom: 2rem;
    }

    .metric-card {
        padding: 1rem;
        border-radius: 12px;
        background-color: #1a1d24;
        border: 1px solid #2a2e39;
    }

    </style>
    """,
    unsafe_allow_html=True
)

 
# SESSION STATE
 

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

 

# SIDEBAR

st.sidebar.title("VeStaff RAG")

st.sidebar.caption(
    "AWS Customer Agreement Assistant"
)

page = st.sidebar.radio(
    "Navigation",
    ["Chat", "Analytics"]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    f"Session: {st.session_state.session_id[:8]}..."
)

st.sidebar.markdown("---")

if st.sidebar.button(
    "📄 Ingest AWS Agreement",
    use_container_width=True
):

    with st.sidebar.spinner(
        "Processing document..."
    ):

        try:

            response = requests.post(
                f"{API_BASE_URL}/ingest",
                timeout=300
            )

            response.raise_for_status()

            data = response.json()

            st.sidebar.success(
                f"Ingested successfully "
                f"({data['chunks_created']} chunks)"
            )

        except Exception as e:

            st.sidebar.error(
                f"Ingestion failed: {str(e)}"
            )

 
# CHAT PAGE
 

if page == "Chat":

    st.markdown(
        '<div class="main-title">VeStaff RAG</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AWS Customer Agreement Assistant</div>',
        unsafe_allow_html=True
    )

    # Render chat history

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

            if (
                msg["role"] == "assistant"
                and "confidence_score" in msg
            ):

                st.caption(
                    f"Confidence Score: {msg['confidence_score']:.4f}"
                )

                with st.expander("Source Chunks"):

                    for chunk in msg["source_chunks"]:

                        st.markdown(
                            f"**Chunk {chunk['chunk_index']}**"
                        )

                        st.caption(
                            f"Score: {chunk['score']:.4f}"
                        )

                        st.code(
                            chunk["content"],
                            language=None
                        )

    # User input

    prompt = st.chat_input(
        "Ask a question about the AWS agreement..."
    )

    if prompt:

        # Add user message

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Call backend

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    response = requests.post(
                        f"{API_BASE_URL}/ask",
                        json={
                            "session_id":
                            st.session_state.session_id,

                            "question":
                            prompt
                        },
                        timeout=60
                    )

                    if response.status_code != 200:
                        try:
                            error_detail = (
                                response.json()
                                .get("detail", "Unknown error")
                            )
                        except Exception:
                            error_detail = response.text
                        st.error(error_detail)
                        st.stop()

                    data = response.json()

                    answer = data["answer"]

                    confidence_score = (
                        data["confidence_score"]
                    )

                    source_chunks = (
                        data["source_chunks"]
                    )

                    st.markdown(answer)

                    st.caption(
                        f"Confidence Score: "
                        f"{confidence_score:.4f}"
                    )

                    with st.expander(
                        "Source Chunks"
                    ):

                        for chunk in source_chunks:

                            st.markdown(
                                f"**Chunk "
                                f"{chunk['chunk_index']}**"
                            )

                            st.caption(
                                f"Score: "
                                f"{chunk['score']:.4f}"
                            )

                            st.code(
                                chunk["content"],
                                language=None
                            )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "confidence_score":
                            confidence_score,
                            "source_chunks":
                            source_chunks
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Error: {str(e)}"
                    )
 
# ANALYTICS PAGE
 

else:

    st.title("Analytics Dashboard")

    try:

        response = requests.get(
            f"{API_BASE_URL}/analytics",
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Queries",
                data["total_queries"]
            )

            st.metric(
                "Success Rate (%)",
                data["success_rate"]
            )

        with col2:

            st.metric(
                "Avg Latency (ms)",
                data["average_latency_ms"]
            )

            st.metric(
                "Avg Confidence",
                data["average_confidence_score"]
            )

        st.markdown("---")

        st.subheader(
            "Most Frequent Questions"
        )

        st.table(
            data["most_frequent_questions"]
        )

        st.subheader(
            "Unanswered Queries"
        )

        st.table(
            data["unanswered_queries"]
        )

        st.subheader(
            "Recent Queries"
        )

        st.table(
            data["recent_queries"]
        )

        st.subheader(
            "Slowest Queries"
        )

        st.table(
            data["slowest_queries"]
        )

    except Exception as e:

        st.error(
            f"Could not load analytics: {e}"
        )