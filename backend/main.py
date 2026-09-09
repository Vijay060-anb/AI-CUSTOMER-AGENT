from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.customer_agent import process_customer_message
from agent.conversation_memory import add_message
from integrations.n8n import send_to_n8n
from backend.logger import log_interaction


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="AI Customer Support Agent",
    description=(
        "Hybrid AI customer support agent "
        "with business workflows."
    ),
    version="1.0.0",
)


# =========================================================
# STATIC FRONTEND
# =========================================================

app.mount(
    "/static",
    StaticFiles(
        directory="frontend"
    ),
    name="static",
)


# =========================================================
# CHAT REQUEST MODEL
# =========================================================

class ChatRequest(BaseModel):

    message: str

    conversation_id: Optional[str] = ""

    order_id: Optional[str] = ""

    new_item: Optional[str] = ""

    customer_id: Optional[str] = ""

    customer_name: Optional[str] = ""

    email: Optional[str] = ""

    new_address: Optional[str] = ""


# =========================================================
# CUSTOMER AGENT PIPELINE
# =========================================================

def run_customer_agent(
    request: ChatRequest
):

    # -----------------------------------------------------
    # 1. PROCESS CUSTOMER MESSAGE
    # -----------------------------------------------------

    result = process_customer_message(
        message=request.message,

        conversation_id=request.conversation_id,

        order_id=request.order_id,

        new_item=request.new_item,

        customer_id=request.customer_id,

        customer_name=request.customer_name,

        email=request.email,

        new_address=request.new_address,
    )


    # -----------------------------------------------------
    # 2. STORE AGENT RESPONSE IN CONVERSATION MEMORY
    # -----------------------------------------------------

    add_message(
        request.conversation_id,
        "agent",
        result.get(
            "response",
            ""
        )
    )


    # -----------------------------------------------------
    # 3. SEND RESULT TO N8N
    # -----------------------------------------------------

    n8n_result = send_to_n8n(
        result
    )

    result["n8n"] = n8n_result


    # -----------------------------------------------------
    # 4. ADD SESSION INFORMATION
    # -----------------------------------------------------

    result["conversation_id"] = (
        request.conversation_id
    )

    if not result.get("order_id"):
    	result["order_id"] = request.order_id
    result["customer_name"] = (
        request.customer_name
    )


    # -----------------------------------------------------
    # 5. LOG INTERACTION
    # -----------------------------------------------------

    try:

        log_interaction(
            result
        )

    except Exception as error:

        print(
            "Warning: interaction logging failed: "
            f"{error}"
        )


    # -----------------------------------------------------
    # 6. RETURN RESPONSE
    # -----------------------------------------------------

    return result


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return FileResponse(
        "frontend/index.html"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# CHAT ENDPOINT
# =========================================================

@app.post("/chat")
def chat(
    request: ChatRequest
):

    return run_customer_agent(
        request
    )


# =========================================================
# BACKWARD-COMPATIBLE API ENDPOINT
# =========================================================

@app.post("/api/chat")
def api_chat(
    request: ChatRequest
):

    return run_customer_agent(
        request
    )
