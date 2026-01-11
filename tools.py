from langchain.tools import tool
import uuid
from storage.ticket_store import save_ticket, create_ticket_document

import re  # Added for validation

@tool
def check_order_status(order_id: str) -> str:
    """
    Check order status using order ID. 
    Use this when the user asks where their package is or for tracking info.
    """
    # Simple validation mock
    clean_id = order_id.strip()
    if not clean_id:
        return "Error: No Order ID provided. Please ask the user for their Order ID."
    
    # Mock database lookup
    # In a real app, you'd query a SQL DB here
    mock_db = {
        "ORD-123": "In Transit - Arriving Tomorrow",
        "ORD-456": "Delivered - Left at Front Porch",
        "ORD-789": "Processing - Ready to Ship",
        "ORD-890": "Returned - ordered recieved"
    }
    
    status = mock_db.get(clean_id)
    if status:
        return f"Order {clean_id}: {status}"
    else:
        return f"I couldn't find order '{clean_id}'. Please verify the ID."

@tool
def initiate_return(order_id: str, reason: str) -> str:
    """
    Initiate a return. REQUIRE both 'order_id' and 'reason' from the user.
    """
    if not order_id or not reason:
        return "Error: Missing order_id or reason. Ask the user for details."

    return (
        f"✅ Return successfully initiated for {order_id}.\n"
        f"Reason recorded: '{reason}'.\n"
        f"A return label has been emailed to you."
    )

@tool
def create_support_ticket(issue: str) -> str:
    """
    Create and store a support ticket for unresolved issues.
    """
    ticket_id = str(uuid.uuid4())[:8]

    ticket_doc = create_ticket_document(
        issue=issue,
        ticket_id=ticket_id
    )

    save_ticket(ticket_doc)

    return (
        f"🎫 Support ticket created successfully!\n"
        f"Ticket ID: {ticket_id}\n"
        f"Issue: {issue}\n"
        f"Our support team will contact you within 24 hours."
    )


@tool
def escalate_to_human() -> str:
    """
    Escalate the conversation to a human support agent.
    """
    return (
        "📞 I’m escalating this to a human support agent.\n"
        "You’ll be contacted shortly. Thank you for your patience."
    )


from rag.retriever import get_retriever

# --- Load Retrievers ---
# We load them once at startup
retriever_returns = get_retriever("returns")
retriever_shipping = get_retriever("shipping")
retriever_general = get_retriever("general")

# --- Define Specific Tools ---

@tool
def search_return_policy(query: str) -> str:
    """
    Useful for questions about refunds, returning items, money back, or exchange policies.
    """
    if not retriever_returns:
        return "Return policy documents are not available."
    docs = retriever_returns.invoke(query)
    return "\n\n".join([d.page_content for d in docs])

@tool
def search_shipping_policy(query: str) -> str:
    """
    ONLY use this for delivery, tracking, shipping costs, or carrier info.
    DO NOT use for payments or returns.
    """
    if not retriever_shipping:
        return "Shipping policy documents are not available."
    docs = retriever_shipping.invoke(query)
    return "\n\n".join([d.page_content for d in docs])

@tool
def search_general_faq(query: str) -> str:
    """
    Useful for general questions about the company, hours of operation, or contact info.
    """
    if not retriever_general:
        return "FAQ documents are not available."
    docs = retriever_general.invoke(query)
    return "\n\n".join([d.page_content for d in docs])



TOOLS = [check_order_status, 
         initiate_return, 
         create_support_ticket, 
         escalate_to_human, 
         search_return_policy,
         search_shipping_policy, 
         search_general_faq]

