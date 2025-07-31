# EKS Diagnostic AI Agent

This project implements an AI-powered assistant to interact with an Amazon EKS (Elastic Kubernetes Service) cluster. The goal is to provide DevOps engineers with a conversational interface to **scan**, **diagnose**, and **triage** Kubernetes-related issues in a human-readable way.

The AI agent runs as a backend service powered by LangChain and AWS Bedrock, and is accessed through a separate **Streamlit** frontend dashboard.

---

##  Core Features

- **Cluster Scanning**
  - List all nodes, pods, and services
  - Check resource usage and status

- **Diagnosis**
  - Analyze pod events and logs
  - Identify failed or unhealthy workloads
  - Highlight resource constraints or misconfigurations

- **Triage and Recommendations**
  - Summarize root causes in natural language
  - Propose next actions (e.g., restart pods, change resource limits)
  - Explain EKS/K8s concepts to assist junior engineers

---

## Directory Structure (Planned)
aip3-curso/
├── agents/                  # LangChain agents setup (diagnostic, triage)
│   └── eks_diagnostic.py
│
├── tools/                   # Custom LangChain tools wrapping kubectl/eksctl
│   ├── scan.py
│   ├── diagnose.py
│   └── utils.py
│   └── auth.py 
│
├── prompts/                 # Prompt templates
│   └── eks_agent_prompt.py
│
├── core/                    # LLM + Bedrock integration
│   └── bedrock_client.py
│
├── app.py                   # FastAPI or Flask API to serve agent results
├── requirements.txt
└── README.md

> The `Streamlit` frontend lives in a separate repo or folder (e.g., `eks-dashboard/`).

---

##  Technologies

- **LangChain** for agent orchestration
- **AWS Bedrock** for LLM generation (Claude, Titan, etc.)
- **kubectl / eksctl** for interacting with EKS cluster
- **Streamlit** for frontend
- Optional: Redis for caching, logging for audit trail

---

##  Planned Agents

| Agent Name         | Role                                                             |
|--------------------|------------------------------------------------------------------|
| `EKSScanAgent`     | Gathers information using `kubectl get` and `describe` commands |
| `EKSDiagnoseAgent` | Parses symptoms, errors, and logs to identify root causes        |
| `EKSTriageAgent`   | Recommends actions and explains possible fixes in plain English |

---

## Next Tasks

### Setup
- [ ] Scaffold project with initial folders and base files
- [ ] Configure AWS Bedrock access and LLM wrapper (`core/bedrock_client.py`)
- [ ] Write prompt templates for `diagnostic` and `triage` agents

### Tools
- [ ] Implement `kubectl` wrapper tools for:
  - [ ] Node and pod scanning
  - [ ] Log extraction
  - [ ] Event inspection

### Agent Flow
- [ ] Create LangChain-compatible agents for:
  - [ ] Scan phase
  - [ ] Diagnosis
  - [ ] Triage and explanation

### Streamlit
- [ ] Create input box + output rendering for responses
- [ ] Add mode toggles (Scan, Diagnose, Triage)

---

##  Goals

- Help DevOps engineers quickly understand EKS problems
- Translate raw Kubernetes output into readable insights
- Provide AI-backed guidance with explainable actions

---

##  Author
- Built with an AI-assisted DevOps engineer