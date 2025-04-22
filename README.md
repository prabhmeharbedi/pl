# P-Bot: Multi-Agent Property Assistant

## Overview
P-Bot is an AI-powered assistant designed to help users with property-related issues, combining text and image-based support. It leverages multiple specialized agents to answer tenancy questions, detect issues from images, and provide troubleshooting advice.

---

## Tools & Technologies Used

- **Python 3.10+** (Backend)
- **FastAPI** (API server)
- **Agno Framework** (agent orchestration, memory, and tool integration)
- **OpenAI GPT & Anthropic Claude** (LLM models for agent reasoning)
- **Pillow (PIL)** (image processing)
- **DuckDuckGoTools** (web search for agents)
- **Frontend:** React (in `frontend/`), with modern UI/UX
- **Other:** Pydantic, dotenv, and more (see `requirements.txt`)

---

## Logic Behind Agent Switching

P-Bot uses a modular, multi-agent architecture:

- **Router Agent:**
  - Analyzes each user query (and context, e.g., image presence).
  - Decides which specialized agent should handle the request:
    - **Issue Detection Agent:** For property damage, maintenance, troubleshooting, or when an image is provided.
    - **Tenancy FAQ Agent:** For questions about tenancy laws, agreements, or rights.
  - The router uses both explicit signals (e.g., image attached) and LLM-based classification of the query.
  - If the router fails, the system defaults to the most likely agent based on input type.

- **Session Context:**
  - Session IDs and conversation history are maintained for continuity and smooth agent transitions.

---

## How Image-Based Issue Detection Works

1. **Image Upload:** User uploads an image (e.g., of property damage).
2. **Preprocessing:**
   - Image is opened and resized (max 1024px) to optimize for LLM token limits.
   - Converted to RGB and encoded as base64.
3. **Agent Processing:**
   - The Issue Detection Agent receives both the user message and the image.
   - The image is passed to a vision-capable LLM (e.g., GPT-4 with vision) via the Agno framework.
   - The agent analyzes the image and text, then provides a diagnosis or troubleshooting steps.
4. **Response:**
   - The result is returned to the user, possibly with annotated suggestions or next steps.

---

## Use Case Examples Covered

- **Device/Property Troubleshooting:**
  - "What's wrong with this wall?" [+ image]
  - "How do I fix this leaky faucet?" [+ image]
  - "Is this mold or just a stain?" [+ image]
- **Tenancy FAQ:**
  - "How much notice do I need to give before moving out?"
  - "Can my landlord increase rent during the lease term?"
  - "What should I do if my landlord won't return my deposit?"
- **Hybrid Scenarios:**
  - User starts with a text query, then uploads an image for clarification; the system switches agents as needed.
- **Automatic Escalation:**
  - If the initial agent cannot resolve the issue, the system escalates to a more specialized agent automatically.

---

## Getting Started

See `QUICKSTART.md` for setup and usage instructions. 