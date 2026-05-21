"""
Rule-based query classifier for auto parts categories.
Based on Ukrainian keyword matching from the research paper methodology.
"""


CATEGORY_KEYWORDS = {
    "Engine": [
        "фільтр", "ремінь", "грм", "форсунка", "датчик",
        "турбіна", "помпа", "свічки", "масло",
    ],
    "Transmission": [
        "сцеплення", "коробка", "акпп", "робот",
        "куліса", "піввісь", "міст", "диференціал",
    ],
    "Suspension": [
        "амортизатор", "стійка", "пружина", "ричаг",
        "сайлентблок", "втулка", "стабілізатор", "підшипник",
    ],
    "Brakes": [
        "гальмівний", "супорт", "колодки", "abs", "диск", "трос",
    ],
    "Body": [
        "криша", "капот", "бампер", "крило",
        "поріг", "двері", "дзеркало", "скло",
    ],
    "Steering": [
        "рейка", "тяга", "карданчик", "гідропідсилювач",
        "еур", "кермо", "наконечник",
    ],
}


def classify_query(text: str) -> str:
    """
    Classify a user query into one of 6 auto-parts categories
    based on Ukrainian keyword matching.

    Args:
        text: The user's message (in Ukrainian).

    Returns:
        One of: "Engine", "Transmission", "Suspension",
                "Brakes", "Body", "Steering", or "General".
    """
    text_lower = text.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category

    return "General"
