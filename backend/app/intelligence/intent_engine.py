import re


INTENT_KEYWORDS = {

    "ORDER_TRACKING": [
        "where is my order",
        "track my order",
        "order status",
        "delivery status",
        "ఎక్కడ ఉంది",
        "నా ఆర్డర్",
        "ఆర్డర్ ఎక్కడ",
        "मेरा ऑर्डर",
        "ऑर्डर कहाँ है",
        "order kaha hai"
    ],

    "PRODUCT_RETURN": [
        "return my product",
        "return this item",
        "want to return",
        "refund my money",
        "వాపస్ చేయాలి",
        "రిటర్న్ చేయాలి",
        "वापस करना है",
        "मुझे रिटर्न करना है",
        "return karna hai"
    ],

    "PAYMENT_ISSUE": [
        "payment failed",
        "payment problem",
        "money deducted",
        "transaction failed",
        "పేమెంట్ ఫెయిల్",
        "డబ్బులు కట్ అయ్యాయి",
        "पेमेंट फेल",
        "पैसे कट गए",
        "payment nahi hua"
    ],

    "PRODUCT_INFORMATION": [
        "product details",
        "product information",
        "price of product",
        "product availability",
        "ఉత్పత్తి వివరాలు",
        "ధర ఎంత",
        "प्रोडक्ट की जानकारी",
        "इसकी कीमत",
        "product ki price"
    ],

    "ACCOUNT_SUPPORT": [
        "login problem",
        "account problem",
        "forgot password",
        "reset password",
        "లాగిన్ సమస్య",
        "పాస్‌వర్డ్ మర్చిపోయాను",
        "लॉगिन समस्या",
        "पासवर्ड भूल गया",
        "password bhool gaya"
    ],

    "CUSTOMER_SUPPORT": [
        "help me",
        "customer support",
        "need assistance",
        "talk to support",
        "నాకు సహాయం కావాలి",
        "సహాయం చేయండి",
        "मुझे मदद चाहिए",
        "मदद कीजिए"
    ]
}


def normalize_text(text: str) -> str:

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
        flags=re.UNICODE
    )

    text = re.sub(r"\s+", " ", text)

    return text


def detect_intent(text: str):

    if not text or not text.strip():

        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "message": "No customer message provided."
        }

    normalized_text = normalize_text(text)

    detected_intents = {}

    for intent, keywords in INTENT_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            normalized_keyword = normalize_text(keyword)

            if normalized_keyword in normalized_text:

                score += len(normalized_keyword.split())

        if score > 0:
            detected_intents[intent] = score

    if not detected_intents:

        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "message": "Unable to identify customer intent."
        }

    best_intent = max(
        detected_intents,
        key=detected_intents.get
    )

    total_score = sum(
        detected_intents.values()
    )

    confidence = (
        detected_intents[best_intent] / total_score
    ) * 100

    return {
        "intent": best_intent,
        "confidence": round(confidence, 2),
        "message": "Customer intent identified successfully."
    }