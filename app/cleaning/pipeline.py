from app.cleaning.title_clean import TitleExtractor, TitleNormalizer
from app.cleaning.name_clean import NameNormalizer
from app.models import PassengerClean, PassengerRaw, CleaningStep


class CleanerPipeline:
    def __init__(self, steps: list[CleaningStep]):
        self.steps = steps

    def run(self, raw: PassengerRaw) -> PassengerClean:
        # start from a PassengerClean object populated with raw values
        passenger = PassengerClean(
            Name=raw.Name,
            Age=raw.Age,
            Pclass=raw.Pclass,
            Fare=raw.Fare,
            Title=None,
            Title_Normalized=None,
        )
        for step in self.steps:
            passenger = step.apply(passenger)
        return passenger


def build_titanic_cleaner() -> CleanerPipeline:
    return CleanerPipeline([
        TitleExtractor(),
        TitleNormalizer(),
        NameNormalizer(),
    ])

titanic_cleaner = build_titanic_cleaner()