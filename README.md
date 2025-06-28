# Multi-Agent Survival Simulation

## 🏕️ Project Overview

**putos-todos** survival game built on top of Amazon EKS using:
- Large Language Models (Bedrock)
- Vector memory (OpenSearch)
- RAG (Retrieval-Augmented Generation)
- Kubeflow Pipelines for turn-based orchestration

Agents interact, strategize, and compete in a high-stakes survival environment. Each agent has a role, a unique goal, and access to different tools and memory. They communicate through structured natural language chat, simulating emergent behavior.

---

## 🎯 Game Objective

The simulation runs over a series of "days" (turns). Agents must survive.

---

Each agent has:
- A unique **knowledge base** (chunked from RAG)
- Private **state**
- Ability to **chat** with other agents
- Memory of previous rounds

---

## ⚙️ Architecture

### Core Stack:
- **EKS**: Hosts the orchestrated game logic and agent pods
- **Kubeflow Pipeline**: Orchestrates the turn-based round logic
- **OpenSearch**: Used as a vector store for RAG memory
- **S3**: Stores raw logs, game state, and knowledge corpora
- **Bedrock**: LLM inference for agents’ thoughts and chats
- **Flask API**: Optional interface for injecting events or monitoring

---

## 🔁 Game Loop Flow

1. **Environment Setup**: RAG corpus is loaded and assigned to agents
2. **Turn Loop Starts**:
    - Each agent receives the current state and their private goal
    - Agent generates a natural language action or statement
    - All chat is logged
3. **Evaluators** review:
    - Were systems fixed?
    - Was a sabotage successful?
    - Did any agent die or win?
4. **Next Round** begins until win condition or max days

---

## 📦 Project Structure
/agents
├── base_agent.py

/pipelines
└── survival_turn_pipeline.py

/memory
└── vector_store.py

/tools
├── action_simulator.py
└── environment_events.py

/ui
└── dashboard.py  # (optional Streamlit viewer)

main.py  # Entry point to launch the game
---

## 🔐 Features

- 🔄 **Multi-turn simulation** using KFP (Kubeflow Pipelines)
- 🧠 **Tool-augmented agents** (can act, reason, deceive)
- 🔎 **RAG integration** for memory and environmental knowledge
- 💾 **Chat logs + memory persistence**
- 🧪 **Customizable win/lose conditions**
- 🧑‍💻 Easily extendable with new roles or personalities

---

## 🛠️ Dev & Deployment

### Prerequisites:
- Python 3.10+
- AWS EKS + Kubeflow installed
- Bedrock or Ollama set up for LLM access
- OpenSearch running (or FAISS locally)

### Local Dev:
```bash
python main.py --agents 5 --rounds 10