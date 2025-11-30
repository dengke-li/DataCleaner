import re

from app.models import PassengerClean, CleaningStep


class NameNormalizer(CleaningStep):
    def apply(self, passenger: PassengerClean) -> PassengerClean:
        name = passenger.Name.strip()
        name = re.sub(r"\s+", " ", name)
        name = " ".join(part.capitalize() for part in name.split())
        return passenger.model_copy(update={"Name": name})
