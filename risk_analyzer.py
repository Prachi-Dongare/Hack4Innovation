risk_history = []


def get_risk_level(confidence):

    if confidence > 0.95:
        return "HIGH"

    if confidence > 0.80:
        return "MEDIUM"

    return "LOW"


def update_risk(label, confidence):

    level = get_risk_level(confidence)

    risk_history.append(level)

    critical_alert = False

    if len(risk_history) >= 3 and risk_history[-1] == "HIGH":
        if risk_history[-2] == "HIGH":
            critical_alert = True

    return level, risk_history, critical_alert