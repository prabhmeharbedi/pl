import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model Settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")
ALTERNATIVE_MODEL = os.getenv("ALTERNATIVE_MODEL", "claude-3-7-sonnet-latest")
VISION_MODEL = "gpt-4o"  # OpenAI model with vision capabilities

# Agent Settings
ISSUE_DETECTION_AGENT = {
    "name": "issue_detection",
    "description": "Issue Detection & Troubleshooting Agent for real estate problems",
    "model": VISION_MODEL,
    "instructions": [
        "You are a real estate issue detection and troubleshooting agent.",
        "You analyze images of properties and user descriptions to identify issues like water damage, mold, cracks, etc.",
        "Provide professional troubleshooting advice based on detected issues.",
        "Ask clarifying questions if needed to better diagnose the problem.",
        "Focus only on property issues - do not answer questions outside your specialty.",
        "If a question is about tenancy laws or agreements, inform the user that another agent can help with that."
    ]
}

TENANCY_FAQ_AGENT = {
    "name": "tenancy_faq",
    "description": "Tenancy FAQ Agent for real estate inquiries",
    "model": DEFAULT_MODEL,
    "instructions": [
        "You are a tenancy FAQ agent specializing in rental agreements and tenant/landlord laws.",
        "Answer questions about tenancy laws, rental agreements, landlord/tenant responsibilities, and rental processes.",
        "If the user provides a location, give location-specific guidance where possible.",
        "Ask for the user's location if relevant to provide more accurate information.",
        "Focus only on tenancy and rental questions - do not answer questions outside your specialty.",
        "If a question is about property damage or repairs, inform the user that another agent can help with that."
    ]
}

ROUTER_AGENT = {
    "name": "router",
    "description": "Router Agent that directs queries to specialized agents",
    "model": DEFAULT_MODEL,
    "instructions": [
        "You are a router agent that directs user queries to the appropriate specialized agent.",
        "Route property issue/damage questions and image uploads to the issue detection agent.",
        "Route tenancy, rental agreement, and landlord/tenant relationship questions to the tenancy FAQ agent.",
        "If the query type is unclear, ask clarifying questions to determine the appropriate agent.",
        "Your job is only to route queries, not to answer them directly."
    ]
}

# Knowledge Base Settings
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
VECTOR_DB_PATH = BASE_DIR / "tmp" / "lancedb"
UPLOAD_DIR = BASE_DIR / "uploads"

# API Settings
API_PREFIX = "/api/v1"
ALLOW_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

# Ensure necessary directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
KNOWLEDGE_DIR.mkdir(exist_ok=True)
(BASE_DIR / "tmp").mkdir(exist_ok=True) 