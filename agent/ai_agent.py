import json
import os
import re
from typing import Dict, Any

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


MODEL = "openai/gpt-oss-120b"


VALID_INTENTS = {
    "edit_account",
    "switch_account",
    "check_invoice",
    "complaint",
    "contact_customer_service",
    "delivery_period",
    "registration_problems",
    "check_payment_methods",
    "contact_human_agent",
    "payment_issue",
    "newsletter_subscription",
    "get_invoice",
    "place_order",
    "cancel_order",
    "track_refund",
    "change_order",
    "get_refund",
    "create_account",
    "check_refund_policy",
    "review",
    "set_up_shipping_address",
    "delivery_options",
    "delete_account",
    "recover_password",
    "track_order",
    "change_shipping_address",
    "check_cancellation_fee",
}


SYSTEM_PROMPT = """
You are an AI customer support intent classifier.

Your job is to classify a customer's message into exactly ONE
of the allowed intents.

You MUST return valid JSON.

Return ONLY this format:

{
  "intent": "one_allowed_intent",
  "confidence": 0.95,
  "reason": "short explanation"
}

Do not return markdown.
Do not return code fences.
Do not return additional text.

Allowed intents:

ACCOUNT:
- create_account
- delete_account
- edit_account
- recover_password
- registration_problems
- switch_account

CANCEL:
- check_cancellation_fee

CONTACT:
- contact_customer_service
- contact_human_agent

DELIVERY:
- delivery_options
- delivery_period

FEEDBACK:
- complaint
- review

INVOICE:
- check_invoice
- get_invoice

ORDER:
- cancel_order
- change_order
- place_order
- track_order

PAYMENT:
- check_payment_methods
- payment_issue

REFUND:
- check_refund_policy
- get_refund
- track_refund

SHIPPING:
- change_shipping_address
- set_up_shipping_address

SUBSCRIPTION:
- newsletter_subscription


IMPORTANT INTENT DISTINCTIONS:

track_order:
Customer wants to know where an existing order is,
its current status, or its location.

Examples:
"Where is my order?"
"Where is my package?"
"Can you track my order?"

delivery_period:
Customer asks how long delivery/shipping normally takes.

Examples:
"How long does shipping take?"
"When will my order arrive?"
"How many days does delivery take?"

change_order:
Customer wants to change an existing order or ordered the wrong item.

Examples:
"I ordered the wrong item."
"Can I change my order?"

change_shipping_address:
Customer wants to change the delivery address.

Examples:
"I entered the wrong address."
"Can I change my shipping address?"

get_refund:
Customer is requesting or starting a refund.

Examples:
"I want a refund."
"Please refund my order."
"Can I get my money back?"

check_refund_policy:
Customer asks about refund rules, eligibility,
conditions, limits, or policy.

Examples:
"What is your refund policy?"
"Am I eligible for a refund?"
"How long do I have to request a refund?"

track_refund:
Customer already requested a refund and wants its status.

Examples:
"Where is my refund?"
"When will my refund arrive?"
"I already requested a refund."

contact_human_agent:
Customer explicitly wants to speak with a human/person/representative.

Examples:
"I want to speak to a human."
"Connect me to an agent."
"I need a real person."

contact_customer_service:
Customer asks how to contact customer service,
without explicitly requesting a human agent.

Examples:
"How can I contact support?"
"What is your support email?"

payment_issue:
Customer reports a payment failure, declined payment,
payment error, or payment problem.

check_payment_methods:
Customer asks which payment methods are accepted.

complaint:
Customer is expressing dissatisfaction or making a complaint.

review:
Customer wants to leave feedback, rating, or review.

For vague messages, choose the most appropriate intent
based on the customer's wording.
"""


def get_client() -> Groq:

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. "
            "Set it in your .env file."
        )

    return Groq(api_key=api_key)


def extract_json(text: str) -> Dict[str, Any]:

    if not text:
        raise ValueError("AI returned an empty response.")

    text = text.strip()


    # Remove markdown code fences if the model adds them.

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()


    # Try the complete response first.

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass


    # Try to find a JSON object inside the response.

    match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL
    )

    if match:

        try:
            return json.loads(
                match.group(0)
            )

        except json.JSONDecodeError:
            pass


    raise ValueError(
        "AI response was not valid JSON."
    )


def validate_result(
    result: Dict[str, Any]
) -> Dict[str, Any]:

    intent = result.get("intent")

    confidence = result.get("confidence")

    reason = result.get("reason", "")


    if intent not in VALID_INTENTS:

        raise ValueError(
            "AI returned invalid intent: "
            + str(intent)
        )


    try:

        confidence = float(confidence)

    except (TypeError, ValueError):

        confidence = 0.0


    confidence = max(
        0.0,
        min(1.0, confidence)
    )


    return {
        "intent": intent,
        "confidence": confidence,
        "reason": str(reason),
    }


def classify_with_ai(
    message: str
) -> Dict[str, Any]:

    if not message or not message.strip():

        return {
            "intent": "contact_customer_service",
            "confidence": 0.0,
            "reason": "The customer message was empty."
        }


    client = get_client()


    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": (
                        "Classify this customer message:\n\n"
                        + message
                    ),
                },
            ],

            temperature=0,

            max_tokens=300,
        )


        content = response.choices[0].message.content


        result = extract_json(content)

        return validate_result(result)


    except Exception as error:

        print(
            "AI classification error:",
            repr(error)
        )


        # Safe fallback.

        return {
            "intent": "contact_customer_service",
            "confidence": 0.0,
            "reason": (
                "AI classification failed. "
                "Fallback customer-service routing was used."
            ),
        }


if __name__ == "__main__":

    test_messages = [

        "Where is my package?",

        "How long does shipping usually take?",

        "I accidentally ordered the wrong item",

        "I want to complain about your service",

        "Can I get a refund for this purchase?",

        "I want to speak to a human agent",

        "I need help with my account",

    ]


    print("=" * 60)

    print("AI CUSTOMER SUPPORT CLASSIFIER TEST")

    print("=" * 60)


    for message in test_messages:

        print()

        print("Message:", message)

        print()

        result = classify_with_ai(message)

        print("Result:")

        print(
            json.dumps(
                result,
                indent=2
            )
        )