
# 🛍️ E-Commerce Customer Support Agent

An AI-powered **Customer Support Agent for the eCommerce industry**, built using **LangChain**, **LangGraph**, **Ollama**, **RAG**, and **Streamlit**.

<img width="1920" height="1020" alt="Screenshot 2026-01-11 152549" src="https://github.com/user-attachments/assets/dd4b3beb-4b46-481c-a223-d06c19a45643" />


This project simulates a real-world customer support system capable of handling:
- 📦 Order tracking
- 🚚 Shipping queries
- 🔄 Returns & refunds
- ❓ General FAQs
- 🎫 Support ticket creation
- 📞 Escalation to human agents

---

## 🚀 Tech Stack

- **Python**
- **LangChain & LangGraph**
- **Ollama (Local LLM – Qwen)**
- **FAISS (Vector Store)**
- **SQLite (Conversation persistence)**
- **Streamlit (Frontend UI)**

---

## 🧠 Architecture Overview

- **LangGraph** manages agent state, tool routing, and conversation flow
- **Tools** handle order tracking, returns, tickets, and RAG-based search
- **RAG** retrieves answers from policy PDFs (Shipping, Returns, FAQs)
- **SQLite Checkpointing** enables multi-threaded persistent chats
- **Streamlit UI** provides a clean, chat-style customer support experience

---

## 📂 Project Structure

```

Project/
├── app.py                    # Streamlit UI
├── main.py                   # LangGraph agent & workflow
├── tools.py                  # Tools (orders, returns, RAG, tickets)
├── prompt.py                 # System prompt
├── requirements.txt
├── Storage/
│   ├── ticket_store.py       # Ticket persistence
│   └── tickets.json
└── rag/
    ├── retriever.py          # FAISS retriever loader
    ├── vectorstores/         # FAISS indexes
    └── docs/
       ├── returns/
       ├── shipping/
       └── general/

````

---

## ⚙️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Aakash109-hub/ecommerce-customer-support-agent.git
cd ecommerce-customer-support-agent
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start Ollama & pull model

```bash
ollama pull qwen3:4b
ollama run qwen3:4b
```

### 4️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

---

## ✨ Key Features

* 💬 Chat-based customer support interface
* 🧠 Tool-using AI agent with LangGraph
* 📄 RAG-powered policy answering from PDFs
* 🎫 Automatic support ticket creation
* 🔄 Return initiation workflow
* 📞 Human escalation support
* 💾 Persistent chat history with SQLite
* 🖥️ Modern, responsive UI

---

## 📌 Use Cases

* AI-powered customer support automation
* RAG-based document Q&A systems
* AI agent + tool orchestration demos

---

## 🔮 Future Improvements

* Real database integration for orders
* Authentication & user accounts
* Admin dashboard for tickets
* Multi-language support
* Deployment on cloud (Docker / AWS)

---

## 👤 Author

**Aakash**
Aspiring AI/ML Engineer
Focused on AI Agents, RAG systems, and real-world LLM applications
