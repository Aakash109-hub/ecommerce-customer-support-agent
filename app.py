import streamlit as st
import uuid
from main import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage

# =====================================================
# 1. Page Config
# =====================================================
st.set_page_config(
    page_title="E-Commerce Customer Support",
    page_icon="🛍️",
    layout="wide"
)

# =====================================================
# 2. Global Theme & Styling
# =====================================================
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #f8fafc;
}

/* ===============================
   Global Text Fix
================================ */

/* All headings */
h1, h2, h3, h4, h5, h6 {
    color: #0f172a !important;   /* Dark slate */
}

/* Subheaders like "Live Support" */
[data-testid="stSubheader"] {
    color: #0f172a !important;
    font-weight: 600;
}

/* Paragraphs & list items */
p, li, span {
    color: #334155 !important;   /* Readable gray */
}

/* Support cards text */
.support-card h4 {
    color: #0f172a !important;
}
.support-card p,
.support-card li {
    color: #475569 !important;
}

/* Chat title */
.stMarkdown h3 {
    color: #0f172a !important;
}

/* Sidebar text */
.css-1d391kg, .css-1cpxqw2 {
    color: #e5e7eb !important;
}

/* Chat messages */
[data-testid="stChatMessage"] p {
    color: #0f172a !important;
}

/* Typing indicator */
.typing {
    color: #64748b !important;
    font-style: italic;
}

            

/* Remove default padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}

/* Header */
.support-header {
    background: #0f172a;
    padding: 18px;
    border-radius: 14px;
    color: white;
    margin-bottom: 20px;
}

/* Cards */
.support-card {
    background: #ffffff;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

/* Chat container */
.chat-container {
    background: #ffffff;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

/* Quick replies */
.quick-replies {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    margin-bottom: 8px;
}
.quick-replies button {
    border-radius: 999px;
    background-color: #eef2ff;
    color: #1e3a8a;
    border: none;
    font-size: 0.85rem;
    white-space: nowrap;
}
.quick-replies button:hover {
    background-color: #e0e7ff;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
}

/* Text */
p, li {
    color: #334155;
}

.support-header {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 22px;
        border-radius: 14px;
        margin-bottom: 24px;
    }

.support-header h2 {
        color: #ffffff !important;
        font-weight: 700;
        margin-bottom: 6px;
    }

            
.support-header p {
        color: #cbd5f5 !important;
        font-size: 15px;
        margin: 0;
    }

</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. Session State
# =====================================================
def init_state():
    defaults = {
        "chat_history": [],
        "thread_id": str(uuid.uuid4()),
        "chat_threads": retrieve_all_threads(),
        "pending_user_input": None,
        "is_typing": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

QUICK_REPLIES = [
    "📦 Track my order",
    "🚚 Shipping delay",
    "🔄 Return a product",
    "💰 Refund policy",
    "❓ General question"
]

# =====================================================
# 4. Helpers
# =====================================================
def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    messages = []
    if state.values and "messages" in state.values:
        for msg in state.values["messages"]:
            if isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage) and msg.content:
                messages.append({"role": "assistant", "content": msg.content})
    return messages


def reset_chat():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.session_state.pending_user_input = None
    st.session_state.is_typing = False
    st.rerun()

# =====================================================
# 5. Sidebar
# =====================================================
st.sidebar.title("🛍️ Help Center")
st.sidebar.caption("E-Commerce Support Assistant")

if st.sidebar.button("➕ New Support Chat", use_container_width=True):
    reset_chat()

st.sidebar.subheader("Recent Conversations")

all_threads = list(set(
    st.session_state.chat_threads + [st.session_state.thread_id]
))

for tid in all_threads:
    if st.sidebar.button(f"Chat {tid[:8]}", key=tid, use_container_width=True):
        st.session_state.thread_id = tid
        st.session_state.chat_history = load_conversation(tid)
        st.rerun()

# =====================================================
# 6. Header
# =====================================================
st.markdown("""
<div class="support-header">
    <h2>🛍️ E-Commerce Customer Support</h2>
    <p>Orders, shipping, returns, and refunds</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 7. Layout
# =====================================================
left_col, right_col = st.columns([2, 1], gap="large")

# =====================================================
# 8. Left Column (Support Info)
# =====================================================
with left_col:
    st.markdown("""
    <div class="support-card">
        <h4>📦 Quick Help</h4>
        <ul>
            <li>🚚 Track shipping status</li>
            <li>🔄 Returns & refunds</li>
            <li>📦 Order issues</li>
            <li>❓ FAQs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="support-card">
        <h4>🧾 Order Assistance</h4>
        <p>Share your <strong>order ID</strong> in chat for faster support.</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 9. Right Column (Chat)
# =====================================================
with right_col:
    st.subheader("💬 Live Support")

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    chat_box = st.container(height=450)

    # Render messages
    with chat_box:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state.is_typing:
            with st.chat_message("assistant"):
                st.markdown("🟢 *Support agent is typing…*")

    st.markdown('</div>', unsafe_allow_html=True)

    # Quick replies (only at start)
    if not st.session_state.chat_history:
        st.markdown('<div class="quick-replies">', unsafe_allow_html=True)
        for reply in QUICK_REPLIES:
            if st.button(reply, key=f"qr_{reply}"):
                st.session_state.chat_history.append(
                    {"role": "user", "content": reply}
                )
                st.session_state.pending_user_input = reply
                st.session_state.is_typing = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Describe your issue…")

    if user_input:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )
        st.session_state.pending_user_input = user_input
        st.session_state.is_typing = True
        st.rerun()

# =====================================================
# 10. Assistant Response
# =====================================================
if st.session_state.pending_user_input:
    user_input = st.session_state.pending_user_input
    st.session_state.pending_user_input = None
    st.session_state.is_typing = False

    CONFIG = {"configurable": {"thread_id": st.session_state.thread_id}}

    with right_col:
        with chat_box:
            with st.chat_message("assistant"):
                def stream_response():
                    for chunk, meta in chatbot.stream(
                        {"messages": [HumanMessage(content=user_input)]},
                        config=CONFIG,
                        stream_mode="messages"
                    ):
                        if meta.get("langgraph_node") == "agent" and chunk.content:
                            yield chunk.content

                ai_response = st.write_stream(stream_response())

    st.session_state.chat_history.append(
        {"role": "assistant", "content": ai_response}
    )

    if st.session_state.thread_id not in st.session_state.chat_threads:
        st.session_state.chat_threads.append(st.session_state.thread_id)

    st.rerun()
