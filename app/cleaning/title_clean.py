import re

from app.models import PassengerClean, CleaningStep

# match pattern starting with a comma, followed by 0 or serveral whitespaces,
# then capturing any characters that are not a period until a period is encountered.
_TITLE_REGEX = re.compile(r",\s*([^\.]+)\.")

_TITLE_MAP = {
"mr": "Mr",
"sir": "Mr",
"mrs": "Mrs",
"miss": "Mrs",
"ms": "Mrs",
"mme": "Mrs",
"mlle": "Mrs",
"lady": "Mrs",
}


class TitleExtractor(CleaningStep):
    def apply(self, passenger: PassengerClean) -> PassengerClean:
        match = _TITLE_REGEX.search(passenger.Name)
        title = None
        if match:
            raw = re.sub(r"[^A-Za-z]", "", match.group(1))
            title = raw or None
        return passenger.model_copy(update={"Title": title})

class TitleNormalizer(CleaningStep):
    def apply(self, passenger: PassengerClean) -> PassengerClean:
        title = passenger.Title
        if not title:
            return passenger.model_copy(update={"Title_Normalized": None})
        key = title.lower()
        norm = _TITLE_MAP.get(key, "Rare")
        return passenger.model_copy(update={"Title_Normalized": norm})