

# 🛍️ Agente de Soporte al Cliente para E-Commerce

Un **Agente de Soporte al Cliente para la industria del comercio electrónico** impulsado por IA, desarrollado con **LangChain**, **LangGraph**, **Ollama**, **RAG** y **Streamlit**.

![Web Page](assets/Web_Page.png)


Este proyecto simula un sistema de soporte al cliente del mundo real capaz de manejar:
- 📦 Seguimiento de pedidos
- 🚚 Consultas de envío
- 🔄 Devoluciones y reembolsos
- ❓ Preguntas frecuentes generales
- 🎫 Creación de tickets de soporte
- 📞 Escalamiento a agentes humanos

---
## 🧠 Flujo de Trabajo del Agente (LangGraph)

El siguiente diagrama muestra cómo el agente de IA procesa las consultas de los usuarios utilizando un flujo de trabajo basado en LangGraph.

- El nodo del agente razona sobre la consulta del usuario
- Si se requiere una herramienta, la solicitud se enruta al nodo de herramientas
- La salida de la herramienta se envía de vuelta al agente para la respuesta final
- El flujo de trabajo continúa hasta que se genera una respuesta final

![LangGraph Workflow](assets/workflow.png)


---

## 🔍 Trazas de Ejecución en LangSmith

LangSmith se utiliza para monitorear, depurar y analizar cada paso del razonamiento del agente y el uso de herramientas.

A continuación se muestra una captura de una traza de ejecución real que muestra:
- Pasos de razonamiento del agente
- Invocación de herramientas
- Flujo de mensajes entre nodos

![LangSmith Trace](assets/langsmith_trace.png)

---

## 🎥 Demostración en Video

Vea una demostración completa del agente de IA, que incluye:
- Explicación del flujo de trabajo
- Ejecución de herramientas
- Trazas en LangSmith
- Manejo de consultas de extremo a extremo

[![Demostración del Agente de IA](https://img.youtube.com/vi/dlsvk0g1UZs/0.jpg)](https://youtu.be/dlsvk0g1UZs)

---

## 🚀 Stack Tecnológico

- **Python**
- **LangChain & LangGraph**
- **Ollama (LLM local – Qwen)**
- **FAISS (Almacén de vectores)**
- **SQLite (Persistencia de conversaciones)**
- **Streamlit (Interfaz de usuario)**

---

## 🧠 Descripción General de la Arquitectura

- **LangGraph** gestiona el estado del agente, el enrutamiento de herramientas y el flujo de conversaciones
- **Herramientas** manejan el seguimiento de pedidos, devoluciones, tickets y búsqueda basada en RAG
- **RAG** recupera respuestas desde PDFs de políticas (Envíos, Devoluciones, Preguntas frecuentes)
- **Puntos de control en SQLite** habilita chats persistentes con múltiples hilos
- **Interfaz de Streamlit** proporciona una experiencia de soporte al cliente limpia y estilo chat

---

## 📂 Estructura del Proyecto

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

## ⚙️ Cómo Ejecutar el Proyecto

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Aakash109-hub/eCommerce-Customer-Support-Agent.git
cd ecommerce-customer-support-agent
````

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Iniciar Ollama y descargar el modelo

```bash
ollama pull qwen3:4b
ollama run qwen3:4b
```

### 4️⃣ Ejecutar la aplicación de Streamlit

```bash
streamlit run app.py
```

---

## ✨ Características Principales

* 💬 Interfaz de soporte al cliente basada en chat
* 🧠 Agente de IA con uso de herramientas mediante LangGraph
* 📄 Respuestas de políticas impulsadas por RAG desde PDFs
* 🎫 Creación automática de tickets de soporte
* 🔄 Flujo de trabajo para iniciar devoluciones
* 📞 Soporte para escalamiento a humanos
* 💾 Historial de chat persistente con SQLite
* 🖥️ Interfaz de usuario moderna y responsiva

---

## 📌 Casos de Uso

* Automatización de soporte al cliente impulsada por IA
* Sistemas de preguntas y respuestas de documentos basados en RAG
* Demostraciones de orquestación de agentes de IA + herramientas

---

## 🔮 Mejoras Futuras

* Integración con base de datos real para pedidos
* Autenticación y cuentas de usuario
* Panel de administración para tickets
* Soporte multilingüe
* Despliegue en la nube (Docker / AWS)

---

## 👤 Autor

**Aakash**
Ingeniero de IA/ML en formación
Especializado en agentes de IA, sistemas RAG y aplicaciones de LLM del mundo real
