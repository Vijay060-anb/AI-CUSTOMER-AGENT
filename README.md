# AI Customer Support Agent

![AI Customer Support Agent](docs/screenshots/customer-support-ui.png)

An end-to-end AI-powered customer support agent that combines machine-learning intent classification, LLM reasoning, business decision trees, external APIs, database integration, workflow automation, conversation memory, and automated evaluation.

The project is designed around realistic SaaS/customer-support workflows such as order tracking, refunds, cancellations, payments, account management, shipping, invoices, subscriptions, and human-agent escalation.

---

## Project Overview

The system uses a **hybrid routing architecture**:

1. A TF-IDF + Logistic Regression classifier handles clear customer requests.
2. Low-confidence or ambiguous requests are sent to an LLM.
3. The final intent is mapped to a business flow.
4. Business logic determines what action should be taken.
5. External systems such as Supabase and n8n are called when required.
6. Conversation memory allows the agent to handle multi-turn interactions.
7. Every interaction is logged for evaluation and optimization.

### Example

```text
Customer
   ↓
FastAPI Backend
   ↓
Hybrid Intent Router
   ├── High-confidence ML → Business Flow
   │
   └── Low-confidence ML → LLM → Business Flow
                                  ↓
                         External Tools / APIs
                                  ↓
                         Supabase / n8n
                                  ↓
                              Response