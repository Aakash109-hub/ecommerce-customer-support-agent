import streamlit as st
import uuid
from langchain_core.messages import HumanMessage, AIMessage
from main import chatbot, retrieve_all_threads

# =====================================================
# 1. PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="E-Commerce Customer Support",
    page_icon="🛍️",
    layout="wide"
)

# =====================================================
# 2. GLOBAL THEME & STYLING
# =====================================================
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #F4F6F9;
}

/* Hide Streamlit default UI */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Global text */
h1, h2, h3, h4, h5, h6 {
    color: #0f172a !important;
    font-weight: 600;
}
[data-testid="stSubheader"] {
    color: #0f172a !important;
}
p, li, span, div {
    color: #334155;
}

/* ================= HEADER ================= */
.support-header {
    background: linear-gradient(135deg, #4B4ACD, #6366F1);
    padding: 22px 26px;
    border-radius: 16px;
    margin-bottom: 26px;
    box-shadow: 0 12px 32px rgba(75,74,205,0.28);
}
.support-header h2 {
    color: #ffffff !important;
    font-weight: 700;
    margin-bottom: 6px;
}
.support-header p {
    color: #E0E7FF !important;
    font-size: 15px;
    margin: 0;
}

/* ================= LEFT DASHBOARD (NEW) ================= */
.user-dashboard {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
    border: 1px solid #F0F2F6;
}

.user-profile {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
}
.avatar {
    width: 48px;
    height: 48px;
    background: #E0E7FF;
    color: #4B4ACD !important;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
}

/* Order Status Card */
.order-card {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 12px;
    margin-top: 10px;
}
.order-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: #64748B;
    margin-bottom: 8px;
}
.order-item {
    font-weight: 600;
    color: #0F172A !important;
    margin-bottom: 4px;
}
.status-badge {
    background: #DEF7EC;
    color: #03543F !important;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* ================= CHAT ================= */
.chat-container {
    background: #ffffff;
    border-radius: 22px;
    padding: 12px;
    border: 1px solid #EAEAEA;
    box-shadow: 0 15px 40px rgba(0,0,0,0.12);
}

/* Chat title bar */
.chat-title {
    background: #4B4ACD;
    color: white !important;
    padding: 14px 18px;
    border-radius: 16px 16px 0 0;
    font-weight: 600;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 10px;
}
[data-testid="stChatMessage"] p {
    color: #0f172a !important;
}

/* ================= QUICK REPLIES ================= */
.quick-replies {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 8px;
}
.quick-replies button {
    background-color: #ffffff;
    color: #4B4ACD;
    border: 1px solid #E0E0E0;
    border-radius: 14px;
    padding: 8px 16px;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
    box-shadow: 0 3px 6px rgba(0,0,0,0.08);
}
.quick-replies button:hover {
    background-color: #F0F0FF;
    border-color: #4B4ACD;
}

/* Typing indicator */
.typing {
    color: #64748b !important;
    font-style: italic;
}

/* Chat input */
div[data-testid="stChatInput"] {
    border-radius: 18px !important;
    border: 1px solid #E0E0E0;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. SESSION STATE
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

# =====================================================
# 4. HELPERS
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
# 5. SIDEBAR
# =====================================================
st.sidebar.title("🛍️ Help Center")
st.sidebar.caption("E-Commerce Support Assistant")

if st.sidebar.button("➕ New Support Chat", use_container_width=True):
    reset_chat()

st.sidebar.subheader("Recent Conversations")
for tid in set(st.session_state.chat_threads + [st.session_state.thread_id]):
    if st.sidebar.button(f"Chat {tid[:8]}", key=tid, use_container_width=True):
        st.session_state.thread_id = tid
        st.session_state.chat_history = load_conversation(tid)
        st.rerun()

# =====================================================
# 6. HEADER
# =====================================================
st.markdown("""
<div class="support-header">
    <h2>🛍️ E-Commerce Customer Support</h2>
    <p>Orders, shipping, returns, and refunds</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 7. MAIN LAYOUT
# =====================================================
left_col, right_col = st.columns([1, 2], gap="large") # Ratio changed for better look

# ---------------- LEFT COLUMN (USER DASHBOARD) ----------------
with left_col:
    # --- 1. User Profile Card ---
    st.markdown("""
    <div class="user-dashboard">
        <div class="user-profile">
            <div class="avatar">AS</div>
            <div>
                <div style="font-weight:600; font-size:1.1rem; color:#0f172a;">Aakash Gayke</div>
                <div style="font-size:0.85rem; color:#64748B;">Gold Member •USER-109</div>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:10px; border-top:1px solid #EAEAEA; padding-top:10px;">
            <div style="text-align:center;">
                <h4 style="margin:0; color:#4B4ACD !important;">12</h4>
                <span style="font-size:0.8rem; color:#64748B;">Orders</span>
            </div>
            <div style="text-align:center;">
                <h4 style="margin:0; color:#4B4ACD !important;">2</h4>
                <span style="font-size:0.8rem; color:#64748B;">Returns</span>
            </div>
            <div style="text-align:center;">
                <h4 style="margin:0; color:#4B4ACD !important;">Rs. 150</h4>
                <span style="font-size:0.8rem; color:#64748B;">Credit</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 3. Smart Actions ---
    st.markdown("##### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    
    # These buttons act as triggers to inject text into the chat loop
    with col1:
        if st.button("📍 Track Order", use_container_width=True):
            st.session_state.pending_user_input = "I want to track my order ?"
            st.session_state.is_typing = True
            st.rerun()
    with col2:
        if st.button("↩️ Return Item", use_container_width=True):
            st.session_state.pending_user_input = "I want to return order"
            st.session_state.is_typing = True
            st.rerun()
    with col1:
        if st.button("📃 Policies", use_container_width=True):
            st.session_state.pending_user_input = "What is your return policy?"
            st.session_state.is_typing = True
            st.rerun()
    with col2:
        if st.button("☎️ Support", use_container_width=True):
            st.session_state.pending_user_input = "I need to speak to a human"
            st.session_state.is_typing = True
            st.rerun()

# ---------------- RIGHT COLUMN (CHAT APP) ----------------
with right_col:
    st.markdown('<div class="chat-title">💬Sammy</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    chat_box = st.container(height=480) # Increased height slightly

    with chat_box:
        if not st.session_state.chat_history:
            st.info("👋 Hi Aakash! I'm your support assistant. How can I help you today?")
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state.is_typing:
            with st.chat_message("assistant"):
                st.markdown("<span class='typing'>Support agent is typing…</span>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input
    user_input = st.chat_input("Describe your issue…")

    if user_input:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )
        st.session_state.pending_user_input = user_input
        st.session_state.is_typing = True
        st.rerun()

# =====================================================
# 8. ASSISTANT RESPONSE LOGIC
# =====================================================
if st.session_state.pending_user_input:
    user_input = st.session_state.pending_user_input
    # Clear pending state immediately to prevent loops
    st.session_state.pending_user_input = None
    
    CONFIG = {"configurable": {"thread_id": st.session_state.thread_id}}

    with right_col:
        with chat_box:
            with st.chat_message("assistant"):
                def stream_response():
                    # Stream the response from the LangGraph agent
                    for chunk, meta in chatbot.stream(
                        {"messages": [HumanMessage(content=user_input)]},
                        config=CONFIG,
                        stream_mode="messages"
                    ):
                        if meta.get("langgraph_node") == "agent" and chunk.content:
                            yield chunk.content
                
                # Write stream to UI and capture full response
                ai_response = st.write_stream(stream_response())

    # Save complete response to history
    st.session_state.chat_history.append(
        {"role": "assistant", "content": ai_response}
    )
    
    # Turn off typing indicator
    st.session_state.is_typing = False
    
    # Save thread ID to session if new
    if st.session_state.thread_id not in st.session_state.chat_threads:
        st.session_state.chat_threads.append(st.session_state.thread_id)


    st.rerun()
