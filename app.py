import streamlit as st
from ChatBot import movie_recommendation_chat, reset_conversation

st.set_page_config(
    page_title="ReelMatch",
    page_icon="🎬",
    layout="centered"
)

def render_chat_message(role, content):
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    with st.chat_message(role):
        st.markdown(
            f"""
            <div class="{bubble_class}">
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    """
    <style>
    :root {
        --bg-main: #0a1020;
        --bg-panel: #121a2a;
        --bg-panel-2: #172134;
        --text-main: #f8fafc;
        --text-soft: #94a3b8;
        --accent-1: #7c3aed;
        --accent-2: #2563eb;
        --accent-3: #22c55e;
        --border: rgba(148, 163, 184, 0.15);
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(124, 58, 237, 0.25), transparent 28%),
            radial-gradient(circle at top right, rgba(37, 99, 235, 0.22), transparent 32%),
            linear-gradient(135deg, #0a1020, #121826, #1a2333);
        color: var(--text-main);
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.2rem;
        animation: fadeInUp 0.6s ease;
    }

    .hero {
        padding: 1.1rem 1rem 1rem 1rem;
        border-radius: 20px;
        background: linear-gradient(90deg, #6d28d9, #2563eb);
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        animation: fadeInUp 0.7s ease;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 0.02em;
    }

    .hero p {
        margin: 0.35rem 0 0 0;
        font-size: 1rem;
        color: rgba(255,255,255,0.92);
    }

    .footer-note {
        display: flex;
        justify-content: center;
        align-items: center;
        width: fit-content;
        margin: 0.4rem auto 0.45rem auto;
        padding: 0.28rem 0.8rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(148,163,184,0.18);
        color: var(--text-soft);
        font-size: 0.78rem;
        line-height: 1.2;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #111827);
        border-right: 1px solid var(--border);
        box-shadow: var(--shadow);
    }

    .sidebar-brand {
        background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(37,99,235,0.18));
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.9rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        animation: fadeInUp 0.65s ease;
    }

    .brand-badge {
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: linear-gradient(135deg, #7c3aed, #2563eb);
        font-size: 1.25rem;
        flex-shrink: 0;
    }

    .brand-title {
        font-size: 1.02rem;
        font-weight: 700;
        color: white;
    }

    .brand-subtitle {
        font-size: 0.78rem;
        color: var(--text-soft);
    }

    .sidebar-section-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.8rem;
        margin-bottom: 0.85rem;
        animation: fadeInUp 0.75s ease;
    }

    .sidebar-section-card .stSelectbox,
    .sidebar-section-card .stInfo {
        background: transparent;
    }

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding: 0.25rem 0;
        margin: 0.1rem 0;
        animation: fadeInUp 0.45s ease;
    }

    .user-bubble,
    .assistant-bubble {
        max-width: 92%;
        padding: 0.85rem 0.95rem;
        border-radius: 18px;
        line-height: 1.4 !important; /* Tighter text tracking */
        font-size: 0.96rem;
        font-weight: 600;
        white-space: normal !important; /* CRITICAL: Stops rendering raw hidden newlines as massive vertical blocks */
        word-wrap: break-word;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.22);
    }

    .user-bubble {
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        color: #ffffff;
        margin-left: auto;
        border-bottom-right-radius: 6px;
    }

    .assistant-bubble {
        background: linear-gradient(135deg, #111827, #1f2937);
        color: #f8fafc;
        border: 1px solid rgba(148,163,184,0.24);
        margin-right: auto;
        border-bottom-left-radius: 6px;
    }

    /* Overriding Streamlit's native element spacing inside your custom bubbles */
    .assistant-bubble p, .user-bubble p {
        margin: 0 0 4px 0 !important; /* Reduces bottom margin of text blocks */
        padding: 0 !important;
    }

    .assistant-bubble h3, .user-bubble h3 {
        margin: 12px 0 4px 0 !important; /* Controls space above and below movie titles */
        padding: 0 !important;
    }

    .assistant-bubble ul, .user-bubble ul {
        margin: 4px 0 !important;
        padding-left: 20px !important;
    }

    .assistant-bubble li, .user-bubble li {
        margin: 2px 0 !important; /* Pulls individual bullet points completely close together */
        padding: 0 !important;
    }
    .stChatInput {
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(17, 24, 39, 0.9);
    }

    div[data-testid="stChatInput"] {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 16px;
    }

    div[data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background: #ffffff !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
    }

    .stButton > button {
        border-radius: 12px;
        border: none;
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        font-weight: 700;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.28);
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <h1>🎬 ReelMatch</h1>
        <p>Pick your vibe. Set your priority. Let the movie magic begin.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("What kind of movie night are you chasing?")
st.caption("Tell the bot your mood, genre, and what matters most — like fun, depth, runtime, or a surprise twist.")
st.write("---")

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-badge">🎬</div>
            <div>
                <div class="brand-title">ReelMatch</div>
                <div class="brand-subtitle">Movie Recommendation Assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-section-card">
            <div class="brand-title" style="font-size: 0.92rem; margin-bottom: 0.35rem;">Movie Mood</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    mood = st.selectbox(
        "Pick your current vibe",
        [
            "Feel-good",
            "Dark & intense",
            "Heartwarming",
            "Mind-bending",
            "Funny & light",
            "Action-packed",
            "Romantic",
            "Family-friendly",
            "Thriller & suspense",
            "Hidden gems"
            "Biography",
            "Sci-Fi & Fantasy",
            "Documentary",
            "Horror",
            "Musical",
            "Adventure",
            "Animated",
            "Fictional",
            "Historical",
            "Sports",
            "Spiritual"
        ]
    )

    st.markdown(
        """
        <div class="sidebar-section-card">
            <div class="brand-title" style="font-size: 0.92rem; margin-bottom: 0.35rem;">Priority</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    priority = st.selectbox(
        "What matters most?",
        [
            "I want the best storyline",
            "I want something fun and easy",
            "I want a thriller with twists",
            "I want a family-friendly pick",
            "I want something with a strong cast",
            "I want a hidden gem",
            "I want a movie that makes me think",
            "I want a movie that makes me laugh",
            "I want a movie that makes me cry",
            "I want a movie that inspires me",
            "I want a movie that surprises me",
            "I want a movie that is horrorful and scary",
            "I want a movie that is romantic and heartwarming",
        ]
    )

    st.info("The chatbot uses both your mood and priority to personalize recommendations.")

    st.write("---")
    if st.button("Reset Conversation", use_container_width=True):
        reset_conversation()
        st.session_state.chat_history = []
        st.rerun()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for item in st.session_state.chat_history:
    render_chat_message(item["role"], item["content"])

st.markdown(
    """
    <div class="footer-note">
        powered by ReelMatch (Author - Arka)
    </div>
    """,
    unsafe_allow_html=True
)

prompt = st.chat_input("Type your movie preference here...")

if prompt:
    full_context = (
        f"Mood: {mood}\n"
        f"Priority: {priority}"
    )

    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })

    render_chat_message("user", prompt)

    with st.spinner("Searching the reels for your perfect pick..."):
        response = movie_recommendation_chat(prompt, mood_context=full_context)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

    render_chat_message("assistant", response)