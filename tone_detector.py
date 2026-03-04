def detect_indicators(text):

    keywords = [
        "otp",
        "account blocked",
        "urgent",
        "bank verification",
        "share your otp",
        "immediately"
    ]

    found = []

    lower = text.lower()

    for k in keywords:
        if k in lower:
            found.append(k)

    return found